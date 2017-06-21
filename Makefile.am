## Makefile.am
##
## (C) Copyright 2017 Fred Gleason <fredg@paravelsystems.com>
##
##   All Rights Reserved.
##
## Use automake to process this into a Makefile.in

install-exec-local:	
	mkdir -p $(DESTDIR)/etc/flipscript.d
	mkdir -p $(DESTDIR)/usr/lib/flipscripts

bin_SCRIPTS = flip.py

rpm:	dist
	mkdir -p $(HOME)/rpmbuild/SOURCES
	cp flipscript-$(VERSION).tar.gz $(HOME)/rpmbuild/SOURCES/
	$(RPMBUILD) -ba --target noarch-$(VENDOR)-linux flipscript.spec
	mv $(HOME)/rpmbuild/RPMS/noarch/flipscript-*.rpm $(top_srcdir)/
	mv $(HOME)/rpmbuild/SRPMS/flipscript-*.src.rpm $(top_srcdir)/
	rm $(HOME)/rpmbuild/SOURCES/flipscript-$(VERSION).tar.gz

EXTRA_DIST = flip.py\
             get_distro.pl\
             get_target.sh\
             PACKAGE_VERSION

CLEANFILES = *~\
             *.rpm\
             *.tar.gz
DISTCLEANFILES = *.spec
MAINTAINERCLEANFILES = *~\
                       aclocal.m4\
                       configure\
                       install-sh\
                       Makefile.in\
                       missing
