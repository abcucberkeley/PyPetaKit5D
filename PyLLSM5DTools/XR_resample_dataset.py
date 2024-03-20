import os
import subprocess


def XR_resample_dataset(dataPath, resultPath, rsfactor, **kwargs):
    function_name = "XR_resample_dataset"
    XR_resample_dataset_dict = {
        "Interp": [kwargs.get("Interp", "linear"), "char"],
        "Save16bit": [kwargs.get("Save16bit", True), "logical"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 2), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "ConfigFile": [kwargs.get("ConfigFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/LLSM5DTools/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2023a"
    dataPathString = "{" + ",".join(f"'{item}'" for item in dataPath) + "}"
    resultPathString = "{" + ",".join(f"'{item}'" for item in resultPath) + "}"
    rsfactorString = "[" + ",".join(str(item) for item in rsfactor) + "]"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPath}\" \"{resultPath}\" \"{rsfactorString}\" "
    
    for key, value in XR_resample_dataset_dict.items():
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
    