import os
import subprocess


def XR_imaris_conversion_data_wrapper(dataPaths, **kwargs):
    function_name = "XR_imaris_conversion_data_wrapper"
    XR_imaris_conversion_data_wrapper_dict = {
        "resultDirName": [kwargs.get("resultDirName", "imaris"), "char"],
        "overwrite": [kwargs.get("overwrite", False), "logical"],
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0']), "cell"],
        "pixelSizes": [kwargs.get("pixelSizes", [0.108,0.108,0.108]), "numericArr"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "blockSize": [kwargs.get("blockSize", [64,64,64]), "numericArr"],
        "inputBbox": [kwargs.get("inputBbox", []), "numericArr"],
        "converterPath": [kwargs.get("converterPath", f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/microscopeDataProcessing/tools/Imaris/Parallel_Imaris_Writer/linux/parallelimariswriter"), "char"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 24), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "configFile": [kwargs.get("configFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_imaris_conversion_data_wrapper_dict.items():
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
    