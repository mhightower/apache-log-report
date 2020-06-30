# Apache Combined Plus Log Report

This application produces a report based on a single Apache log file.

## How to use?

`python3 apache_log_process.py <apache_log>`

Ex: `python3 apache_log_process.py /var/log/apache/apache.log`

Tested using Python 3.6.9

### Exit code

0 Successful  
66 Usage  
66 No Input  
69 Python version unavailable  

Tested on Windows wsl Ubuntu 18.04.4 LTS so exit codes may differ.


## Output example

Number of lines parsed: 43378    
Duration of log file: 0.59375    

Most requested page: /kms/my/home/    
Most frequent visitor: 37.17.24.145    

Min page load time: 538    
Average page load time: 2503.3449213887225    
Max page load time: 4580    

Number of errors: 4406    
Total data transferred: 216857012    

### Notes on output

* Duration of log file is in seconds.
* page load time is in microseconds.
* Total data transferred is in bytes.

## Code style

PEP8
