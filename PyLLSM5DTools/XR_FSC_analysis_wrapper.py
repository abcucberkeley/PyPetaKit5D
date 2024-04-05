import math
import os
import subprocess


def XR_FSC_analysis_wrapper(dataPaths, **kwargs):
    function_name = "XR_FSC_analysis_wrapper"
    XR_FSC_analysis_wrapper_dict = {
        "outDirstr": [kwargs.get("outDirstr", "FSCs"), "char"],
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "dz": [kwargs.get("dz", 0.1), "numericScalar"],
        "dr": [kwargs.get("dr", 1), "numericScalar"],
        "dtheta": [kwargs.get("dtheta", math.pi/12), "numericScalar"],
        "resThreshMethod": [kwargs.get("resThreshMethod", "fixed"), "char"],
        "resThresh": [kwargs.get("resThresh", 0.2), "numericScalar"],
        "N": [kwargs.get("N", [251,251,251]), "numericArr"],
        "bbox": [kwargs.get("bbox", []), "numericScalar"],
        "resAxis": [kwargs.get("resAxis", "xz"), "char"],
        "skipConeRegion": [kwargs.get("skipConeRegion", True), "logical"],
        "ChannelPatterns": [kwargs.get("ChannelPatterns", ['tif']), "cell"],
        "Channels": [kwargs.get("Channels", [488,560]), "numericArr"],
        "multiRegions": [kwargs.get("multiRegions", False), "logical"],
        "regionInterval": [kwargs.get("regionInterval", [50,50,-1]), "numericArr"],
        "regionGrid": [kwargs.get("regionGrid", []), "numericScalar"],
        "clipPer": [kwargs.get("clipPer", []), "numericScalar"],
        "suffix": [kwargs.get("suffix", "decon"), "char"],
        "iterInterval": [kwargs.get("iterInterval", 5), "numericScalar"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "ConfigFile": [kwargs.get("ConfigFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/LLSM5DTools/mcc/linux_with_jvm/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2023a"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_FSC_analysis_wrapper_dict.items():
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
    