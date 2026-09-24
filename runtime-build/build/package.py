import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess as sp

src = Path('/work/source')
prefix = src / 'linux/build-aarch64'
out = Path('/out')
lib = out / 'lib'
evidence = out / 'evidence'
licenses = out / 'licenses'
# Recollect generated libraries so incremental and fresh bundles match.
if lib.exists():
    shutil.rmtree(lib)
for p in (lib, evidence, licenses, out / 'tools'):
    p.mkdir(parents=True, exist_ok=True)

def run(*args):
    return sp.check_output(args, text=True, stderr=sp.STDOUT)

shutil.copy2(src / 'build/mkxp-z.aarch64', out / 'mkxp-z.aarch64')
for generated in (out / 'stdlib', out / 'stdlib-aarch64-linux'):
    if generated.exists():
        shutil.rmtree(generated)
shutil.copytree(prefix / 'lib/ruby/3.1.0', out / 'stdlib', dirs_exist_ok=True)
arch = out / 'stdlib/aarch64-linux'
assert arch.is_dir(), list((out / 'stdlib').iterdir())
native = out / 'stdlib-aarch64-linux'
shutil.copytree(arch, native, dirs_exist_ok=True)
shutil.rmtree(arch)
arch.symlink_to('../stdlib-aarch64-linux')
rbconfig = native / 'rbconfig.rb'
rbconfig.write_text(re.sub(r'TOPDIR \|\| DESTDIR \+ "[^"]*"', 'TOPDIR || DESTDIR + ""', rbconfig.read_text()))
rg = out / 'stdlib/rubygems.rb'
rg.write_text(rg.read_text().replace('Gem::Specification.load_defaults', '#Gem::Specification.load_defaults'))
shutil.copy2(prefix / 'bin/ruby', out / 'tools/ruby')
shutil.copy2('/work/runtime-probe', out / 'tools/runtime-probe')
shutil.copy2('/etc/ssl/certs/ca-certificates.crt', out / 'cacert.pem')
shutil.copy2('/recipe/check-ruby.rb', out / 'tools/check-ruby.rb')
shutil.copy2('/recipe/check-odin.sh', out / 'tools/check-odin.sh')
shutil.copy2('/recipe/run.sh', out / 'run.sh')

# Keep the target's glibc/loader, graphics and platform integration libraries.
system = re.compile(r'^(ld-linux-aarch64\.so\.1|lib(c|m|dl|pthread|rt|resolv|util|anl)\.so\.[0-9]+|lib(GL|GLX|GLdispatch|EGL|GLESv[12]|gbm|drm|drm_[a-z0-9]+)\.so\..*)$')
hostprovided = re.compile(r'^lib(wayland-(client|cursor|egl)|xkbcommon|decor.*|udev|dbus.*|pulse.*|asound)\.so(?:\..*)?$')
seeds = [out / 'mkxp-z.aarch64', out / 'tools/ruby', out / 'tools/runtime-probe']
seeds += list(native.rglob('*.so'))
dynamic_names = set(re.findall(r'^#define SDL_\S*DYNAMIC\S* "([^"]+)"', (prefix / 'include/SDL2/SDL_config.h').read_text(), re.M))
dynamic_names.update(('libwayland-client.so.0', 'libwayland-cursor.so.0', 'libwayland-egl.so.1',
             'libxkbcommon.so.0', 'libdecor-0.so.0', 'libpulse.so.0', 'libasound.so.2',
             'libpulse-simple.so.0', 'libudev.so.1', 'libdbus-1.so.3'))
for name in sorted(dynamic_names):
    if system.match(name) or hostprovided.match(name):
        continue
    paths = list(prefix.glob('lib/' + name)) + list(Path('/usr/lib/aarch64-linux-gnu').glob(name))
    assert paths, name
    dest = lib / name
    shutil.copy2(paths[0].resolve(), dest)
    seeds.append(dest)

origins = {}
seen = set()
queue = list(seeds)
ldd_logs = []
while queue:
    obj = queue.pop(0)
    if str(obj) in seen:
        continue
    seen.add(str(obj))
    output = run('ldd', str(obj))
    ldd_logs.append(f'### {obj}\n{output}')
    assert 'not found' not in output, output
    for name, path in re.findall(r'^\s*(\S+) => (/\S+)', output, re.M):
        if system.match(name) or hostprovided.match(name):
            continue
        dest = lib / name
        if not dest.exists():
            shutil.copy2(Path(path).resolve(), dest)
            origins[name] = path
            queue.append(dest)

elfs = [out / 'mkxp-z.aarch64', out / 'tools/ruby', out / 'tools/runtime-probe']
elfs += list(lib.iterdir()) + list(native.rglob('*.so'))
for obj in elfs:
    relative = os.path.relpath(lib, obj.parent)
    rpath = '$ORIGIN' if relative == '.' else '$ORIGIN/' + relative
    sp.check_call(['patchelf', '--set-rpath', rpath, str(obj)])

(evidence / 'container-ldd.txt').write_text('\n'.join(ldd_logs))
(evidence / 'library-origins.json').write_text(json.dumps(origins, indent=2) + '\n')
required = sorted(set(re.findall(r'GLIBC_([0-9.]+)', '\n'.join(run('readelf', '-V', str(p)) for p in elfs))), key=lambda s: tuple(map(int, s.split('.'))))
assert tuple(map(int, required[-1].split('.'))) <= (2, 41), required
(evidence / 'glibc-symbol-versions.txt').write_text('\n'.join(required) + '\n')
(evidence / 'elf-header.txt').write_text(run('readelf', '-h', str(out / 'mkxp-z.aarch64')))
(evidence / 'sdl-config.h').write_text((prefix / 'include/SDL2/SDL_config.h').read_text())
assert '#define SDL_VIDEO_DRIVER_WAYLAND 1' in (evidence / 'sdl-config.h').read_text()
assert '#define SDL_JOYSTICK_DISABLED 1' not in (evidence / 'sdl-config.h').read_text()

repos = [src] + [p.parent for p in (src / 'linux/downloads/aarch64').rglob('.git') if p.is_dir() or p.is_file()]
locks = []
for repo in sorted(set(repos)):
    locks.append({'path': str(repo.relative_to(src)), 'url': run('git', '-C', str(repo), 'remote', 'get-url', 'origin').strip(),
                  'commit': run('git', '-C', str(repo), 'rev-parse', 'HEAD').strip()})
    label = str(repo.relative_to(src)).replace('/', '__') if repo != src else 'mkxp-z'
    for item in repo.iterdir():
        if re.match(r'(?i)(copying|licen[cs]e|copyright|notice|authors)', item.name):
            (licenses / label).mkdir(exist_ok=True)
            if item.is_file():
                shutil.copy2(item, licenses / label / item.name)
            elif item.is_dir():
                shutil.copytree(item, licenses / label / item.name, dirs_exist_ok=True)
    # Include vendored codec/fmt licenses that are not separate Git repositories.
    for current, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in ('.git', 'cmakebuild', 'build', 'downloads', '.libs', '.deps')
                   and not (Path(current) / d / '.git').exists()]
        for name in files:
            if re.match(r'(?i)^(copying|licen[cs]e|copyright|notice)([._-]|$)', name):
                item = Path(current) / name
                target = licenses / label / item.relative_to(repo)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
(evidence / 'source-locks.json').write_text(json.dumps(locks, indent=2) + '\n')
versions = []
for pc in sorted((prefix / 'lib/pkgconfig').glob('*.pc')):
    version = re.search(r'^Version: (.*)$', pc.read_text(), re.M)
    versions.append(f'{pc.stem}\t{version.group(1) if version else "unknown"}')
(evidence / 'dependency-versions.tsv').write_text('\n'.join(versions) + '\n')
archives = []
for p in sorted((src / 'linux/downloads/aarch64').glob('*')):
    if p.is_file():
        archives.append(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name)
    elif p.is_dir() and not (p / '.git').exists():
        for item in p.iterdir():
            if item.is_file() and re.match(r'(?i)(copying|licen[cs]e|copyright|notice|authors)', item.name):
                (licenses / p.name).mkdir(exist_ok=True)
                shutil.copy2(item, licenses / p.name / item.name)
(evidence / 'download-SHA256SUMS').write_text('\n'.join(archives) + '\n')
shutil.copy2(src / 'assets/LICENSE.mkxp-z-with-https.txt', licenses / 'LICENSE.mkxp-z-with-https.txt')
shutil.copytree('/usr/share/common-licenses', licenses / 'debian-common', dirs_exist_ok=True)
for doc in Path('/usr/share/doc').glob('*/copyright'):
    target = licenses / 'ubuntu-packages' / doc.parent.name
    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(doc, target / 'copyright')
manifest = []
for p in sorted(out.rglob('*')):
    if p.is_file() and not p.is_symlink() and not str(p.relative_to(out)).startswith(('build/', 'evidence/')):
        manifest.append(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + str(p.relative_to(out)))
(evidence / 'SHA256SUMS').write_text('\n'.join(manifest) + '\n')
print('Packaged', len(elfs), 'ELF objects; maximum GLIBC_' + required[-1])
