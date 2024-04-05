import os
import subprocess


def XR_deskew_rotate_data_wrapper(dataPaths, **kwargs):
    function_name = "XR_deskew_rotate_data_wrapper"
    XR_deskew_rotate_data_wrapper_dict = {
        "DSDirStr": [kwargs.get("DSDirStr", "DS/"), "char"],
        "DSRDirStr": [kwargs.get("DSRDirStr", "DSR/"), "char"],
        "Deskew": [kwargs.get("Deskew", True), "logical"],
        "Rotate": [kwargs.get("Rotate", True), "logical"],
        "Overwrite": [kwargs.get("Overwrite", False), "logical"],
        "ChannelPatterns": [kwargs.get("ChannelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0','CamB_ch1']), "cell"],
        "dz": [kwargs.get("dz", 0.5), "numericScalar"],
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "SkewAngle": [kwargs.get("SkewAngle", 32.45), "numericScalar"],
        "ObjectiveScan": [kwargs.get("ObjectiveScan", False), "logical"],
        "ZstageScan": [kwargs.get("ZstageScan", False), "logical"],
        "Reverse": [kwargs.get("Reverse", False), "logical"],
        "flipZstack": [kwargs.get("flipZstack", False), "logical"],
        "parseSettingFile": [kwargs.get("parseSettingFile", False), "logical"],
        "Crop": [kwargs.get("Crop", False), "logical"],
        "DSRCombined": [kwargs.get("DSRCombined", True), "logical"],
        "LLFFCorrection": [kwargs.get("LLFFCorrection", False), "logical"],
        "BKRemoval": [kwargs.get("BKRemoval", False), "logical"],
        "LowerLimit": [kwargs.get("LowerLimit", 0.4), "numericScalar"],
        "constOffset": [kwargs.get("constOffset", []), "numericScalar"],
        "LSImagePaths": [kwargs.get("LSImagePaths", ['','','']), "cell"],
        "BackgroundPaths": [kwargs.get("BackgroundPaths", ['','','']), "cell"],
        "Save16bit": [kwargs.get("Save16bit", False), "logical"],
        "save3DStack": [kwargs.get("save3DStack", True), "logical"],
        "SaveMIP": [kwargs.get("SaveMIP", True), "logical"],
        "largeFile": [kwargs.get("largeFile", False), "logical"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "BatchSize": [kwargs.get("BatchSize", [1024,1024,1024]), "numericArr"],
        "BlockSize": [kwargs.get("BlockSize", [256,256,256]), "numericArr"],
        "zarrSubSize": [kwargs.get("zarrSubSize", [20,20,20]), "numericArr"],
        "inputBbox": [kwargs.get("inputBbox", []), "numericArr"],
        "taskSize": [kwargs.get("taskSize", []), "numericScalar"],
        "resample": [kwargs.get("resample", []), "numericArr"],
        "Interp": [kwargs.get("Interp", "linear"), "char"],
        "maskFns": [kwargs.get("maskFns", []), "cell"],
        "suffix": [kwargs.get("suffix", ""), "char"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "parseParfor": [kwargs.get("parseParfor", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 1), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "debug": [kwargs.get("debug", False), "logical"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "ConfigFile": [kwargs.get("ConfigFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/LLSM5DTools/mcc/linux/run_mccMaster.sh"
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
    