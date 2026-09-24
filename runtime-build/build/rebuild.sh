#!/bin/bash
set -euo pipefail
recipe_dir=$(cd -- "$(dirname -- "$0")" && pwd)
output_dir=$(dirname -- "$recipe_dir")
if [ -f "$recipe_dir/builder-image.tar.gz" ]; then
  gzip -dc "$recipe_dir/builder-image.tar.gz" | docker --context colima image load
else
  docker --context colima build --platform linux/arm64 -t rejuv-enumag-builder:afce4ce "$recipe_dir"
fi
docker --context colima run --rm --platform linux/arm64 \
  --mount type=volume,src=rejuv-enumag-work,dst=/work \
  --mount "type=bind,src=$recipe_dir,dst=/recipe,readonly" \
  --mount "type=bind,src=$output_dir,dst=/out" \
  rejuv-enumag-builder:afce4ce
COPYFILE_DISABLE=1 tar -czf "$recipe_dir/runtime-aarch64.tar.gz" -C "$output_dir" \
  mkxp-z.aarch64 lib stdlib stdlib-aarch64-linux tools run.sh cacert.pem \
  licenses BUILD.md patches evidence
