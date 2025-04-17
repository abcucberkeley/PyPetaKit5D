import os
import subprocess


def XR_microscopeAutomaticProcessing(dataPaths, **kwargs):
    function_name = "XR_microscopeAutomaticProcessing"
    XR_microscopeAutomaticProcessing_dict = {
        "overwrite": [kwargs.get("overwrite", False), "logical"],
        "streaming": [kwargs.get("streaming", True), "logical"],
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0']), "cell"],
        "skewAngle": [kwargs.get("skewAngle", 32.45), "numericScalar"],
        "dz": [kwargs.get("dz", 0.5), "numericScalar"],
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "reverse": [kwargs.get("reverse", True), "logical"],
        "objectiveScan": [kwargs.get("objectiveScan", False), "logical"],
        "zStageScan": [kwargs.get("zStageScan", False), "logical"],
        "save16bit": [kwargs.get("save16bit", [True,True]), "logicalArr"],
        "dzFromEncoder": [kwargs.get("dzFromEncoder", False), "logical"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "save3DStack": [kwargs.get("save3DStack", True), "logical"],
        "deskew": [kwargs.get("deskew", True), "logical"],
        "rotate": [kwargs.get("rotate", True), "logical"],
        "stitch": [kwargs.get("stitch", False), "logical"],
        "parseSettingFile": [kwargs.get("parseSettingFile", False), "logical"],
        "flipZstack": [kwargs.get("flipZstack", False), "logical"],
        "inputAxisOrder": [kwargs.get("inputAxisOrder", "yxz"), "char"],
        "outputAxisOrder": [kwargs.get("outputAxisOrder", "yxz"), "char"],
        "DSRCombined": [kwargs.get("DSRCombined", True), "logical"],
        "FFCorrection": [kwargs.get("FFCorrection", False), "logical"],
        "BKRemoval": [kwargs.get("BKRemoval", False), "logical"],
        "lowerLimit": [kwargs.get("lowerLimit", 0.4), "numericScalar"],
        "constOffset": [kwargs.get("constOffset", []), "numericScalar"],
        "FFImagePaths": [kwargs.get("FFImagePaths", ['','','']), "cell"],
        "backgroundPaths": [kwargs.get("backgroundPaths", ['','','']), "cell"],
        "resampleType": [kwargs.get("resampleType", "isotropic"), "char"],
        "resampleFactor": [kwargs.get("resampleFactor", []), "numericArr"],
        "inputBbox": [kwargs.get("inputBbox", []), "numericArr"],
        "stitchResultDirName": [kwargs.get("stitchResultDirName", ""), "char"],
        "imageListFullpaths": [kwargs.get("imageListFullpaths", ""), "cell"],
        "axisOrder": [kwargs.get("axisOrder", "xyz"), "char"],
        "blendMethod": [kwargs.get("blendMethod", "none"), "char"],
        "xcorrShift": [kwargs.get("xcorrShift", False), "logical"],
        "xcorrMode": [kwargs.get("xcorrMode", "primaryFirst"), "char"],
        "xyMaxOffset": [kwargs.get("xyMaxOffset", 300), "numericScalar"],
        "zMaxOffset": [kwargs.get("zMaxOffset", 50), "numericScalar"],
        "edgeArtifacts": [kwargs.get("edgeArtifacts", 2), "numericScalar"],
        "primaryCh": [kwargs.get("primaryCh", ""), "char"],
        "stitchMIP": [kwargs.get("stitchMIP", []), "logicalArr"],
        "onlineStitch": [kwargs.get("onlineStitch", False), "logical"],
        "generateImageList": [kwargs.get("generateImageList", ""), "char"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 1), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "maxTrialNum": [kwargs.get("maxTrialNum", 3), "numericScalar"],
        "unitWaitTime": [kwargs.get("unitWaitTime", 1), "numericScalar"],
        "minModifyTime": [kwargs.get("minModifyTime", 1), "numericScalar"],
        "maxModifyTime": [kwargs.get("maxModifyTime", 10), "numericScalar"],
        "maxWaitLoopNum": [kwargs.get("maxWaitLoopNum", 10), "numericScalar"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "configFile": [kwargs.get("configFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_microscopeAutomaticProcessing_dict.items():
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
    