#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 16:02:33 2018

@author: angel
"""

# -*- coding: utf-8 -*-
#!/usr/bin/env python3

from sys import argv
import re
import subprocess
import os
from tempfile import NamedTemporaryFile

"""Help"""
if ('-h' or '-help' or '--h' or '--help' or 'help') in argv:
    print '\nThe arguments given must be the following ones:'
    print 'python parseradarv4.py (commands) (> DestinationFile)\n'
    print 'The commands available are the following ones:\n'
    print '-r or -R\tprints RADAR output.\n-t\tprints a table containing the',
    print 'information of the repeats found in the\n\tdifferent genes.'
    print '-t or -T\tdisplays RADAR\'s output in a table format.'
    print '-p or -P\tprints a list of all the proteins containing repeats (only names).'
    print '-s or -S\tprints the output of SignalP.\n'
    quit()

"""Functions"""

#Takes a .fasta file and gives it to RADAR. Then returns the RADAR's output.
def call_radar(fasta):
    command='radar.py %s' % fasta
    radar_output=subprocess.check_output(command.split(' '), shell=False)
    return radar_output

#Converts the output of radar to a string and then splits it by proteins
def split_by_proteins(radar_output):
    string=[]
    for i in radar_output:
        string.append(i)
    file=''.join(string)
    file_by_protein=re.split('\n(?=>)',file)
    return file_by_protein

#Takes a sorted-by-protein radar output and makes a table
def print_table(file_by_protein):
    re_header=re.compile('No.*Level')
    re_protein=re.compile('(>.+)')
    re_others=re.compile('\s+\d+\|\s+\d+\.\d+\|\s+\d+\|\s+\d+\|\s+\d+\|\s+\d+\|\s+\d+')
    for i in file_by_protein:
        print '\n'*2
        flag=0
        line=i.split('\n')
        for n in range(len(line)):
            p=re_protein.search(line[n])
            h=re_header.search(line[n])
            s=re_others.search(line[n])
            if p:
                #Prints protein names
                print p.group(),'\n'
            if h:
                #Prints header
                if flag==0:
                    print '|',h.group(),'|'
                    print '-'*75
                    flag=1
            if s:
                #Prints values
                print '|',s.group(),'|'
            if line[n]=='No repeats found':
                print 'No repeats found'

#Takes a sorted-by-gene radar output and returns a list with all the proteins containing repeats
def capture_proteins(file_by_protein):
    proteins_with_repeats=[]
    re_protein=re.compile('(>jgi\|.+)')
    for i in file_by_protein:
        p=re_protein.search(i)
        line=i.split('\n')
        if line[1]=='No repeats found':
            continue
        else:
            proteins_with_repeats.append(p.group())
    return proteins_with_repeats

#Takes a list of all the proteins containing repeats. Then gets those proteins sequence
#back from the original .fasta file and submits the sequences to SignalP.
#Returns SignalP output
def call_signalp(proteins_with_repeats,file_input):
    temp=NamedTemporaryFile(dir='/home/angel/program')
    string=[]
    for i in open(file_input):
        string.append(i)
    file=''.join(string)
    input_by_protein=re.split('\n(?=>)',file)
    for n in input_by_protein:
        for i in proteins_with_repeats:
            if i in n:
                temp.write('\n%s\n' % n)
    temp.read()
    command='signalp %s' % temp.name
    signalp_output=subprocess.check_output(command.split(' '), shell=False)
    return signalp_output

#Takes the SignalP output and returns a list of proteins containing both repeats
#and signal sequences
def get_repeat_signal(signalp_output):
    lines=signalp_output.split('\n')
    list=[]
    re_proteins=re.compile('([^\s]+)\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+Y\s+[^\s]+\s+[^\s]+')
    for n in lines:
        p=re_proteins.search(n)
        if p:
            list.append('>'+p.group(1))
    return list

"""def create_fasta(list):
    file=open(argv[1]).read()
    fasta=open(str(argv[1])+'_result.fasta','w+')
    for n in list:
        re_proteins=re.compile(n)
        p=re_proteins.finditer(file)
        if p:
            print p.group(0)
    file.close()
    fasta.close()"""



"""Program"""

file_input=argv[1]
radar_output=call_radar(file_input)
if ('-r' or '-R') in argv:
    print radar_output,'\n'*2

file_by_proteins=split_by_proteins(radar_output)

if ('-t' or '-T') in argv:
    print_table(file_by_proteins)
    print '\n'*2

proteins_with_repeats=capture_proteins(file_by_proteins)

if ('-p' or '-P') in argv:
    print 'Proteins containing repeats: %s' % len(proteins_with_repeats), '\n'
    for n in proteins_with_repeats:
        print n
    print '\n'*2

signalp_output=call_signalp(proteins_with_repeats,file_input)

if ('-s' or '-S') in argv:
    print signalp_output
    print '\n'*2

repeats_and_signal=get_repeat_signal(signalp_output)
print 'Proteins containing both repeats and signal sequences: %s' % len(repeats_and_signal),'\n'
for n in repeats_and_signal:
    print n

"""if '-f' in argv:
    create_fasta(repeats_and_signal)"""

quit()
