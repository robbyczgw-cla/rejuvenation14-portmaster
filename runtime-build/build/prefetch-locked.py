"""Restore the exact dependency commits recorded by package.py before make."""
import json
import hashlib
from pathlib import Path
import shutil
import subprocess as sp

root = Path('/work/source')
lock = Path('/recipe/source-locks.json')
if lock.exists():
    for item in sorted(json.loads(lock.read_text()), key=lambda x: (x['path'].count('/'), x['path'])):
        if item['path'] == '.':
            continue
        dest = root / item['path']
        if not (dest / '.git').exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            sp.check_call(['git', 'clone', '--no-checkout', item['url'], str(dest)])
        sp.check_call(['git', '-C', str(dest), 'fetch', 'origin', item['commit']])
        sp.check_call(['git', '-C', str(dest), 'checkout', '--detach', item['commit']])
archive_lock = Path('/recipe/download-SHA256SUMS')
if archive_lock.exists():
    for line in archive_lock.read_text().splitlines():
        digest, name = line.split('  ', 1)
        target = root / 'linux/downloads/aarch64' / name
        archived = Path('/recipe/source-archives') / name
        if archived.exists() and not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(archived, target)
        if target.exists():
            assert hashlib.sha256(target.read_bytes()).hexdigest() == digest, name
