## Makefile.am
##
## (C) Copyright 2017-2025 Fred Gleason <fredg@paravelsystems.com>
##
##   All Rights Reserved.
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License version 2 as
##   published by the Free Software Foundation.
##
##   This program is distributed in the hope that it will be useful,
##   but WITHOUT ANY WARRANTY; without even the implied warranty of
##   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##   GNU General Public License for more details.
##
##   You should have received a copy of the GNU General Public
##   License along with this program; if not, write to the Free Software
##   Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
##
## Use automake to process this into a Makefile.in

if DOCBOOK_AM
  DOCBOOK_OPT = docs
endif

SUBDIRS = helpers \
          $(DOCBOOK_OPT) \
          debian \
          commands \
          expect

deb:	dist
	./build_debs.sh

rpm:	dist
	mkdir -p $(HOME)/rpmbuild/SOURCES
	cp flipscript-$(VERSION).tar.gz $(HOME)/rpmbuild/SOURCES/
	$(RPMBUILD) -ba --target noarch-$(VENDOR)-linux flipscript.spec
	mv $(HOME)/rpmbuild/RPMS/noarch/flipscript-*.rpm $(top_srcdir)/
	mv $(HOME)/rpmbuild/SRPMS/flipscript-*.src.rpm $(top_srcdir)/
	rm $(HOME)/rpmbuild/SOURCES/flipscript-$(VERSION).tar.gz

EXTRA_DIST = build_debs.sh.in\
             get_distro.pl\
             get_target.sh\
             PACKAGE_VERSION

CLEANFILES = *~\
             *.buildinfo\
             *.changes\
             *.deb\
             *.ddeb\
             *.dsc\
             *.rpm\
             *.tar.gz\
             *.tar.xz
DISTCLEANFILES = *.spec\
                 build_debs.sh
MAINTAINERCLEANFILES = *~\
                       aclocal.m4\
                       compile\
                       configure\
                       install-sh\
                       Makefile.in\
                       missing
