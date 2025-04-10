{pkgs}: {
  deps = [
    pkgs.lsof
    pkgs.python312Packages.pytest
    pkgs.geckodriver
    pkgs.gdb
    pkgs.libffi
    pkgs.zlib
    pkgs.openjpeg
    pkgs.libwebp
    pkgs.libtiff
    pkgs.libjpeg
    pkgs.libimagequant
    pkgs.lcms2
    pkgs.tk
    pkgs.tcl
    pkgs.qhull
    pkgs.gtk3
    pkgs.gobject-introspection
    pkgs.ghostscript
    pkgs.freetype
    pkgs.ffmpeg-full
    pkgs.cairo
    pkgs.gitFull
    pkgs.libcxx
    pkgs.cacert
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.chromedriver
    pkgs.glibcLocales
    pkgs.zeromq
    pkgs.coreutils
    pkgs.xsimd
    pkgs.pkg-config
    pkgs.libxcrypt
    pkgs.postgresql
    pkgs.openssl
  ];
}
