Setup/ Dependencies:

Python version: python 3.7
Operating System: Unix based
Processor: Intel processors (not ARM because of non availability of hardware counters used as features for running regression model)
Library: Scikit-Learn (for Linear Regression model)
Installation required for perf:

	>> sudo apt-get install linux-tools-common linux-tools-generic linux-tools-`uname -r`

	uname -r (type this on terminal) gives the kernel release. For example 3.2.0.43 

	To check if perf  installation was successful type the following on terminal
	>> perf record /bin/ls

Input:

Requires root privilege since perf-stat is running in the background and it requires root privileges.

pid (process id is optional) and sleep time (in seconds) for perf-stat to load hardware counter data for every process running on the system.

Below is an example to run the power model for 5s sleep time which displays the calculated power on screen after every 6.2 seconds as well as saves the data to an output file.

>>python3  power.py 5 [predict]

The following command is to obtain the last logged power consumption of a process (right before the c_top command was executed) while the previous script runs in the background.

>>c_top {$process_id}

c_top command is an alias to run >> python3 reverse_read.py {$process_id} 

Output:

The output is calculated power consumption which is used to calculate the carbon intensity for every process.
