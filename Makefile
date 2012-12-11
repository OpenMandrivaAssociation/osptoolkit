#
# OSP Toolkit Makefile for Debian
#

# Default install directory
INSTALL_PATH = $(DESTDIR)/usr
CONFIG_PATH = $(DESTDIR)/etc
PC_PATH = $(DESTDIR)/usr/lib/pkgconfig

# Compile tools
CC = gcc
D2M = docbook-to-man

# Compile flags
DEFFLAGS = -DOSP_ALLOW_DUP_TXN -DOSP_NO_DELETE_CHECK -DOSP_SDK -D_REENTRANT \
	   -D_POSIX_THREADS -DOPENSSL_NO_KRB5 -D_GNU_SOURCE
INCFLAGS = -I$(INCDIR) -I$(ENRDIR) -I$(EXPDIR)
# DEBFLAGS = -DOSPC_DEBUG=1
GFLAGS = -g -Wall
CFLAGS = $(DEFFLAGS) $(INCFLAGS) $(DEBFLAGS) $(GFLAGS) $(ADDFLAGS)
colon = :
period = .
LTFLAGS = -rpath /usr/lib -version-number $(subst $(period),$(colon),$(VERSION))
LDFLAGS =

# General libries
GENLIBS = -lm -lpthread

# SSL library selection for OpenSSL
SSL_OBJS = ospopenssl
SSLLIBS = -lssl -lcrypto

# OSP Toolkit directories
INCDIR = include
LIBDIR = lib
SRCDIR = src
ENRDIR = enroll
EXPDIR = test
BINDIR = bin
DEBDIR = debian

# OSP Toolkit objects & library
OSP_OBJS = osppkcs1 osppkcs8 osppkcs7 ospcryptowrap ospasn1ids ospasn1object \
	   ospx509 ospasn1 ospasn1primitives ospasn1parse ospcrypto osptnlog \
	   ospsecssl  ospsecurity osplist osphttp ospxml ospmime ospprovider \
           ospproviderapi ospsocket ospcomm osputils ospmsgque ospmsginfo \
	   osptransapi osptrans ospinit ospmsgelem ospdest ospusage ospmsgattr \
	   ospcallid osptoken ospmsgutil ospmsgdesc ospostime ospxmltype \
	   ospxmlparse ospxmlattr ospxmlutil ospxmlenc ospxmlelem ospusageind \
           ospstatus ospauthreq ospauthrsp ospauthind ospauthcnf ospreauthreq \
	   ospreauthrsp ospusagecnf ospb64 ospbfr osptokeninfo  ospfail \
	   ospaltinfo ospssl  ospstatistics osptnprobe ospaudit osptnaudit \
	   osptransids ospciscoext ospcapind ospcapcnf \
           $(SSL_OBJS)
OSPOBJS = $(addprefix $(SRCDIR)/,$(addsuffix .lo,$(OSP_OBJS)))
OSP_LIB = libosptk
OSPLIB = $(addprefix $(LIBDIR)/,$(addsuffix .la,$(OSP_LIB)))
OSPLIBLT = $(addsuffix .la,$(OSP_LIB))
OSPSTATIC = $(addsuffix .a,$(OSP_LIB))
OSPSHARED = $(addsuffix .so.$(VERSION),$(OSP_LIB))
OSPSLINK = $(addsuffix .so.$(MAJOR),$(OSP_LIB))
OSPSLIB = $(addsuffix .so,$(OSP_LIB))
OSP_DOC = osptoolkit.txt
OSPDOC = $(DEBDIR)/$(OSP_DOC)
OSP_PC = $(OSP_LIB)$(MAJOR).pc
OSPPC = $(DEBDIR)/$(OSP_PC)

# OSP Toolkit enroll application
ENR_OBJS = osptnepinit osptnepenroll osptnep osptneputil
ENROBJS = $(addprefix $(ENRDIR)/,$(addsuffix .o,$(ENR_OBJS)))
ENR_EXEC = enroll
ENREXEC = $(BINDIR)/$(ENR_EXEC)
ENR_WRAP = enroll.sh
ENRWRAP = $(BINDIR)/$(ENR_WRAP)
ENR_CONF = openssl.cnf
ENRCONF = $(BINDIR)/$(ENR_CONF)
ENR_SGML = ospenroll.sgml
ENRSGML = $(DEBDIR)/$(ENR_SGML)
ENR_MAN = ospenroll.1
ENRMAN = $(DEBDIR)/$(ENR_MAN)

# OSP Toolkit test application
EXP_OBJS = nonblocking syncque test_app
EXPOBJS = $(addprefix $(EXPDIR)/,$(addsuffix .o,$(EXP_OBJS)))
EXP_EXEC = test_app
EXPEXEC = $(BINDIR)/$(EXP_EXEC)
EXP_CONF = test.cfg
EXPCONF = $(BINDIR)/$(EXP_CONF)
EXP_SGML = osptest.sgml
EXPSGML = $(DEBDIR)/$(EXP_SGML)
EXP_MAN = osptest.1
EXPMAN = $(DEBDIR)/$(EXP_MAN)

.SUFFIXES: .lo .c 

.c.o:
	$(CC) $(CFLAGS) -o $(@) -c $(<)

.c.lo:
	libtool --mode=compile $(CC) $(CFLAGS) -o $(@) -c $(<)

build: $(OSPLIB) $(OSPPC)
$(OSPLIB): $(OSPOBJS)
	libtool --mode=link $(CC) $(GFLAGS) $(ADDFLAGS) -o $(@) $(^) \
		$(LTFLAGS) $(LDFLAGS) $(SSLLIBS) $(GENLIBS)
$(OSPPC): Makefile
	@ echo 'Building $(OSPPC) ...'
	@ ( echo 'prefix=$(INSTALL_PATH)'; \
	echo 'exec_prefix=$${prefix}'; \
	echo 'libdir=$${exec_prefix}/lib'; \
	echo 'includedir=$${prefix}/include'; \
	echo ''; \
	echo 'Name: OSPToolkit'; \
	echo 'Description: OSP shared library'; \
	echo 'Version: '$(VERSION); \
	echo 'Requires: '; \
	echo 'Libs: -L$${libdir} -losptk'; \
	echo 'Libs.private: $(SSLLIBS) $(GENLIBS)'; \
	echo 'Cflags: -I$${includedir} -I$${includedir}/osp' ) > $(OSPPC)

enroll: $(ENREXEC)
$(ENREXEC): $(ENROBJS) $(OSPLIB)
	libtool --mode=link $(CC) $(GFLAGS) $(ADDFLAGS) $(LDFLAGS) -o $(@) $(^)

test: $(EXPEXEC)
$(EXPEXEC): $(EXPOBJS) $(OSPLIB)
	libtool --mode=link $(CC) $(GFLAGS) $(ADDFLAGS) $(LDFLAGS) -o $(@) $(^)

manpages: $(ENRMAN) $(EXPMAN)
$(ENRMAN): $(ENRSGML)
	$(D2M) $(<) > $(@)
$(EXPMAN): $(EXPSGML)
	$(D2M) $(<) > $(@)

install-lib: build
	libtool --mode=install cp $(OSPLIB) $(INSTALL_PATH)/lib/
	rm -f $(INSTALL_PATH)/lib/$(OSPLIBLT)
	rm -f $(INSTALL_PATH)/lib/$(OSPSTATIC)
	rm -f $(INSTALL_PATH)/lib/$(OSPSLIB)

install-dev: build
	cp $(INCDIR)/osp/* $(INSTALL_PATH)/include/osp
	libtool --mode=install cp $(OSPLIB) $(INSTALL_PATH)/lib/
	rm -f $(INSTALL_PATH)/lib/$(OSPSHARED)
	rm -f $(INSTALL_PATH)/lib/$(OSPSLINK)
	cp $(OSPPC) $(PC_PATH)
	chmod 644 $(PC_PATH)/$(OSP_PC)

install-bin: enroll test manpages
	libtool --mode=install cp $(ENREXEC) $(INSTALL_PATH)/lib/osp/
	cp $(ENRWRAP) $(INSTALL_PATH)/lib/osp/
	cp $(ENRCONF) $(CONFIG_PATH)/osp/
	cp $(ENRMAN) $(INSTALL_PATH)/share/man/man1/
	libtool --mode=install cp $(EXPEXEC) $(INSTALL_PATH)/lib/osp/
	cp $(EXPCONF) $(CONFIG_PATH)/osp/
	cp $(EXPMAN) $(INSTALL_PATH)/share/man/man1/
	cp $(OSPDOC) $(INSTALL_PATH)/share/doc/osptoolkit/

clean:
	libtool --mode=clean rm -f $(OSPLIB) $(OSPOBJS)
	libtool --mode=clean rm -f $(ENREXEC) $(ENROBJS)
	libtool --mode=clean rm -f $(EXPEXEC) $(EXPOBJS)
	rm -f $(ENRMAN) $(EXPMAN) $(OSPPC)

