# CONFIG FILE FOR POWER MODEL

MODEL = "./model.pkl"           # File path to saved model

BASE_POW = 100000               # Average "Base Power" in milliwatts of the system at idle (subtracted from predictions to isolate per process power)

ERROR_DIR = "./"                # Directory path to error output

# Replace the body, arguments of this function with your own logic to get the carbon intensity
# TODO: I'll get you a sample implementation
def getCarbonIntensity():
    return 0