#!/bin/bash
# Build the installable port zip: launcher + rejuvenation14/ + runtime.
# Usage: tools/make-release.sh <runtime-aarch64.tar.gz> [version]
# Output: dist/rejuvenation14.zip (unzip into the ports folder, add game files).
set -euo pipefail

RUNTIME_TGZ="${1:?usage: $0 <runtime-aarch64.tar.gz> [version]}"
VERSION="${2:-dev}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

mkdir -p "$STAGE/rejuvenation14/runtime"
cp "$ROOT/Rejuvenation V14.sh" "$STAGE/"
chmod +x "$STAGE/Rejuvenation V14.sh"
cp -R "$ROOT/rejuvenation14/." "$STAGE/rejuvenation14/"
cp "$ROOT/port.json" "$ROOT/gameinfo.xml" "$STAGE/rejuvenation14/"
tar -xzf "$RUNTIME_TGZ" -C "$STAGE/rejuvenation14/runtime"

# PortMaster unpacks with Python's zipfile, which turns symlinks into text
# files. The launcher uses stdlib-aarch64-linux directly, so drop links.
find "$STAGE" -type l -print -delete

# Never ship game data or local state.
find "$STAGE/rejuvenation14/game" -mindepth 1 ! -name README.txt -exec rm -rf {} +
rm -rf "$STAGE/rejuvenation14/userdata" "$STAGE/rejuvenation14/mkxp.json" \
       "$STAGE/rejuvenation14/gamecontrollerdb.txt" "$STAGE/rejuvenation14/log.txt"
find "$STAGE" -name .DS_Store -delete
rm -f "$STAGE/rejuvenation14/runtime/run.sh"   # dev-only start script from the runtime build

# The runtime tarball carries build logs; ship the public build docs instead.
RT="$STAGE/rejuvenation14/runtime"
rm -rf "$RT/evidence"
# RDoc (documentation generator, ships CC-BY icon images) is not used at runtime.
rm -rf "$RT/stdlib/rdoc" "$RT/stdlib/rdoc.rb"
cp "$ROOT/runtime-build/BUILD.md" "$ROOT/runtime-build/SOURCE.md" "$RT/"
cp "$ROOT/runtime-build/build/check-odin.sh" "$RT/tools/check-odin.sh"

# Refuse to ship anything that points at the development machine. The
# patterns live in an untracked file (one extended regex per line).
PATTERNS="$ROOT/tools/private-patterns.txt"
if [ -f "$PATTERNS" ] && grep -rIlE -f "$PATTERNS" "$STAGE"; then
  echo "ERROR: private paths or addresses in release files (listed above)" >&2
  exit 1
fi

echo "$VERSION" > "$STAGE/rejuvenation14/PORT_VERSION"
mkdir -p "$ROOT/dist"
rm -f "$ROOT/dist/rejuvenation14.zip"
(cd "$STAGE" && zip -qr -X "$ROOT/dist/rejuvenation14.zip" "Rejuvenation V14.sh" rejuvenation14)
echo "dist/rejuvenation14.zip ($(du -h "$ROOT/dist/rejuvenation14.zip" | cut -f1)), version $VERSION"
shasum -a 256 "$ROOT/dist/rejuvenation14.zip"
