import os
import subprocess


def XR_deskew_rotate_data_wrapper(dataPaths, **kwargs):
    function_name = "XR_deskew_rotate_data_wrapper"
    XR_deskew_rotate_data_wrapper_dict = {
        "DSDirName": [kwargs.get("DSDirName", "DS"), "char"],
        "DSRDirName": [kwargs.get("DSRDirName", "DSR"), "char"],
        "deskew": [kwargs.get("deskew", True), "logical"],
        "rotate": [kwargs.get("rotate", True), "logical"],
        "overwrite": [kwargs.get("overwrite", False), "logical"],
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0','CamB_ch1']), "cell"],
        "dz": [kwargs.get("dz", 0.5), "numericScalar"],
        "xyPixelSize": [kwargs.get("xyPixelSize", [0.108]), "numericArr"],
        "skewAngle": [kwargs.get("skewAngle", 32.45), "numericScalar"],
        "objectiveScan": [kwargs.get("objectiveScan", False), "logical"],
        "zStageScan": [kwargs.get("zStageScan", False), "logical"],
        "reverse": [kwargs.get("reverse", False), "logical"],
        "flipZstack": [kwargs.get("flipZstack", False), "logical"],
        "parseSettingFile": [kwargs.get("parseSettingFile", False), "logical"],
        "crop": [kwargs.get("crop", False), "logical"],
        "inputAxisOrder": [kwargs.get("inputAxisOrder", "yxz"), "char"],
        "outputAxisOrder": [kwargs.get("outputAxisOrder", "yxz"), "char"],
        "DSRCombined": [kwargs.get("DSRCombined", True), "logical"],
        "FFCorrection": [kwargs.get("FFCorrection", False), "logical"],
        "BKRemoval": [kwargs.get("BKRemoval", False), "logical"],
        "lowerLimit": [kwargs.get("lowerLimit", 0.4), "numericScalar"],
        "constOffset": [kwargs.get("constOffset", []), "numericScalar"],
        "FFImagePaths": [kwargs.get("FFImagePaths", ['','','']), "cell"],
        "backgroundPaths": [kwargs.get("backgroundPaths", ['','','']), "cell"],
        "save16bit": [kwargs.get("save16bit", True), "logical"],
        "save3DStack": [kwargs.get("save3DStack", True), "logical"],
        "saveMIP": [kwargs.get("saveMIP", True), "logical"],
        "largeFile": [kwargs.get("largeFile", False), "logical"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "batchSize": [kwargs.get("batchSize", [1024,1024,1024]), "numericArr"],
        "blockSize": [kwargs.get("blockSize", [256,256,256]), "numericArr"],
        "inputBbox": [kwargs.get("inputBbox", []), "numericArr"],
        "taskSize": [kwargs.get("taskSize", []), "numericScalar"],
        "resampleFactor": [kwargs.get("resampleFactor", []), "numericArr"],
        "interpMethod": [kwargs.get("interpMethod", "linear"), "char"],
        "maskFullpaths": [kwargs.get("maskFullpaths", []), "cell"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "parseParfor": [kwargs.get("parseParfor", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 1), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "debug": [kwargs.get("debug", False), "logical"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "configFile": [kwargs.get("configFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2023a"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_deskew_rotate_data_wrapper_dict.items():
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
    