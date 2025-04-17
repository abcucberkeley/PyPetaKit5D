import os
import subprocess


def XR_crop_dataset(dataPaths, inputBbox, **kwargs):
    function_name = "XR_crop_dataset"
    XR_crop_dataset_dict = {
        "resultDirName": [kwargs.get("resultDirName", "Cropped"), "char"],
        "cropType": [kwargs.get("cropType", "fixed"), "char"],
        "pad": [kwargs.get("pad", False), "logical"],
        "lastStartCoords": [kwargs.get("lastStartCoords", []), "numericArr"],
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA_ch0','CamB_ch0']), "cell"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "largeFile": [kwargs.get("largeFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "batchSize": [kwargs.get("batchSize", [1024,1024,1024]), "numericArr"],
        "blockSize": [kwargs.get("blockSize", [256,256,256]), "numericArr"],
        "save16bit": [kwargs.get("save16bit", True), "logical"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 2), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "configFile": [kwargs.get("configFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    inputBboxString = "[" + ",".join(str(item) for item in inputBbox) + "]"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" \"{inputBboxString}\" "
    
    for key, value in XR_crop_dataset_dict.items():
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
    