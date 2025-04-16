## Makefile.am
##
## Makefile.am for flipscripts commands/
##
##   (C) Copyright 2025 Fred Gleason <fredg@paravelsystems.com>
##
##   This program is free software; you can redistribute it and/or modify
##   it under the terms of the GNU General Public License as
##   published by the Free Software Foundation; either version 2 of
##   the License, or (at your option) any later version.
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

install-exec-am:
	mkdir -p $(DESTDIR)@prefix@/bin
	cp flip.py $(DESTDIR)@prefix@/bin/flip
	cp mscp.py $(DESTDIR)@prefix@/bin/mscp

uninstall-local:
	rm $(DESTDIR)@prefix@/bin/flip
	rm $(DESTDIR)@prefix@/bin/mscp

EXTRA_DIST = flip.py\
             mscp.py

CLEANFILES = *~
