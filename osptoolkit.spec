%define	major 0
%define libname	%mklibname osptk %{major}

Summary:	The OSP Toolkit(tm)
Name:		osptoolkit
Version:	3.3.6
Release:	%mkrel 3
License:	BSD-like
Group:		System/Libraries
URL:		http://www.transnexus.com/
Source0:	http://www.transnexus.com/OSP%20Toolkit/Toolkits%20for%20Download/OSPToolkit-%{version}.tar.bz2
Patch0:		TK-3_3_1-20041213_B-asterisk.diff
Patch1:		TK-3_3_3-20051103_B-shared.diff
BuildRequires:	openssl-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
The OSP Toolkit is a complete development kit for software
developers who want to implement the client side of the European
Telecommunication Standards Institute's (ETSI) Open Settlement
Protocol.  The OSP Toolkit includes source code written in ANSI C,
test tools and extensive documentation on how to implement OSP. 
A hosted OSP test server is freely available on the Internet for
all developers to test their OSP implementation.   

%package -n	%{libname}
Summary:	The OSP Toolkit(tm) shared library
Group:          System/Libraries
Obsoletes:	%{mklibname osp 0}

%description -n	%{libname}
The OSP Toolkit is a complete development kit for software
developers who want to implement the client side of the European
Telecommunication Standards Institute's (ETSI) Open Settlement
Protocol.  The OSP Toolkit includes source code written in ANSI C,
test tools and extensive documentation on how to implement OSP. 
A hosted OSP test server is freely available on the Internet for
all developers to test their OSP implementation.   

%package -n	%{libname}-devel
Summary:	Static library and header files for the libosp library
Group:		Development/C
Obsoletes:	libosp-devel osp-devel osptk-devel
Provides:	libosp-devel = %{version}
Provides:	osp-devel = %{version}
Provides:	osptk-devel = %{version}
Requires:	%{libname} = %{version}
Obsoletes:	%{mklibname osp 0}-devel

%description -n	%{libname}-devel
The OSP Toolkit is a complete development kit for software
developers who want to implement the client side of the European
Telecommunication Standards Institute's (ETSI) Open Settlement
Protocol.  The OSP Toolkit includes source code written in ANSI C,
test tools and extensive documentation on how to implement OSP. 
A hosted OSP test server is freely available on the Internet for
all developers to test their OSP implementation.   

This package contains the static libosp library and its header
files.

%package -n	osp-tools
Summary:	Various utilities for the libosp library
Group:		System/Servers

%description -n	osp-tools
The OSP Toolkit is a complete development kit for software
developers who want to implement the client side of the European
Telecommunication Standards Institute's (ETSI) Open Settlement
Protocol.  The OSP Toolkit includes source code written in ANSI C,
test tools and extensive documentation on how to implement OSP. 
A hosted OSP test server is freely available on the Internet for
all developers to test their OSP implementation.   

This package contains various utilities utilizing the libosp
library.

%prep

%setup -q -n TK-3_3_6-20060303
%patch0 -p0 -b .asterisk
%patch1 -p1 -b .shared

# lib64 fix
find -name "Makefile" | xargs perl -pi -e "s|/usr/lib|%{_libdir}|g"

%build

%make RPM_OPT_FLAGS="%{optflags} -pthread" -C src
%make RPM_OPT_FLAGS="%{optflags} -pthread" -C enroll
%make RPM_OPT_FLAGS="%{optflags} -pthread" -C test

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_includedir}/osp

install -m0755 src/libosptk.so.%{major} %{buildroot}%{_libdir}/
ln -s libosptk.so.%{major} %{buildroot}%{_libdir}/libosptk.so

install -m0644 src/libosptk.a %{buildroot}%{_libdir}/
install -m0644 include/osp/*.h %{buildroot}%{_includedir}/osp/

install -m0755 test/test_app %{buildroot}%{_bindir}/osp-test_app
install -m0755 enroll/enroll %{buildroot}%{_bindir}/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc LICENSE.txt README.txt RELNOTES.txt
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%doc LICENSE.txt README.txt RELNOTES.txt
%doc test/nonblocking.[ch]
%{_includedir}/osp
%{_libdir}/*.so
%{_libdir}/*.a

%files -n osp-tools
%defattr(-,root,root)
%doc LICENSE.txt README.txt RELNOTES.txt
%doc bin/enroll.sh bin/test.cfg bin/openssl.cnf bin/.rnd
%{_bindir}/osp-test_app
%{_bindir}/enroll


