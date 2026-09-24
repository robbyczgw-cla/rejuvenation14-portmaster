from pathlib import Path
import subprocess

p = Path('linux/Makefile')
s = subprocess.check_output(['git', 'show', 'HEAD:linux/Makefile'], text=True)
s = s.replace('--with-static-linked-ext', '--without-static-linked-ext')
s = s.replace('-DSDL_DBUS=yes', '-DSDL_DBUS=yes -DSDL_WAYLAND=ON -DSDL_WAYLAND_LIBDECOR=ON -DSDL_X11=OFF -DSDL_KMSDRM=OFF -DSDL_JOYSTICK=ON -DSDL_HIDAPI=ON')
# Static libraries also feed Ruby shared extensions.
s = s.replace('-flax-vector-conversions -O3', '-flax-vector-conversions -fPIC -O3')
# Make's original PKG_CONFIG_LIBDIR hides the Wayland and libffi development files.
s = s.replace('PKG_CONFIG_LIBDIR := $(BUILD_PREFIX)/lib/pkgconfig', 'PKG_CONFIG_LIBDIR := $(BUILD_PREFIX)/lib/pkgconfig:/usr/lib/aarch64-linux-gnu/pkgconfig:/usr/share/pkgconfig')
# A phony directory prerequisite otherwise reclones an existing D-Bus tree.
s = s.replace('$(DOWNLOADS)/dbus/CMakeLists.txt: init_dirs', '$(DOWNLOADS)/dbus/CMakeLists.txt: | init_dirs')
p.write_text(s)
