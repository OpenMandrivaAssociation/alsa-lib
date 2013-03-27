%define major 2

%define oldlib %mklibname alsa %{major}
%define olddev %mklibname -d alsa2

%define libname %mklibname asound %{major}
%define devname %mklibname -d asound

Summary:	Config files for Advanced Linux Sound Architecture (ALSA)
Name:		alsa-lib
Version:	1.0.26
Release:	3
Epoch:		2
Source0:	ftp://ftp.alsa-project.org/pub/lib/%{name}-%{version}.tar.bz2
Source1:	README.soundprofiles
License:	LGPLv2+
Url:		http://www.alsa-project.org/
Group:		Sound
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
#fix build with new automake
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*
autoreconf -fi
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
%{_datadir}/alsa/cards/*
%{_datadir}/alsa/pcm/*
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


%changelog
* Fri Sep 07 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2:1.0.26-1
+ Revision: 816513
- Update to 1.0.26

* Wed Mar 28 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2:1.0.25-8
+ Revision: 787954
- add conflicts to deal with /usr/bin/aserver being moved between packages

* Mon Mar 12 2012 Oden Eriksson <oeriksson@mandriva.com> 2:1.0.25-7
+ Revision: 784425
- fix deps

* Mon Mar 12 2012 Oden Eriksson <oeriksson@mandriva.com> 2:1.0.25-6
+ Revision: 784414
- rebuilt to make sure it ends up in main

* Mon Mar 12 2012 Oden Eriksson <oeriksson@mandriva.com> 2:1.0.25-5
+ Revision: 784397
- rebuild

* Sat Mar 10 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2:1.0.25-4
+ Revision: 783834
- fix incorrect provides/obsoletes of dev package

* Wed Mar 07 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 1.0.25-3
+ Revision: 782632
- use upstream solution for more flexible config without patching
- fix sound on the non-PA profile. (mga)
- own %%{_libdir}/alsa-lib
- move aserver from -devel to main package
- make library packag have a versioned dependency on main package and drop main
  package's versioned dependency on library package
- use %%{EVRD} macro
- rename libalsa2-data to alsa-lib
- rename %%{_lib}alsa2 to %%{_lib}asound2
- don't build static library anymore
- don't ship COPYING file
- fix license
- cleanup package
- drop dead provides/obsoletes
- rename src.rpm to match upstream name

* Mon Feb 20 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 2:1.0.25-2
+ Revision: 778157
- move smixer plugins out of library package (should maybe be packaged
  separately?)

* Sat Jan 28 2012 Bernhard Rosenkraenzer <bero@bero.eu> 2:1.0.25-1
+ Revision: 769537
- Update to 1.0.25
- Build static and shared libraries
  separately (required by 1.0.25)

* Sat Dec 10 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.0.24.1-7
+ Revision: 740065
- delete the static libs, its sub package and the libtool *.la files
- various fixes

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2:1.0.24.1-6
+ Revision: 662345
- mass rebuild

* Tue Mar 08 2011 Funda Wang <fwang@mandriva.org> 2:1.0.24.1-5
+ Revision: 642973
- drop static devel from common devel package

* Tue Mar 08 2011 Funda Wang <fwang@mandriva.org> 2:1.0.24.1-4
+ Revision: 642827
- obsoletes correct devel package

* Tue Mar 08 2011 Funda Wang <fwang@mandriva.org> 2:1.0.24.1-3
+ Revision: 642796
- drop invalid obsoletes

* Tue Mar 08 2011 Funda Wang <fwang@mandriva.org> 2:1.0.24.1-2
+ Revision: 642795
- rebuild
- rebuild

* Mon Mar 07 2011 Matthew Dawkins <mattydaw@mandriva.org> 2:1.0.24.1-1
+ Revision: 642747
- removed unneeded autoreconf
- new version 1.0.24.1
- patches 0100 thru 0109 and 0501 upstreamed
- removed unneeded COPYING doc in every pkg
- dropped major from devel and static pkgs

* Sat Nov 13 2010 Anssi Hannula <anssi@mandriva.org> 2:1.0.23-8mdv2011.0
+ Revision: 597366
- backport fixes from git master
  o fix some minor memleaks
  o present all HDMI outputs on HDA Intel hardware
  o fix namehint skipping certain devices

* Fri Oct 29 2010 Funda Wang <fwang@mandriva.org> 2:1.0.23-7mdv2011.0
+ Revision: 590265
- rebuild for py 2.7

* Sat Oct 16 2010 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.23-6mdv2011.0
+ Revision: 586043
- Revised patch for compensating for TLV min-is-mute flag

* Fri Oct 08 2010 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.23-5mdv2011.0
+ Revision: 584255
- Add a fix for converting to dB then the h/w has a min-is-mute quirk (fixes some PulseAudio issues relating to mute when hitting e.g. 16%%)

* Mon Aug 30 2010 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.23-4mdv2011.0
+ Revision: 574353
- Cherry-pick a typo fix for one of the previous patches.

* Tue Aug 24 2010 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.23-3mdv2011.0
+ Revision: 572590
- Fix race condition related to snd_config_update_free_global() thread safety (mdv#59052, bko#232068, alsa#2124 + many others)

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - ditch *.a & *.la for smixer
    - ditch backwards compatible scriptlets for no longer supported releases
    - ensure clean buildroot at beginning of %%install

* Tue Apr 27 2010 Christophe Fergeau <cfergeau@mandriva.com> 2:1.0.23-2mdv2010.1
+ Revision: 539610
- rebuild so that shared libraries are properly stripped again
- rebuild so that shared libraries are properly stripped again

* Sat Apr 17 2010 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.23-1mdv2010.1
+ Revision: 535802
- New version: 1.0.23
- Drop upstream patches

* Sun Feb 28 2010 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.22-3mdv2010.1
+ Revision: 512815
- Add some patches from master to fix recording and some distortion with S24_3LE samples

* Mon Dec 21 2009 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.22-2mdv2010.1
+ Revision: 480575
- Backport official ALSA patch for the timer close fd leak

* Sun Dec 20 2009 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.22-1mdv2010.1
+ Revision: 480500
- Add upstream/Ubuntu patch to properly closer timers when freeing slaves
- Use standard %%make and remove some no longer needed install code.

  + Thierry Vignaud <tv@mandriva.org>
    - new release

* Wed Sep 09 2009 Thierry Vignaud <tv@mandriva.org> 2:1.0.21a-1mdv2010.0
+ Revision: 435320
- new release

* Mon Aug 31 2009 Thierry Vignaud <tv@mandriva.org> 2:1.0.21-1mdv2010.0
+ Revision: 422989
- new release

* Mon Aug 31 2009 Thierry Vignaud <tv@mandriva.org> 2:1.0.20-3mdv2010.0
+ Revision: 422977
- new release

* Sun Aug 16 2009 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.20-2mdv2010.0
+ Revision: 416921
- Fix copy+paste filelist typo
- Add soundprofile support for pure alsa sound system (i.e. no pulseaudio)

* Mon May 11 2009 Thierry Vignaud <tv@mandriva.org> 2:1.0.20-1mdv2010.0
+ Revision: 374784
- new release

* Fri Feb 20 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2:1.0.19-1mdv2009.1
+ Revision: 343072
- Updated to version 1.0.19
  * dropped alsa-lib-1.0.18-fix-softvol-access-refine.patch (merged)

* Mon Feb 09 2009 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2:1.0.18-4mdv2009.1
+ Revision: 338934
- Added fix to softvol issue from alsa-lib upstream (fixes for example
  speaker-test hang in some cases).

* Fri Dec 26 2008 Funda Wang <fwang@mandriva.org> 2:1.0.18-3mdv2009.1
+ Revision: 319313
- fix str fmt
- rebuild for new python

* Wed Oct 29 2008 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.18-1mdv2009.1
+ Revision: 298678
- Final version: 1.0.18

* Wed Sep 10 2008 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.18-0.rc3.1mdv2009.0
+ Revision: 283540
- New release candidate: 1.0.18rc3

* Sun Aug 24 2008 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.17a-1mdv2009.0
+ Revision: 275468
- Drop upstream patches
- New version 1.0.17a

* Wed Jul 23 2008 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.17-2mdv2009.0
+ Revision: 242055
- Some upstream fixes relating to rewind() calls needed for newer PA

* Wed Jul 16 2008 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.17-1mdv2009.0
+ Revision: 236495
- New version: 1.0.17

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 2:1.0.17-0.rc2.1mdv2009.0
+ Revision: 219551
- new release

* Mon Jun 09 2008 Thierry Vignaud <tv@mandriva.org> 2:1.0.17-0.rc1.1mdv2009.0
+ Revision: 217218
- new release

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Tue Mar 25 2008 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.16-2mdv2008.1
+ Revision: 190086
- Also include the "pulse" device alsa config as it is not loaded automatically.

* Wed Feb 06 2008 Thierry Vignaud <tv@mandriva.org> 2:1.0.16-1mdv2008.1
+ Revision: 163054
- new release

* Tue Jan 29 2008 Thierry Vignaud <tv@mandriva.org> 2:1.0.16-0.rc2.1mdv2008.1
+ Revision: 159893
- new release

* Mon Jan 21 2008 Thierry Vignaud <tv@mandriva.org> 2:1.0.16-0.rc1.1mdv2008.1
+ Revision: 155915
- new release

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 2:1.0.15-6mdv2008.1
+ Revision: 152816
- remove useless kernel require

* Fri Dec 28 2007 Frederic Crozat <fcrozat@mandriva.com> 2:1.0.15-5mdv2008.1
+ Revision: 138870
- Patch2 (HG): fix ioplug period update (Alsa bug #2601)

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Dec 05 2007 Frederic Crozat <fcrozat@mandriva.com> 2:1.0.15-4mdv2008.1
+ Revision: 115677
- Patch1 (Fedora): add hook to /etc/alsa/alsa.conf to auto-enable pulseaudio alsa plugin when its package is installed

* Mon Oct 22 2007 Thierry Vignaud <tv@mandriva.org> 2:1.0.15-3mdv2008.1
+ Revision: 101274
- patch 0: prevents some deadlock when a couple of applications interact and one
  of them closes the device and later re-opens it
- use %%mklibname (cosmetic)

* Wed Oct 17 2007 Thierry Vignaud <tv@mandriva.org> 2:1.0.15-2mdv2008.1
+ Revision: 99660
- suggests the proper plugins depending on the actual arch

* Tue Oct 16 2007 Thierry Vignaud <tv@mandriva.org> 2:1.0.15-1mdv2008.1
+ Revision: 98941
- new release

* Mon Oct 08 2007 Thierry Vignaud <tv@mandriva.org> 2:1.0.15-0.rc3.4mdv2008.1
+ Revision: 95745
- new release

* Wed Sep 19 2007 Thierry Vignaud <tv@mandriva.org> 2:1.0.15-0.rc1.4mdv2008.0
+ Revision: 91110
- patch 3: update PC-Speaker.conf in order to use softvol
- stop overwiting PC-Speaker.conf with an old version

* Mon Sep 17 2007 Thierry Vignaud <tv@mandriva.org> 2:1.0.15-0.rc1.3mdv2008.0
+ Revision: 89357
- the dmix and dsnoop plugins need a fixed substream number instead of the
  next-available one (-1) as the default number
- suggests alsa-plugins

* Mon Sep 03 2007 Thierry Vignaud <tv@mandriva.org> 2:1.0.15-0.rc1.1mdv2008.0
+ Revision: 78500
- new release

* Wed Aug 22 2007 Thierry Vignaud <tv@mandriva.org> 2:1.0.14a-3mdv2008.0
+ Revision: 68982
- patch 0: add a .conf file to enable dmix/dsnoop and softvol for CMI8788, which
  helps mask the bug that all audio is forced to 48 kHz

* Sat Jun 23 2007 Per Øyvind Karlsen <peroyvind@mandriva.org> 2:1.0.14a-2mdv2008.0
+ Revision: 43492
- add PC-Speaker.conf

* Mon Jun 18 2007 Colin Guthrie <cguthrie@mandriva.org> 2:1.0.14a-1mdv2008.0
+ Revision: 40976
- New Release 1.0.14a (our patches have been accepted upstream)
- Fix the loading of ALSA Plugins due to configure.in typo.

  + Thierry Vignaud <tv@mandriva.org>
    - new release
    - fix installing

* Thu May 03 2007 Thierry Vignaud <tv@mandriva.org> 2:1.0.14-2.rc4.3mdv2008.0
+ Revision: 21684
- package new file
- new release

