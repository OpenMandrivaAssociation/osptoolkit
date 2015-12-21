%define	major 4
%define libname %mklibname osptk %{major}
%define develname %mklibname osptk -d
%define _disable_lto 1

Summary:	The OSP Toolkit(tm)
Name:		osptoolkit
Version:	4.10.0
Release:	1
License:	BSD-like
Group:		System/Libraries
URL:		http://sourceforge.net/projects/osp-toolkit
Source0:	http://dfn.dl.sourceforge.net/sourceforge/osp-toolkit/OSPToolkit-%{version}.tar.gz
Source1:	Makefile
Patch0:		osptoolkit_3.4.2-1.diff
BuildRequires:	openssl-devel
BuildRequires:	libtool

%description
The OSP Toolkit is a complete development kit for software developers who want
to implement the client side of the European Telecommunication Standards
Institute's (ETSI) Open Settlement Protocol. The OSP Toolkit includes source
code written in ANSI C, test tools and extensive documentation on how to
implement OSP. A hosted OSP test server is freely available on the Internet for
all developers to test their OSP implementation.   

%package -n	%{libname}
Summary:	The OSP Toolkit(tm) shared library
Group:          System/Libraries

%description -n	%{libname}
The OSP Toolkit is a complete development kit for software developers who want
to implement the client side of the European Telecommunication Standards
Institute's (ETSI) Open Settlement Protocol. The OSP Toolkit includes source
code written in ANSI C, test tools and extensive documentation on how to
implement OSP. A hosted OSP test server is freely available on the Internet for
all developers to test their OSP implementation.   

%package -n	%{develname}
Summary:	Static library and header files for the libosp library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	libosp-devel = %{version}
Provides:	osp-devel = %{version}
Provides:	osptk-devel = %{version}
Obsoletes:	%{mklibname osp 0 -d}
Obsoletes:	%{mklibname osptk 0 -d}

%description -n	%{develname}
The OSP Toolkit is a complete development kit for software developers who want
to implement the client side of the European Telecommunication Standards
Institute's (ETSI) Open Settlement Protocol. The OSP Toolkit includes source
code written in ANSI C, test tools and extensive documentation on how to
implement OSP. A hosted OSP test server is freely available on the Internet for
all developers to test their OSP implementation.   

This package contains the static libosp library and its header files.

%package -n	osp-tools
Summary:	Various utilities for the libosptk library
Group:		System/Servers

%description -n	osp-tools
This package contains various utilities utilizing the libosptk library.

%prep

%setup -q -n TK-4_10_0-20151216
%patch0 -p1

install -m0644 %{SOURCE1} Makefile

# lib64 fix
find -name "Makefile" | xargs perl -pi -e "s|/usr/lib|%{_libdir}|g"
find -name "Makefile" | xargs perl -pi -e "s|/lib\b|/%{_lib}|g"

%build

%make CC=%{__cc} build VERSION="%{version}" MAJOR="%{major}" ADDFLAGS="%{optflags}" LDFLAGS="%{ldflags}"
%make CC=%{__cc} enroll VERSION="%{version}" MAJOR="%{major}" ADDFLAGS="%{optflags}" LDFLAGS="%{ldflags}"
%make CC=%{__cc} test VERSION="%{version}" MAJOR="%{major}" ADDFLAGS="%{optflags} -Dtrue=1 -Dfalse=0" LDFLAGS="%{ldflags}"


%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}/pkgconfig
install -d %{buildroot}%{_includedir}/osp

libtool --mode=install install -m0755 lib/libosptk.la %{buildroot}%{_libdir}/libosptk.la
libtool --mode=install install -m0755 bin/test_app %{buildroot}%{_bindir}/osp-test_app
libtool --mode=install install -m0755 bin/enroll %{buildroot}%{_bindir}/osp-enroll

install -m0644 include/osp/*.h %{buildroot}%{_includedir}/osp/
install -m0644 debian/libosptk*.pc %{buildroot}%{_libdir}/pkgconfig/libosptk.pc

rm -f %{buildroot}%{_libdir}/*.*a

%files -n %{libname}
%doc LICENSE.txt README.txt RELNOTES.txt debian/osptoolkit.txt
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%doc test/nonblocking.[ch]
%{_includedir}/osp
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n osp-tools
%doc bin/enroll.sh bin/test.cfg bin/openssl.cnf bin/.rnd
%{_bindir}/osp-test_app
%{_bindir}/osp-enroll


%changelog
* Tue Apr 03 2012 Oden Eriksson <oeriksson@mandriva.com> 4.0.3-1mdv2012.0
+ Revision: 788934
- 4.0.3

* Fri Oct 22 2010 Lonyai Gergely <aleph@mandriva.org> 3.6.1-1mdv2011.0
+ Revision: 587230
- 3.6.1
  The patch is rediffed.

* Fri Apr 16 2010 Funda Wang <fwang@mandriva.org> 3.5.2-2mdv2010.1
+ Revision: 535248
- rebuild

* Mon Aug 31 2009 Oden Eriksson <oeriksson@mandriva.com> 3.5.2-1mdv2010.0
+ Revision: 422856
- 3.5.2

* Wed Jul 09 2008 Oden Eriksson <oeriksson@mandriva.com> 3.4.2-1mdv2009.0
+ Revision: 233094
- 3.4.2

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Fri Oct 20 2006 Oden Eriksson <oeriksson@mandriva.com> 3.3.6-3mdv2007.0
+ Revision: 71326
- fix linkage
- bunzip patches
- fix linkage (pthread)
- Import osptoolkit

* Fri Jun 02 2006 Oden Eriksson <oeriksson@mandriva.com> 3.3.6-2mdv2007.0
- use a working url for the source location

* Thu Mar 23 2006 Oden Eriksson <oeriksson@mandriva.com> 3.3.6-1mdk
- 3.3.6

* Fri Feb 10 2006 Oden Eriksson <oeriksson@mandriva.com> 3.3.4-1mdk
- 3.3.4

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 3.3.3-3mdk
- rebuilt against openssl-0.9.8a

* Thu Nov 03 2005 Oden Eriksson <oeriksson@mandriva.com> 3.3.3-2mdk
- fix compilation (gwenole)
- fix deps due new libname

* Wed Nov 02 2005 Stefan van der Eijk <stefan@eijk.nu> 3.3.3-1mdk
- %%mkrel
- 3.3.3

* Sat Sep 03 2005 Oden Eriksson <oeriksson@mandriva.com> 3.3.1-4mdk
- rebuild
- use sane deps names

* Fri May 06 2005 Oden Eriksson <oeriksson@mandriva.com> 3.3.1-3mdk
- rebuilt with gcc4

* Fri Apr 29 2005 Oden Eriksson <oeriksson@mandriva.com> 3.3.1-2mdk
- fix deps

* Mon Jan 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.3.1-1mdk
- initial Mandrakelinux package

