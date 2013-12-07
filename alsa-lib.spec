%define major 2

%define oldlib %mklibname alsa %{major}
%define olddev %mklibname -d alsa2

%define libname %mklibname asound %{major}
%define devname %mklibname -d asound

Summary:	Config files for Advanced Linux Sound Architecture (ALSA)
Name:		alsa-lib
Version:	1.0.27.2
Release:	4
Epoch:		2
Group:		Sound
License:	LGPLv2+
Url:		http://www.alsa-project.org/
Source0:	ftp://ftp.alsa-project.org/pub/lib/%{name}-%{version}.tar.bz2
Source1:	README.soundprofiles
BuildRequires:	doxygen
BuildRequires:	python-devel
Requires(post):	update-alternatives
Requires(postun):	update-alternatives
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

%package -n	%{devname}
Summary:	Development files for Advanced Linux Sound Architecture (ALSA)
Group:		Development/C
Requires:	%{libname} = %{EVRD}
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
%setup -q

%build
%configure2_5x \
		--enable-shared \
        --enable-python

# Force definition of -DPIC so that VERSIONED_SYMBOLS are used
# FIXME: alsa people should not depend on PIC to determine a DSO build...
perl -pi -e 's,(^pic_flag=.+)(-fPIC),\1-DPIC \2,' libtool
%make
%make -C doc doc

%install
%makeinstall_std

%ifnarch arm armv7hf armv7hl
# No need to keep ARM-only hardware support...
rm -rf %buildroot%_datadir/ucm/PandaBoard*
%endif

# (cg) For sound profile support
mkdir -p %{buildroot}%{_sysconfdir}/sound/profiles/alsa
echo "SOUNDPROFILE=alsa" > %{buildroot}%{_sysconfdir}/sound/profiles/alsa/profile.conf
echo "# This file is left blank to allow alsa to default to dmix" > %{buildroot}%{_sysconfdir}/sound/profiles/alsa/alsa-default.conf
install -m 644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/sound/profiles/README
ln -s %{_sysconfdir}/sound/profiles/current/alsa-default.conf %{buildroot}%{_datadir}/alsa/alsa.conf.d/99-default.conf

%define alt_name soundprofile
%define alt_priority 10

%post
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/sound/profiles/current %{alt_name} %{_sysconfdir}/sound/profiles/alsa %{alt_priority}

%postun
if [ ! -f %{_sysconfdir}/sound/profiles/alsa/profile.conf ]; then
  /usr/sbin/update-alternatives --remove %{alt_name} %{_sysconfdir}/sound/profiles/alsa
fi

%files
%{_bindir}/aserver
%dir %{_sysconfdir}/sound/profiles
%dir %{_sysconfdir}/sound/profiles/alsa
%{_sysconfdir}/sound/profiles/README
%{_sysconfdir}/sound/profiles/alsa/profile.conf
%{_sysconfdir}/sound/profiles/alsa/alsa-default.conf
%dir %{_datadir}/alsa/
%dir %{_datadir}/alsa/cards/
%dir %{_datadir}/alsa/pcm/
%dir %{_datadir}/alsa/ucm/
%{_datadir}/alsa/cards/*
%{_datadir}/alsa/pcm/*
%{_datadir}/alsa/ucm/*
%{_datadir}/alsa/alsa.conf
%{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/smixer.conf
%{_datadir}/alsa/sndo-mixer.alisp
%dir %{_libdir}/alsa-lib
%dir %{_libdir}/alsa-lib/smixer/
%{_libdir}/alsa-lib/smixer/*

%files -n %{libname}
%{_libdir}/libasound.so.%{major}*

%files -n %{devname}
%dir %{_includedir}/alsa/
%{_includedir}/alsa/*
%{_includedir}/sys/asoundlib.h
%{_datadir}/aclocal/alsa.m4
%{_libdir}/libasound.so
%{_libdir}/pkgconfig/alsa.pc

%files docs
%doc doc/doxygen/html/* doc/asoundrc.txt

