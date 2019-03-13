# sonar

This programme is used to find, within any given set of proteins, the subset of them containing both repeated sequences and signal sequences.
# Usage

Please, execute
	sonar.py -h
or
	sonar.py -help
for usage instructions.
The simplest use case is:
	sonar.py (yourfile).fasta (commands) > (Destiny file)
The arguments given must be the following ones:'
    print 'python parseradarv4.py (commands) (> DestinationFile)\n'
The commands available are the following ones:
	-r or -R Prints RADAR's output. Prints a table containing the information of the repeats found in the different genes.
	-t or -T	displays RADAR's output in a table format.
	-p or -P	prints a list of all the proteins containing repeats (only names).
	-s or -S	prints the output of SignalP.

