import os
import subprocess


def XR_psf_detection_and_analysis_wrapper(dataPaths, **kwargs):
    function_name = "XR_psf_detection_and_analysis_wrapper"
    XR_psf_detection_and_analysis_wrapper_dict = {
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "dz": [kwargs.get("dz", 0.1), "numericScalar"],
        "angle": [kwargs.get("angle", 32.45), "numericScalar"],
        "cropSize": [kwargs.get("cropSize", [256,128,201]), "numericArr"],
        "flipZstack": [kwargs.get("flipZstack", False), "logical"],
        "distThresh": [kwargs.get("distThresh", [256,128,201]), "numericArr"],
        "ChannelPatterns": [kwargs.get("ChannelPatterns", ['CamA_ch0','CamB_ch0']), "cell"],
        "Channels": [kwargs.get("Channels", [488,560]), "numericArr"],
        "RWFn": [kwargs.get("RWFn", ['/clusterfs/fiona/Gokul/RW_PSFs/PSF_RW_515em_128_128_101_100nmSteps.tif','/clusterfs/fiona/Gokul/RW_PSFs/PSF_RW_605em_128_128_101_100nmSteps.tif']), "cell"],
        "sourceStr": [kwargs.get("sourceStr", "test"), "char"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", False), "logical"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "ConfigFile": [kwargs.get("ConfigFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/LLSM5DTools/mcc/linux_with_jvm/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2023a"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_psf_detection_and_analysis_wrapper_dict.items():
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
    