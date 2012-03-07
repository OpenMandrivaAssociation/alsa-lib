%define	libname_orig libalsa
%define	major	2
%define	libname	%mklibname alsa %major
%define	devname	%mklibname -d alsa

Summary:	Advanced Linux Sound Architecture (ALSA) library
Name:		alsa-lib
Version:	1.0.25
Release:	3
Source0:	ftp://ftp.alsa-project.org/pub/lib/%{name}-%{version}.tar.bz2
Source1:	README.soundprofiles

# (cg) Mandriva Specific patches
Patch0500:	0500-Add-hooks-to-auto-enable-and-default-to-pulseaudio-w.patch

License:	LGPLv2+
Epoch:		2
Url:		http://www.alsa-project.org/
Group:		Sound
BuildRequires:	doxygen 
BuildRequires:	python-devel

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
Requires:	%{libname_orig}-data
Suggests:	%mklibname alsa-plugins

%description -n	%{libname}
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

Using the ALSA api requires to use the ALSA library.

%package -n	%{libname_orig}-data
Summary:	Config files for Advanced Linux Sound Architecture (ALSA)
Group:		Sound
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Requires(post):	update-alternatives
Requires(postun):update-alternatives

%description -n %{libname_orig}-data
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
Requires:	%{libname} >= %{epoch}:%{version}-%{release}
Provides:	%{libname_orig}-devel = %{version}-%{release}

%description -n	%{devname}
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

This package contains files needed in order to develop an application
that made use of ALSA.

%package	docs
Summary:	Documentation for Advanced Linux Sound Architecture (ALSA)
Group:		Books/Howtos
Requires:	%{libname} >= %{epoch}:%{version}-%{release}

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

This package contains the documentation that describe tha ALSA lib API.

%prep
%setup -q
%apply_patches

%build
mkdir shared
cd shared
CONFIGURE_TOP=..
%configure2_5x --enable-shared --enable-python
# Force definition of -DPIC so that VERSIONED_SYMBOLS are used
# FIXME: alsa people should not depend on PIC to determine a DSO build...
perl -pi -e 's,(^pic_flag=.+)(-fPIC),\1-DPIC \2,' libtool
%make
%make -C doc doc
cd ..
mkdir static
cd static
%configure2_5x --disable-shared --enable-static --enable-python
# Force definition of -DPIC so that VERSIONED_SYMBOLS are used
# FIXME: alsa people should not depend on PIC to determine a DSO build...
perl -pi -e 's,(^pic_flag=.+)(-fPIC),\1-DPIC \2,' libtool
%make
cd ..

%install
%makeinstall_std -C static
%makeinstall_std -C shared

# (cg) For sound profile support
mkdir -p %{buildroot}%{_sysconfdir}/sound/profiles/alsa
echo "SOUNDPROFILE=alsa" >%{buildroot}%{_sysconfdir}/sound/profiles/alsa/profile.conf
install -m 644 %{SOURCE1} -D%{buildroot}%{_sysconfdir}/sound/profiles/README

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a
rm -f %{buildroot}%{_libdir}/alsa-lib/smixer/*.*a

%define alt_name soundprofile
%define alt_priority 10

%post -n %{libname_orig}-data
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/sound/profiles/current %{alt_name} %{_sysconfdir}/sound/profiles/alsa %{alt_priority}

%postun -n %{libname_orig}-data
if [ ! -f %{_sysconfdir}/sound/profiles/alsa/profile.conf ]; then
  /usr/sbin/update-alternatives --remove %{alt_name} %{_sysconfdir}/sound/profiles/alsa
fi

%files -n %{libname_orig}-data
%dir %{_sysconfdir}/sound/profiles
%dir %{_sysconfdir}/sound/profiles/alsa
%{_sysconfdir}/sound/profiles/README
%{_sysconfdir}/sound/profiles/alsa/profile.conf
%dir %{_datadir}/alsa/
%dir %{_datadir}/alsa/cards/
%dir %{_datadir}/alsa/pcm/
%{_datadir}/alsa/cards/*
%{_datadir}/alsa/pcm/*
%{_datadir}/alsa/alsa.conf
%{_datadir}/alsa/alsa.conf.d
%{_datadir}/alsa/smixer.conf
%{_datadir}/alsa/sndo-mixer.alisp
%dir %{_libdir}/alsa-lib/smixer/
%{_libdir}/alsa-lib/smixer/*

%files -n %{libname}
%doc COPYING
%{_libdir}/libasound.so.%{major}*

%files docs
%doc COPYING shared/doc/doxygen/html/* doc/asoundrc.txt

%files -n %{devname}
%dir %{_includedir}/alsa/
%{_includedir}/alsa/*
%{_includedir}/sys/asoundlib.h
%{_datadir}/aclocal/alsa.m4
%{_libdir}/libasound.so
%{_libdir}/pkgconfig/alsa.pc
%{_bindir}/*
