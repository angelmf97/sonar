----
# Sonar
 
Sonar is a Python based script used to find, within any given set of proteins, the subset of secreted RCPs, i.e. those proteins contaning both internal repeats and secretion signal. It makes use of the programmes RADAR and SignalP 4.1. The results of the analyses can be visualized in an Excel table if the user wants so.

----
## Usage  
  
Please, execute  
```
sonar.py -h  
```
or  
```
sonar.py --help  
```
for usage instructions.  
  
Simplest use case:  
```
sonar.py -f example.fasta  
```
An example file can be found in this repository.
  
The commands available are the following ones:  

| Command       | Function                         |
|---------------|----------------------------------|
| -h, --help    | show this help message and exit. |
| -f , --file   | input file.                      |
| -t,--table | prints two tables containing the results of RADAR (RCPs only) and SignalP 4.1 (secreted RCPs). |
| -r, --radar   | prints the output of RADAR.      |
| -s,--signalp | prints the output of SignalP 4.1 |
| -o , --output | destination directory of the tables and the list of proteins found.           |

## Requisites
  * Python 2.
  * Having RADAR installed (https://github.com/AndreasHeger/radar).
  * Having SignalP 4.0 installed.
  * Having the package XlsxWriter installed (https://pypi.org/project/XlsxWriter/).
