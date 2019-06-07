#!/usr/bin/python

import re
import subprocess
import os
from tempfile import NamedTemporaryFile
import argparse
import xlsxwriter


parser=argparse.ArgumentParser(description='Sonar is a Python based script used to find, within any given set of proteins, the subset of them containing both repeated sequences and signal sequences, also known as secreted RCPs (repeat-containing proteins). It makes use of the programmes RADAR and SignalP 4.0.')
parser.add_argument('-f','--file',metavar='',type=argparse.FileType(),required=True,help='input file.')
parser.add_argument('-t','--table',action='store_true',required=False,help='prints two tables containing the information of RADAR (RCPs only) and SignalP-4.1 (secreted RCPs).')
parser.add_argument('-r','--radar',action='store_true',required=False,help='prints the output of RADAR.')
parser.add_argument('-s','--signalp',action='store_true',required=False,help='prints the output of SignalP 4.1.')
parser.add_argument('-o','--output',type=str,metavar='',required=False,default='.',help='destination directory.')

args=parser.parse_args()


#Takes a .fasta file and gives it to RADAR protein by protein. Then returns the RADAR's output.
def callradar():
    proteins_with_repeats=[]
    file=args.file.read().split('>')
    list_of_proteins=[]
    flag=0
    
    for n in file:
        if flag==0:
            flag=1
        else:
            protein='>'+n
            list_of_proteins.append(protein)

    radar_list=[]

    for n in list_of_proteins:
        radartemp=NamedTemporaryFile()
        radartemp.write(n)
        radartemp.read()

        try:
            command='radar.py %s' % radartemp.name
            radar_output=subprocess.check_output(command.split(' '), shell=False)
            re_search=re.search('No repeats found',radar_output)

            if re_search:
                continue

            else:
                proteins_with_repeats.append(n)
                radar_list.append(radar_output)

        except Exception as inst:
            print inst
            search='>.+\n'.search(n)
            print 'Error in sequence:' + search.group()
    
    return radar_list,proteins_with_repeats

#Takes the list of proteins containing repeats and passes it to SignalP-4.1
def callsonar(proteins_with_repeats):
    sonartemp=NamedTemporaryFile()
    string=[]
    
    for n in proteins_with_repeats:
        sonartemp.write(n)
    sonartemp.read()
    command='signalp %s' % sonartemp.name
    signalp_output=subprocess.check_output(command.split(' '), shell=False)
    sonarlines=signalp_output.split('\n')
    repeats_and_signal=[]
    re_proteins=re.compile('([^\s]+)\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+Y\s+[^\s]+\s+[^\s]+')
    
    for n in sonarlines:
        p=re_proteins.search(n)
        if p:
            for protein in proteins_with_repeats:
                if p.group(1) in protein:
                    repeats_and_signal.append(protein)
    
    return signalp_output,repeats_and_signal

#Makes the tables    
def maketables(radar_list,signalp_output):
    workbook = xlsxwriter.Workbook(args.output+'/'+os.path.splitext(os.path.basename(args.file.name))[0]+'tables.xlsx')
    sheet=workbook.add_worksheet('RADAR')
    header=['Protein','No. of Repeats','Total Score','Length','Diagonal','BW-From','BW-To','Level']
    col=0

    for i in header:
        sheet.write(0,col,i)
        col+=1

    row=1

    for protein in radar_list:
        col=0
        pname=re.search('(>.+)\n',protein)
        numbers=re.findall('\s+\d+\|\s+\d+\.\d+\|\s+\d+\|\s+\d+\|\s+\d+\|\s+\d+\|\s+\d+',protein)

        for h in numbers:
            col=0
            sheet.write(row,col,pname.group(1))
            col+=1
            splitted=h.split('|')
            for value in splitted:
                cleanvalue=value.strip()
                sheet.write(row,col,cleanvalue)
                col+=1
            row+=1
 
    sheet=workbook.add_worksheet('SignalP-4.1')
    header=['name','Cmax','pos','Ymax','pos','Smax','pos','Smean','D','?','Dmaxcut','Networks-used']
    
    col=0
    for i in header:
        sheet.write(0,col,i)
        col+=1
    sonarlines=re.findall('[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+[^\s]+\s+Y\s+[^\s]+\s+[^\s]+',signalp_output)
    row=1
    
    for line in sonarlines:
        splitted=line.split(' ')
        
        col=0
        for value in splitted:
            cleanvalue=value.strip()
            if cleanvalue!='':
                sheet.write(row,col,cleanvalue)
                col+=1
        row+=1
    
    workbook.close()
    
def main():
    print '\n'
    print 'Please wait, this could take several time.\n'
    radar_list,proteins_with_repeats=callradar()
    signalp_output,repeats_and_signal=callsonar(proteins_with_repeats)
    out=open(args.output+'/'+os.path.splitext(os.path.basename(args.file.name))[0]+'results.fasta','w+')
    
    for protein in repeats_and_signal:
        out.write(protein)
    out.close()
    
    if args.radar:
        for protein in radar_list:
            print protein
    
    if args.signalp:
        print signalp_output

    if args.table:    
        maketables(radar_list,signalp_output)
	print 'Tables stored at %s \n' % out.name
    
    print 'Proteins containing repeats (RCPs) = %s' % len(proteins_with_repeats)
    print 'Secreted RCPs = %s' % len(repeats_and_signal)

if __name__=="__main__":
    main()

