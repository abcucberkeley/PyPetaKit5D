import os
import subprocess


def XR_chromatic_shift_correction_data_wrapper(dataPaths, **kwargs):
    function_name = "XR_chromatic_shift_correction_data_wrapper"
    XR_chromatic_shift_correction_data_wrapper_dict = {
        "chromaticOffset": [kwargs.get("chromaticOffset", []), "numericArr"],
        "resultDirName": [kwargs.get("resultDirName", "Chromatic_Shift_Corrected"), "char"],
        "mode": [kwargs.get("mode", "valid"), "char"],
        "padValue": [kwargs.get("padValue", 0), "numericScalar"],
        "newOrigin": [kwargs.get("newOrigin", []), "numericScalar"],
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA','CamB']), "cell"],
        "psfFullpaths": [kwargs.get("psfFullpaths", []), "cell"],
        "maxOffset": [kwargs.get("maxOffset", [20,20,20]), "numericArr"],
        "cropLength": [kwargs.get("cropLength", [0,0,0]), "numericArr"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "largeFile": [kwargs.get("largeFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "batchSize": [kwargs.get("batchSize", [1024,1024,1024]), "numericArr"],
        "blockSize": [kwargs.get("blockSize", [256,256,256]), "numericArr"],
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
    
    for key, value in XR_chromatic_shift_correction_data_wrapper_dict.items():
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
            separator = ","
            if key == "chromaticOffset":
                separator = ";"
            numericArrString = "[" + separator.join(str(item) for item in value[0]) + "]"
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
    