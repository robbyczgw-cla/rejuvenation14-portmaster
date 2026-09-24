#!/bin/bash
set -euo pipefail
test "$(uname -m)" = aarch64
test "$(dpkg --print-architecture)" = arm64
mkdir -p /out/evidence
cp /build-packages.tsv /out/evidence/build-packages.tsv
if [ ! -d /work/source/.git ]; then
  git clone https://github.com/enumag/mkxp-z.git /work/source
fi
cd /work/source
git checkout --detach afce4ce68404fb19383e00fe415b86dcc3aa214c
python3 /recipe/prefetch-locked.py
python3 /recipe/patch-build.py
git diff -- linux/Makefile > /out/evidence/build-adaptations.patch
controller_patch=/out/patches/0001-open-all-gamecontrollers.patch
axis_patch=/out/patches/0002-ignore-inactive-controller-axis-noise.patch
if git apply --reverse --check "$axis_patch" 2>/dev/null; then
  echo 'Controller patches 0001 and 0002 already applied'
else
  if git apply --reverse --check "$controller_patch" 2>/dev/null; then
    echo 'Controller patch 0001 already applied'
  else
    git apply --check "$controller_patch"
    git apply "$controller_patch"
  fi
  git apply --check "$axis_patch"
  git apply "$axis_patch"
fi
git diff -- src/eventthread.cpp > /out/evidence/controller-adaptations.patch
cp .github/workflows/autobuild.yml /out/evidence/official-autobuild.yml
cd linux
if [ -f downloads/aarch64/openal/cmakebuild/CMakeCache.txt ]; then
  cmake -S downloads/aarch64/openal -B downloads/aarch64/openal/cmakebuild
fi
make NPROC=6
cd ..
# Official workflow restores Ruby's duplicated DESTDIR prefix here.
set +u
source linux/vars.sh
set -u
cp icons/rejuvenation.png assets/icon.png
if [ -f build/build.ninja ]; then
  meson setup --reconfigure build --prefix=/opt/mkxp-z --bindir=. -Dappimage=false -Dworkdir_current=true
else
  meson setup build --prefix=/opt/mkxp-z --bindir=. -Dappimage=false -Dworkdir_current=true
fi
meson compile -C build -j 6
cc /recipe/runtime-probe.c -o /work/runtime-probe $(pkg-config --cflags --libs --static sdl2)
python3 /recipe/check-controllers.py | tee /out/evidence/controller-test3.txt
python3 /recipe/package.py
