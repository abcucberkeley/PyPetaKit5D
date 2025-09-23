import os
import subprocess


def XR_unmix_channels_data_wrapper(dataPaths, **kwargs):
    function_name = "XR_unmix_channels_data_wrapper"
    XR_unmix_channels_data_wrapper_dict = {
        "unmixFactors": [kwargs.get("unmixFactors", []), "numericArr"],
        "mode": [kwargs.get("mode", "linear"), "char"],
        "unmixSigmas": [kwargs.get("unmixSigmas", []), "numericArr"],
        "resultDirName": [kwargs.get("resultDirName", "Unmixed"), "char"],
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA','CamB']), "cell"],
        "channelInd": [kwargs.get("channelInd", 1), "numericScalar"],
        "FFCorrection": [kwargs.get("FFCorrection", False), "logical"],
        "lowerLimit": [kwargs.get("lowerLimit", 0.4), "numericScalar"],
        "FFImagePaths": [kwargs.get("FFImagePaths", ['','']), "cell"],
        "backgroundPaths": [kwargs.get("backgroundPaths", ['','']), "cell"],
        "constBackground": [kwargs.get("constBackground", []), "numericScalar"],
        "constOffset": [kwargs.get("constOffset", []), "numericScalar"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "largeFile": [kwargs.get("largeFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "save16bit": [kwargs.get("save16bit", True), "logical"],
        "batchSize": [kwargs.get("batchSize", [1024,1024,1024]), "numericArr"],
        "blockSize": [kwargs.get("blockSize", [256,256,256]), "numericArr"],
        "borderSize": [kwargs.get("borderSize", [0,0,0]), "numericArr"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 3), "numericScalar"],
        "configFile": [kwargs.get("configFile", ""), "char"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "debug": [kwargs.get("debug", False), "logical"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_unmix_channels_data_wrapper_dict.items():
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
            if type(value[0]) is not list:
                value[0] = [value[0]]
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
    