# POWER MODEL ESITMATE

## Setup/Dependencies:
Requires Scikit-Learn, a Python library for Machine Learning models

If on a UNIX like system, you can run `source py-venv-setup.sh` to create a python virtual environment and install scikit learn.

On future runs, make sure the venv is activated before invoking the script with something like: `source /path/to/power_model/env/bin/activate`

If the setup script fails, make sure python3-venv is installed. On Ubuntu: `apt-get install python3-venv`

If the venv fails to activate, try appending .zsh, .fish, or .csh to the "activate" in the `source` commands (different script types for different shell implementations)


## Usage:

`python3 predict.py 5000.998244,1,0,0,14496916779,24425419430,4537732291,22866275`

Input is comma separated list of hardware counters in this order: Task Clock, Context-Switches, CPU-migrations, page-faults, cycles, instructions, branches, branch-misses


## Outputs:

POWER estimate in milliwatts. See my NOTE in the predict.py file about the distinction between POWER and ENERGY, and conversions etc.
