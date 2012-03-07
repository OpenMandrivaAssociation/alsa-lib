%define lib_name_orig libalsa
%define major 2
%define lib_name %mklibname alsa %major
%define develname %mklibname -d alsa
#define beta 0
%define fname alsa-lib-%{version}%{?beta}

Summary:	Advanced Linux Sound Architecture (ALSA) library
Name:		libalsa2
Version:	1.0.25
Release:	%{?beta:0.%{beta}.}2
Source0:	ftp://ftp.alsa-project.org/pub/lib/%{fname}.tar.bz2
Source1:	README.soundprofiles

# (cg) Mandriva Specific patches
Patch0500: 0500-Add-hooks-to-auto-enable-and-default-to-pulseaudio-w.patch

License:	GPL
Epoch:		2
Url:		http://www.alsa-project.org/
Group:		Sound
Provides:	alsa-lib, %lib_name_orig = %version
Obsoletes:	alsa-lib, %lib_name_orig
Suggests: %mklibname alsa-plugins
#Obsoletes: libalsa1
#Provides: libalsa1
BuildRequires:	doxygen 
BuildRequires:	python-devel
Requires:	%{lib_name_orig}-data

%description
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

Using the ALSA api requires to use the ALSA library.

%if "%{_lib}" != "lib"
%package -n %{lib_name}
Summary:	Advanced Linux Sound Architecture (ALSA) library
Group:		Sound
Provides:	alsa-lib, %lib_name_orig = %version
Obsoletes:	alsa-lib, %lib_name_orig
Requires:	%{lib_name_orig}-data

%description -n %{lib_name}
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

Using the ALSA api requires to use the ALSA library.
%endif

%define alt_name soundprofile
%define alt_priority 10

%package -n %{lib_name_orig}-data
Summary:    Config files for Advanced Linux Sound Architecture (ALSA)
Group:      Sound
Requires:   %lib_name >= %epoch:%version-%release
Requires(post): update-alternatives
Requires(postun): update-alternatives

%description -n %{lib_name_orig}-data
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

This package contains config files by ALSA applications.

%post -n %{lib_name_orig}-data
%{_sbindir}/update-alternatives \
  --install %{_sysconfdir}/sound/profiles/current %{alt_name} %{_sysconfdir}/sound/profiles/alsa %{alt_priority}

%postun -n %{lib_name_orig}-data
if [ ! -f %{_sysconfdir}/sound/profiles/alsa/profile.conf ]; then
  /usr/sbin/update-alternatives --remove %{alt_name} %{_sysconfdir}/sound/profiles/alsa
fi


%package -n %{develname}
Summary:    Development files for Advanced Linux Sound Architecture (ALSA)
Group:      Development/C
Requires:   %lib_name >= %epoch:%version-%release
Provides:   libalsa1-devel alsa-lib-devel, %lib_name_orig-devel = %version-%release
Obsoletes:  libalsa1-devel alsa-lib-devel
Obsoletes:  %{mklibname alsa2 -d}

%description -n %{develname}
Advanced Linux Sound Architecture (ALSA) is a modularized architecture which
supports quite a large range of ISA and PCI cards.
It's fully compatible with old OSS drivers (either OSS/Lite, OSS/commercial).
To use the features of alsa, one can either use:
- the old OSS api
- the new ALSA api that provides many enhanced features.

This package contains files needed in order to develop an application
that made use of ALSA.

%package docs
Summary:    Documentation for Advanced Linux Sound Architecture (ALSA)
Group:      Books/Howtos
Requires:   %lib_name >= %epoch:%version-%release

%description docs
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
%setup -q -n %fname
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
rm -rf %{buildroot}
cd static
%makeinstall_std
cd ../shared
%makeinstall_std
mv doc/doxygen ../doc

# (cg) For sound profile support
mkdir -p %{buildroot}%{_sysconfdir}/sound/profiles/alsa
echo "SOUNDPROFILE=alsa" >%{buildroot}%{_sysconfdir}/sound/profiles/alsa/profile.conf
install -m 644 %SOURCE1 \
                   %{buildroot}%{_sysconfdir}/sound/profiles/README

# cleanup
rm -f %{buildroot}%{_libdir}/*.*a
rm -f %{buildroot}%{_libdir}/alsa-lib/smixer/*.*a

%files -n %{lib_name_orig}-data
%dir %{_sysconfdir}/sound/profiles
%dir %{_sysconfdir}/sound/profiles/alsa
%{_sysconfdir}/sound/profiles/README
%{_sysconfdir}/sound/profiles/alsa/profile.conf
%dir %_datadir/alsa/
%dir %_datadir/alsa/cards/
%dir %_datadir/alsa/pcm/
%_datadir/alsa/cards/*
%_datadir/alsa/pcm/*
%_datadir/alsa/alsa.conf
%_datadir/alsa/alsa.conf.d
%_datadir/alsa/smixer.conf
%_datadir/alsa/sndo-mixer.alisp
%dir %_libdir/alsa-lib/smixer/
%_libdir/alsa-lib/smixer/*

%files -n %{lib_name}
%doc COPYING
%_libdir/*.so.%{major}*

%files docs
%doc COPYING doc/doxygen/html/* doc/asoundrc.txt

%files -n %{develname}
%dir %_includedir/alsa/
%_includedir/alsa/*
%_includedir/sys/asoundlib.h
%_datadir/aclocal/alsa.m4
%_libdir/*.so
%_libdir/pkgconfig/*.pc
%_bindir/*
