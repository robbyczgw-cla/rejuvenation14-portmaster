"""Preserve exact Git sources independently of branch/tag movement."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess as sp

root = Path('/work/source')
dest = Path('/out/build/source-archives')
dest.mkdir(exist_ok=True)
locks = json.loads(Path('/out/evidence/source-locks.json').read_text())
for item in locks:
    label = item['path'].replace('/', '__') if item['path'] != '.' else 'mkxp-z'
    target = dest / (label + '.tar.gz')
    with target.open('wb') as f:
        archive = sp.Popen(['git', '-C', str(root / item['path']), 'archive', item['commit']], stdout=sp.PIPE)
        compressed = sp.run(['gzip', '-n'], stdin=archive.stdout, stdout=f, check=True)
        archive.stdout.close()
        if archive.wait() != 0:
            raise RuntimeError(item['path'])
for source in (root / 'linux/downloads/aarch64').glob('*.tar.*'):
    shutil.copy2(source, dest / source.name)
(dest / 'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest() + '  ' + p.name + '\n'
                                     for p in sorted(dest.glob('*.tar.*'))))
