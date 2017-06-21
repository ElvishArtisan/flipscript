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

identity=''
hostnames=[]
commands=[]

#
# Read the config files
#
for i,file in enumerate(sys.argv):
    if(i>0):
        (identity,hostnames,commands)=Flip_Import(filename=file,identity=identity,hostnames=hostnames,commands=commands)

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

#print('Hostnames:')
#for i in hostnames:
#    print(i)
#print('')

#print('Commands:')
#for i in commands:
#    print(i)
#print('')

#print('Identity:')
#print(identity)
