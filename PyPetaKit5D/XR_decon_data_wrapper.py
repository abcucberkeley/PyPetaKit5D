import os
import subprocess


def XR_decon_data_wrapper(dataPaths, **kwargs):
    function_name = "XR_decon_data_wrapper"
    XR_decon_data_wrapper_dict = {
        "resultDirName": [kwargs.get("resultDirName", "matlab_decon"), "char"],
        "overwrite": [kwargs.get("overwrite", False), "logical"],
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0']), "cell"],
        "skewAngle": [kwargs.get("skewAngle", 32.45), "numericScalar"],
        "dz": [kwargs.get("dz", 0.5), "numericScalar"],
        "xyPixelSize": [kwargs.get("xyPixelSize", [0.108]), "numericArr"],
        "save16bit": [kwargs.get("save16bit", True), "logical"],
        "parseSettingFile": [kwargs.get("parseSettingFile", False), "logical"],
        "flipZstack": [kwargs.get("flipZstack", False), "logical"],
        "background": [kwargs.get("background", []), "numericScalar"],
        "dzPSF": [kwargs.get("dzPSF", 0.1), "numericScalar"],
        "edgeErosion": [kwargs.get("edgeErosion", 0), "numericScalar"],
        "erodeByFTP": [kwargs.get("erodeByFTP", True), "logical"],
        "psfFullpaths": [kwargs.get("psfFullpaths", ['','','']), "cell"],
        "deconIter": [kwargs.get("deconIter", 15), "numericScalar"],
        "RLMethod": [kwargs.get("RLMethod", "simplified"), "char"],
        "wienerAlpha": [kwargs.get("wienerAlpha", 0.005), "numericScalar"],
        "OTFCumThresh": [kwargs.get("OTFCumThresh", 0.9), "numericScalar"],
        "hannWinBounds": [kwargs.get("hannWinBounds", [0.8,1.0]), "numericArr"],
        "skewed": [kwargs.get("skewed", []), "logical"],
        "debug": [kwargs.get("debug", False), "logical"],
        "saveStep": [kwargs.get("saveStep", 5), "numericScalar"],
        "psfGen": [kwargs.get("psfGen", True), "logical"],
        "GPUJob": [kwargs.get("GPUJob", False), "logical"],
        "deconRotate": [kwargs.get("deconRotate", False), "logical"],
        "batchSize": [kwargs.get("batchSize", [1024,1024,1024]), "numericArr"],
        "blockSize": [kwargs.get("blockSize", [256,256,256]), "numericArr"],
        "largeFile": [kwargs.get("largeFile", False), "logical"],
        "largeMethod": [kwargs.get("largeMethod", "inmemory"), "char"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "dampFactor": [kwargs.get("dampFactor", 1), "numericScalar"],
        "scaleFactor": [kwargs.get("scaleFactor", []), "numericScalar"],
        "deconOffset": [kwargs.get("deconOffset", 0), "numericScalar"],
        "maskFullpaths": [kwargs.get("maskFullpaths", []), "cell"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "parseParfor": [kwargs.get("parseParfor", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 2), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "unitWaitTime": [kwargs.get("unitWaitTime", 1), "numericScalar"],
        "maxTrialNum": [kwargs.get("maxTrialNum", 3), "numericScalar"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "configFile": [kwargs.get("configFile", ""), "char"],
        "GPUConfigFile": [kwargs.get("GPUConfigFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_decon_data_wrapper_dict.items():
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
    