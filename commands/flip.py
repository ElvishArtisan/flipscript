#!/usr/bin/python3

# flip.py
#
#    (C) Copyright 2017-2025 Fred Gleason <fredg@paravelsystems.com>
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

import getpass
import glob
import subprocess
import sys

def eprint(*args,**kwargs):
    print(*args,file=sys.stderr,**kwargs)


def TrimWhitelines(string):
    ret=''
    lines=string.split('\n')
    for i in range(len(lines)):
        if((i!=0)and(i!=(len(lines)-1))):
            ret+=lines[i]+'\n'
        else:
            if(len(lines[i])!=0):
                ret+=lines[i]+'\n'
    return ret


def Flip_Import(filename,identity,username,hostnames,commands):
    with open(filename) as f:
        lines=f.readlines()
        lines=[x.strip() for x in lines]
        for line in lines:
            f0=line.split("=")
            values="=".join(f0[1:])
            if(f0[0].lower()=="hostname"):
                hostnames.append(values)
            if(f0[0].lower()=="command"):
                commands.append(values)
            if(f0[0].lower()=="identity"):
                identity=values
            if(f0[0].lower()=="username"):
                username=values
    return (identity,username,hostnames,commands)


def MakeExpect(spawn_cmd,redact,hostname,passphrase):
    f=open('/usr/lib/flipscript/flip.exp','r')
    expect=f.read()
    f.close()

    expect=expect.replace('@HOSTNAME@',hostname)
    expect=expect.replace('@SPAWN_COMMAND@',spawn_cmd)
    if(redact):
        expect=expect.replace('@PASSPHRASE@','<REDACTED>')
    else:
        expect=expect.replace('@PASSPHRASE@',passphrase+'\\n')
    return expect

#
# Check command-line options
#
dump=False
dry_run=False
dump_expect=False
label=False
for arg in sys.argv:
    if(arg=='--list'):
        files=sorted(glob.glob('/var/lib/flipscripts/*.flip'))
        for file in files:
            f1=file.split('/')
            print(f1[-1])
        sys.exit(0)
    if(arg=='--dry-run'):
        dry_run=True
    if(arg=='--dump'):
        dump=True
    if(arg=='--dump-expect'):
        dump_expect=True
    if(arg=='--label'):
        label=True

username=''
identity=''
hostnames=[]
commands=[]

#
# Read the config files
#
initfiles=glob.glob('/etc/flipscript.d/*.flip')
for file in initfiles:
    (identity,username,hostnames,commands)=Flip_Import(filename=file,identity=identity,username=username,hostnames=hostnames,commands=commands)

#
# Read the files from the command-line
#
for i,file in enumerate(sys.argv):
    if(i>0):
        if(file[0:10]=='--command='):
            f0=file.split("=")
            values="=".join(f0[1:])
            commands.append(values)
        if(file[0:11]=='--hostname='):
            f0=file.split("=")
            values="=".join(f0[1:])
            hostnames.append(values)
        if(file[0:11]=='--identity='):
            f0=file.split("=")
            values="=".join(f0[1:])
            identity=values
        if(file[0:11]=='--username='):
            f0=file.split("=")
            values="=".join(f0[1:])
            username=values
        if(file[0:2]!='--'):
            if(file[-5:]!='.flip'):
                file+='.flip'
                try:
                    if(file.find('/')==0):
                        (identity,username,hostnames,commands)=Flip_Import(filename=file,identity=identity,username=username,hostnames=hostnames,commands=commands)
                    else:
                        (identity,username,hostnames,commands)=Flip_Import(filename='/var/lib/flipscripts/'+file,identity=identity,username=username,hostnames=hostnames,commands=commands)
                except IOError:
                    eprint('flip: unable to open file "'+file+'"')
                    sys.exit(256)

if(dump):
    print()
    if(len(identity)>0):
        print('identity='+identity)
    if(len(username)>0):
        print('username='+username)
    for hostname in hostnames:
        print('hostname='+hostname)
    for command in commands:
        print('command='+command)
    print()
    sys.exit(0)

#
# Get the passphrase
#
if(len(identity)>0):
    passphrase=getpass.getpass(prompt="Enter passphrase for key '"+identity+"':")
else:
    passphrase=getpass.getpass(prompt="Enter passphrase for default key:")

#
# Run the commands
#
userarg=''
if(username!=''):
    userarg=username+'@'

for hostname in hostnames:
    for command in commands:
        if(identity==''):
            spawn_cmd='ssh '+userarg+hostname+' '+command
        else:
            spawn_cmd='ssh -i '+identity+' '+userarg+hostname+' '+command
        if(dry_run):
            print(spawn_cmd)
        else:
            expect=MakeExpect(spawn_cmd=spawn_cmd,passphrase=passphrase,hostname=hostname,redact=dump_expect)
            if(dump_expect):
                print('*** EXPECT SCRIPT FOR %s STARTS ***' % hostname)
                print(expect,end='')
                print('**** EXPECT SCRIPT FOR %s ENDS ****' % hostname)
            else:
                if(label):
                    print('*** FROM %s STARTS **********************************' % hostname)
                p=subprocess.run(['expect','-'],input=expect,encoding='utf-8',capture_output=True)
                if(p.returncode==0):
                    print(TrimWhitelines(p.stdout),end='')
                else:
                    eprint('expect(1) returned error: '+p.stderr)
                if(label):
                    print('*** FROM %s ENDS ************************************' % hostname)


