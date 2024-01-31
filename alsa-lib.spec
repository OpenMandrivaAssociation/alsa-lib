# 32-bit devel files are needed for wine

%define major 2
%define oldlib %mklibname alsa %{major}
%define olddev %mklibname -d alsa2
%define libname %mklibname asound %{major}
%define libtopology %mklibname topology %{major}
%define devname %mklibname -d asound
%define lib32name libasound%{major}
%define lib32topology libtopology%{major}
%define dev32name libasound-devel

Summary:	Config files for Advanced Linux Sound Architecture (ALSA)
Name:		alsa-lib
Version:	1.2.11
Release:	1
Group:		Sound
License:	LGPLv2+
Url:		http://www.alsa-project.org/
Source0:	ftp://ftp.alsa-project.org/pub/lib/%{name}-%{version}.tar.bz2
Source10:	imx6-wandboard-.conf
Source11:	imx-hdmi-soc.conf
Source12:	imx-spdif.conf
Patch0:		alsa-lib-1.2.7-hdmi-audio.patch
BuildRequires:	doxygen
BuildRequires:	pkgconfig(python)
Requires(post):	chkconfig
Requires(postun):	chkconfig
Provides:	libalsa-data = 2:%{version}-%{release}
Obsoletes:	libalsa-data < 2:1.0.26
Conflicts:	%{olddev} < 2:1.0.26

%description
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

Using the ALSA api requires to use the ALSA library.

%package -n	%{libname}
Summary:	Advanced Linux Sound Architecture (ALSA) library
Group:		Sound
Requires:	%{name} = %{EVRD}
Suggests:	%mklibname alsa-plugins
Provides:	%{oldlib} = 2:%{version}-%{release}
Obsoletes:	%{oldlib} < 2:1.0.26

%description -n	%{libname}
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

This package contains config files by ALSA applications.

%package -n	%{libtopology}
Summary:	Advanced Linux Sound Architecture (ALSA) library
Group:		Sound
Requires:	%{libname} = %{EVRD}

%description -n	%{libtopology}
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

This package contains config files by ALSA applications.

%package -n	%{devname}
Summary:	Development files for Advanced Linux Sound Architecture (ALSA)
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Requires:	%{libtopology} = %{EVRD}
Provides:	%{olddev} = 2:%{version}-%{release}
Obsoletes:	%{olddev} < 2:1.0.26
Provides:	libalsa-devel = 2:%{version}-%{release}
Obsoletes:	libalsa-devel < 2:1.0.26

%description -n	%{devname}
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

This package contains files needed in order to develop an application
that made use of ALSA.

%if "%{libname}" != "%{lib32name}"
%package -n	%{lib32name}
Summary:	Advanced Linux Sound Architecture (ALSA) library (32-bit)
Group:		Sound
Requires:	%{name} = %{EVRD}
Suggests:	libalsa-plugins
%ifnarch aarch64
BuildRequires:	libc6
%endif

%description -n	%{lib32name}
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

This package contains config files by ALSA applications.

%package -n	%{lib32topology}
Summary:	Advanced Linux Sound Architecture (ALSA) library (32-bit)
Group:		Sound
Requires:	%{lib32name} = %{EVRD}

%description -n	%{lib32topology}
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

This package contains config files by ALSA applications.

%package -n	%{dev32name}
Summary:	Development files for Advanced Linux Sound Architecture (ALSA) (32-bit)
Group:		Development/C
Requires:	%{lib32name} = %{EVRD}
Requires:	%{lib32topology} = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n	%{dev32name}
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

This package contains files needed in order to develop an application
that made use of ALSA.

%endif

%package docs
Summary:	Documentation for Advanced Linux Sound Architecture (ALSA)
Group:		Books/Howtos
Requires:	%{libname} = %{EVRD}
Provides:	libalsa2-docs = 2:%{version}-%{release}
Obsoletes:	libalsa2-docs < 2:1.0.26

%description	docs
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

The Advanced Linux Sound Architecture comes with a kernel API and library API.
This document describes the library API and how it interfaces with the kernel
API. Application programmers should use the library API rather than kernel API.

The Library offers 100% of the functionally of the kernel API, but add next
major improvements in usability, making the application code simpler and better
looking.

This package contains the documentation that describe the ALSA lib API.

%prep
%autosetup -p1
find . -name Makefile.am -exec sed -i -e '/CFLAGS/s:-g -O2::' {} +

# ensure we enable html doc
sed -i 's/GENERATE_RTF/GENERATE_HTML = YES\nGENERATE_RTF/' doc/doxygen.cfg.in doc/doxygen.cfg

%build
# AS of Clang 16, GCC is needed or 
# warning: version script assignment of 'ALSA_1.1.6' to symbol 'snd_dlopen' failed: symbol not defined
# ld.lld: error: undefined symbol: snd_dlopen
# referenced by dlmisc.c:134 (/builddir/build/BUILD/alsa-lib-1.2.9/src/dlmisc.c:134)
# .libs/dlmisc.o:(__snd_dlopen)
export CC=gcc
export CXX=g++	
export PYTHON=%{__python}
export CONFIGURE_TOP="`pwd`"

#repect cflags
find . -name Makefile.am -exec sed -i -e '/CFLAGS/s:-g -O2::' {} +
libtoolize --copy --force
autoreconf -fiv

if [ -e src/conf/smixer.conf ]; then
	echo "smixer.conf is in tree, remove workaround"
	exit 1
else
	cat >src/conf/smixer.conf <<'EOF'
_full smixer-python.so
usb {
	searchl "USB"
	lib smixer-usb.so
}
ac97 {
	searchl "AC97a:"
	lib smixer-ac97.so
}
hda {
	searchl "HDA:"
	lib smixer-hda.so
}
EOF
fi

%ifarch %{x86_64}
mkdir build32
cd build32
%configure32 \
	--prefix=%{_prefix} \
	--libdir=%{_prefix}/lib \
	--sysconfdir=%{_sysconfdir} \
	--enable-shared \
	--enable-symbolic-functions \
	--enable-aload \
	--enable-rawmidi \
	--enable-seq \
	--enable-mixer \
	--enable-mixer-modules
# The topology Versions file is generated in-tree even for
# an out-of-tree build
cp ../src/topology/Versions src/topology/
%make_build
cd ..
%endif

mkdir build
cd build
%configure \
	--enable-shared \
	--enable-symbolic-functions \
	--enable-aload \
	--enable-rawmidi \
	--enable-seq \
	--enable-python \
	--enable-mixer \
	--enable-mixer-modules \
	--enable-mixer-pymods \
	--with-pythonlibs="`python-config --libs`" \
	--with-pythonincludes="`python-config --includes`"
# The topology Versions file is generated in-tree even for
# an out-of-tree build
cp ../src/topology/Versions src/topology/
# Force definition of -DPIC so that VERSIONED_SYMBOLS are used
# FIXME: alsa people should not depend on PIC to determine a DSO build...
perl -pi -e 's,(^pic_flag=.+)(-fPIC),\1-DPIC \2,' libtool
%make_build PYTHON_LIBS=-lpython%{pyver}

%make -C doc doc

%install
%ifarch %{x86_64}
cd build32
%make_install
cd ..
%endif

cd build
%make_install

%ifarch %{arm}
# (proyvind): configuration for wandboard
install -m644 %{SOURCE10} %{SOURCE11} %{SOURCE12} %{buildroot}%{_datadir}/alsa/cards
%endif

%files
%{_bindir}/aserver
%dir %{_datadir}/alsa/
%dir %{_datadir}/alsa/cards/
%dir %{_datadir}/alsa/ctl
%dir %{_datadir}/alsa/pcm/
%{_datadir}/alsa/cards/*
%{_datadir}/alsa/pcm/*
%{_datadir}/alsa/alsa.conf
%{_datadir}/alsa/smixer.conf
%{_datadir}/alsa/ctl/default.conf
%dir %{_libdir}/alsa-lib/
%dir %{_libdir}/alsa-lib/smixer/
%{_libdir}/alsa-lib/smixer/*

%files -n %{libname}
%{_libdir}/libasound.so.%{major}*
%{_libdir}/alsa-lib

%files -n %{libtopology}
%{_libdir}/libatopology.so.%{major}*

%ifarch %{x86_64}
%files -n %{lib32name}
%{_prefix}/lib/libasound.so.%{major}*
%{_prefix}/lib/alsa-lib

%files -n %{lib32topology}
%{_prefix}/lib/libatopology.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif

%files -n %{devname}
%dir %{_includedir}/alsa/
%{_includedir}/alsa/*
%{_includedir}/asoundlib.h
%{_includedir}/sys/asoundlib.h
%{_datadir}/aclocal/alsa.m4
%{_libdir}/libasound.so
%{_libdir}/libatopology.so
%{_libdir}/pkgconfig/alsa-topology.pc
%{_libdir}/pkgconfig/alsa.pc

%files docs
%doc COPYING build/doc/doxygen/html/* doc/asoundrc.txt
