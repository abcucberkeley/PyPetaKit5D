import os
import subprocess


def XR_fftSpectrumComputingWrapper(dataPaths, **kwargs):
    function_name = "XR_fftSpectrumComputingWrapper"
    XR_fftSpectrumComputingWrapper_dict = {
        "Overwrite": [kwargs.get("Overwrite", False), "logical"],
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "dz": [kwargs.get("dz", 0.1), "numericScalar"],
        "outPixelSize": [kwargs.get("outPixelSize", []), "numericScalar"],
        "N": [kwargs.get("N", [1001,1001,1001]), "numericArr"],
        "ChannelPatterns": [kwargs.get("ChannelPatterns", []), "cell"],
        "save3DStack": [kwargs.get("save3DStack", False), "logical"],
        "background": [kwargs.get("background", 0), "numericScalar"],
        "Interp": [kwargs.get("Interp", "linear"), "char"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "ConfigFile": [kwargs.get("ConfigFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/LLSM5DTools/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2023a"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_fftSpectrumComputingWrapper_dict.items():
        if value[1] == "char":
            if not value[0]:
                continue
            cmdString += f"\"{key}\" \"{value[0]}\" "
        elif value[1] == "cell":
            if not value[0]:
                continue
            cellString = "{" + ",".join(f"'{item}'" for item in value[0]) + "}"
            cmdString += f"\"{key}\" \"{cellString}\" "
        elif value[1] == "logicalArr":
            logicalArrString = "[" + ",".join(str(item) for item in value[0]) + "]"
            cmdString += f"\"{key}\" \"{str(logicalArrString).lower()}\" "
        elif value[1] == "logical":
            cmdString += f"\"{key}\" {str(value[0]).lower()} "
        elif value[1] == "numericArr":
            if not value[0]:
                continue
            numericArrString = "[" + ",".join(str(item) for item in value[0]) + "]"
            cmdString += f"\"{key}\" \"{numericArrString}\" "
        elif value[1] == "numericScalar":
            if type(value[0]) is list:
                if not value[0]:
                    continue
                else:
                    value[0] = value[0][0]
            cmdString += f"\"{key}\" {value[0]} "
        else:
            continue
    process = subprocess.Popen(cmdString, shell=True)
    process.wait()
    