
# SONAR
----  
SONAR is a Python based programme used to find, within any given set of proteins, the subset of them containing both repeated sequences and signal sequences. It makes use of the software RADAR and SignalP 4.0.

## Usage
----  
Please, execute  
    *sonar.py -h*  
or  
    *sonar.py -help*  
for usage instructions.  
Use case:  
    *sonar.py (yourfile).fasta (commands) > (Destiny file)*  
The commands available are the following ones:  
    *-r or -R 	prints RADAR's output. Prints a table containing the information of the repeats found in the different genes.*  
    *-t or -T	displays RADAR's output in a table format.*  
    *-p or -P	prints a list of all the proteins containing repeats (only names).*  
    *-s or -S	prints the output of SignalP.*  

