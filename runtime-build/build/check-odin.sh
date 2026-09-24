#!/bin/sh
set -eu
# Runtime folder to check; defaults to the folder containing tools/.
cd "${1:-$(dirname "$0")/..}"
printf '%s\n' '=== Host ==='
uname -m
getconf GNU_LIBC_VERSION
printf '%s\n' '=== Engine dependency check ==='
engine_ldd=$(env LC_ALL=C LD_LIBRARY_PATH="$PWD/lib" ldd ./mkxp-z.aarch64)
printf '%s\n' "$engine_ldd"
case "$engine_ldd" in *"not found"*) exit 1;; esac
printf '%s\n' '=== Every ELF dependency check ==='
find lib stdlib-aarch64-linux tools -type f \( -name '*.so*' -o -name ruby -o -name runtime-probe \) > .elf-files
while IFS= read -r file; do
  report=$(env LC_ALL=C LD_LIBRARY_PATH="$PWD/lib" ldd "$file" 2>&1) || { printf '%s\n%s\n' "$file" "$report"; exit 1; }
  case "$report" in *"not found"*) printf '%s\n%s\n' "$file" "$report"; exit 1;; esac
  printf '%s: OK\n' "$file"
done < .elf-files
printf '%s\n' '=== SDL compile-time capabilities, without SDL_Init ==='
env LD_LIBRARY_PATH="$PWD/lib" ./tools/runtime-probe
printf '%s\n' '=== Ruby ABI and extension checks ==='
env LD_LIBRARY_PATH="$PWD/lib" RUBYLIB="$PWD/stdlib:$PWD/stdlib/aarch64-linux" SSL_CERT_FILE="$PWD/cacert.pem" \
  ./tools/ruby --disable-gems ./tools/check-ruby.rb
printf '%s\n' '=== PASS: no engine/window/game started ==='
