----
# Sonar
 
Sonar is a Python based script used to find, within any given set of proteins, the subset of secreted RCPs, i.e. those proteins contaning both internal repeats and secretion signal. It makes use of the programmes RADAR and SignalP 4.0.  

----
## Usage  
  
Please, execute  

 * `sonar.py -h`  
 
or  
 * `sonar.py --help`  
 
for usage instructions.  
  
Simplest use case:  

 * `sonar.py -f example.fasta`  

An example file can be found in this repository.
  
The commands available are the following ones:  

| Command       | Function                         |
|---------------|----------------------------------|
| -h, --help    | show this help message and exit. |
| -f , --file   | input file.                      |
| -r, --radar   | prints the output of RADAR.      |
| -o , --output | destination directory.           |


