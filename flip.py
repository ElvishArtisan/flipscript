#!/usr/bin/python

# flip.py
#
#    (C) Copyright 2017 Fred Gleason <fredg@paravelsystems.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of version 2 of the GNU General Public License as
#    published by the Free Software Foundation;
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, 
#    Boston, MA  02111-1307  USA
#

from __future__ import print_function

import glob
import subprocess
import sys

def eprint(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)

def Flip_Import(filename,identity,hostnames,commands):
    with open(filename) as f:
        lines=f.readlines()
        lines=[x.strip() for x in lines]
        for line in lines:
            tag,value=line.split("=")
            if(tag.lower()=="hostname"):
                hostnames.append(value)
            if(tag.lower()=="command"):
                commands.append(value)
            if(tag.lower()=="identity"):
                identity=value
    return (identity,hostnames,commands)

#
# Check command-line options
#
for arg in sys.argv:
    if(arg=='--list'):
        files=glob.glob('/usr/lib/flipscripts/*.flip')
        for file in files:
            f1=file.split('/')
            print(f1[-1])
        sys.exit(0)

identity=''
hostnames=[]
commands=[]

#
# Read the config files
#
initfiles=glob.glob('/etc/flipscript.d/*.flip')
for file in initfiles:
    (identity,hostnames,commands)=Flip_Import(filename=file,identity=identity,hostnames=hostnames,commands=commands)

#
# Read the files from the command-line
#
for i,file in enumerate(sys.argv):
    if(i>0):
        if(file[-5:]!='.flip'):
            file+='.flip'
        try:
            if(file.find('/')==0):
                (identity,hostnames,commands)=Flip_Import(filename=file,identity=identity,hostnames=hostnames,commands=commands)
            else:
                (identity,hostnames,commands)=Flip_Import(filename='/usr/lib/flipscripts/'+file,identity=identity,hostnames=hostnames,commands=commands)
        except IOError:
            eprint('flip.py: unable to open file "'+file+'"')
            sys.exit(256)
#
# Run the commands
#
identarg=''
if(identity!=''):
    identarg='-i '+identity

for hostname in hostnames:
    for command in commands:
        proc=subprocess.Popen(('ssh','-i',identity,'root@'+hostname,command),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (output,errs)=proc.communicate()
        if(errs!=''):
            eprint('HOST:"'+hostname+'" COMMAND:"'+command+'" ERROR:"'+errs+'"')
