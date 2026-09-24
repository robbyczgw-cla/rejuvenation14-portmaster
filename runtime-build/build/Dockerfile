FROM ubuntu:22.04@sha256:b8b6ee6aa931ecd9d0d952abc34dc0e5f7c6a30c6bb71b079fe399fde0329c02
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates git wget curl build-essential cmake autoconf automake libtool \
    pkg-config ruby bison xxd zlib1g-dev libbz2-dev libgl1-mesa-dev libegl1-mesa-dev \
    libasound2-dev libpulse-dev ninja-build python3-pip python3-dev \
    libwayland-dev wayland-protocols libxkbcommon-dev libdecor-0-dev libudev-dev \
    libffi-dev libyaml-dev libgdbm-dev libreadline-dev libncurses-dev libcrypt-dev \
    libexpat1-dev gettext patchelf file unzip rsync \
    && python3 -m pip install --no-cache-dir meson==1.5.2 cmake==3.31.6 \
    && dpkg-query -W > /build-packages.tsv
WORKDIR /work
CMD ["bash", "/recipe/build.sh"]
