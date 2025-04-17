import os
import subprocess


def XR_tiffToZarr_wrapper(dataPaths, **kwargs):
    function_name = "XR_tiffToZarr_wrapper"
    XR_tiffToZarr_wrapper_dict = {
        "tiffFullpaths": [kwargs.get("tiffFullpaths", ""), "cell"],
        "resultDirName": [kwargs.get("resultDirName", "zarr"), "char"],
        "locIds": [kwargs.get("locIds", []), "numericScalar"],
        "blockSize": [kwargs.get("blockSize", [256,256,256]), "numericArr"],
        "shardSize": [kwargs.get("shardSize", []), "numericArr"],
        "flippedTile": [kwargs.get("flippedTile", []), "logical"],
        "resampleFactor": [kwargs.get("resampleFactor", []), "numericArr"],
        "partialFile": [kwargs.get("partialFile", False), "logical"],
        "channelPatterns": [kwargs.get("channelPatterns", ['tif']), "cell"],
        "inputBbox": [kwargs.get("inputBbox", []), "numericArr"],
        "tileOutBbox": [kwargs.get("tileOutBbox", []), "numericArr"],
        "readWholeTiff": [kwargs.get("readWholeTiff", True), "logical"],
        "processFunPath": [kwargs.get("processFunPath", ""), "cell"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "bigData": [kwargs.get("bigData", True), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 1), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "maxTrialNum": [kwargs.get("maxTrialNum", 3), "numericScalar"],
        "unitWaitTime": [kwargs.get("unitWaitTime", 3), "numericScalar"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "configFile": [kwargs.get("configFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_tiffToZarr_wrapper_dict.items():
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
    