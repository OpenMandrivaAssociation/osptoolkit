%define	major 4
%define libname %mklibname osptk %{major}
%define develname %mklibname osptk -d

Summary:	The OSP Toolkit(tm)
Name:		osptoolkit
Version:	4.0.3
Release:	%mkrel 1
License:	BSD-like
Group:		System/Libraries
URL:		http://sourceforge.net/projects/osp-toolkit
Source0:	http://dfn.dl.sourceforge.net/sourceforge/osp-toolkit/OSPToolkit-%{version}.tar.gz
Source1:	Makefile
Patch0:		osptoolkit_3.4.2-1.diff
BuildRequires:	openssl-devel
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%setup -q -n TK-4_0_3-20120120
%patch0 -p1

install -m0644 %{SOURCE1} Makefile

# lib64 fix
find -name "Makefile" | xargs perl -pi -e "s|/usr/lib|%{_libdir}|g"
find -name "Makefile" | xargs perl -pi -e "s|/lib\b|/%{_lib}|g"

%build

%make build VERSION="%{version}" MAJOR="%{major}" ADDFLAGS="%{optflags}" LDFLAGS="%{ldflags}"
%make enroll VERSION="%{version}" MAJOR="%{major}" ADDFLAGS="%{optflags}" LDFLAGS="%{ldflags}"
%make test VERSION="%{version}" MAJOR="%{major}" ADDFLAGS="%{optflags}" LDFLAGS="%{ldflags}"

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}/pkgconfig
install -d %{buildroot}%{_includedir}/osp

libtool --mode=install install -m0755 lib/libosptk.la %{buildroot}%{_libdir}/libosptk.la
libtool --mode=install install -m0755 bin/test_app %{buildroot}%{_bindir}/osp-test_app
libtool --mode=install install -m0755 bin/enroll %{buildroot}%{_bindir}/osp-enroll

install -m0644 include/osp/*.h %{buildroot}%{_includedir}/osp/
install -m0644 debian/libosptk*.pc %{buildroot}%{_libdir}/pkgconfig/libosptk.pc

rm -f %{buildroot}%{_libdir}/*.*a

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc LICENSE.txt README.txt RELNOTES.txt debian/osptoolkit.txt
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc test/nonblocking.[ch]
%{_includedir}/osp
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n osp-tools
%defattr(-,root,root)
%doc bin/enroll.sh bin/test.cfg bin/openssl.cnf bin/.rnd
%{_bindir}/osp-test_app
%{_bindir}/osp-enroll
