import sys
import pickle
import config

# Task Clock, Context
# 5000.998244,1,0,0,14496916779,24425419430,4537732291,22866275

# Make a single prediction for a process's POWER consumption
# IN:
#   feats: List of float features: Task Clock, Context-Switches, CPU-migrations, page-faults, cycles, instructions, branches, branch-misses
#       Ex: [5000.998244,1,0,0,14496916779,24425419430,4537732291,22866275]
# OUT:
#   power: Power esitmate in milliwatts for this process 
def powerEstimate(feats):
    try:
        with open(config.MODEL, 'rb') as f:
            model = pickle.load(f)

        # carbonRate = config.getCarbonIntensity()

        feats = [feats]
    
        pred = float(model.predict(feats))

        power = pred - config.BASE_POW
        
        print(power)


    except Exception as ex:
        with open(config.ERROR_DIR + "/model_excep.log", "w") as f:
            f.write(str(ex))



# USAGE: python3 predict.py 5000.998244,1,0,0,14496916779,24425419430,4537732291,22866275
#
#
# Main function: take command line input, split into a list of floats, then predict
# Input is comma separated list of hardware counters in this order: Task Clock, Context-Switches, CPU-migrations, page-faults, cycles, instructions, branches, branch-misses
#


# NOTE: This outputs the POWER estimate in milliwatts (i.e. instantaneous ENERGY)
#       
#       In future, you will want ENERGY in either Joules (i.e. watt*hours) or perhaps milliwatt*hours, milliwatt*seconds, etc.
#       To obtain ENERGY, simlpy multiply the POWER by the time period over which that power was used:
#           
#           Ex: Say a process outputs a POWER of 8000 mw, and that process was running for 5 seconds. The total ENERGY used by that process is:
#               8000 mw * 5 seconds = 40,000 mw*seconds <- ENERGY
#
#           
#
#       To obtain total carbon emissions, obtain a carbon rate (often in (grams of CO2)/kilowatt*hours), and multiply by energy
#       
#       Be mindful of necessary unit conversions! If your ENERGY is in milliwatt*seconds, and carbon rate is in kilowatt*hours you need to convert to kilowatt*hours 
#       (Or vice-versa)
#       I believe the conversion is as follows:
#       
#       1 milliwatt*second = 1/3,600,000 watt*hour = 1/3,600,000,000 kilowatt*hour

if __name__ == "__main__":
    counters = sys.argv[1]
    counters = counters.split(",")
    counters = list(map(float, counters))
    

    power = powerEstimate(counters)

    
