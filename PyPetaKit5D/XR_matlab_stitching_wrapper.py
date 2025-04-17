import os
import subprocess


def XR_matlab_stitching_wrapper(dataPaths, imageListFullpaths, **kwargs):
    function_name = "XR_matlab_stitching_wrapper"
    XR_matlab_stitching_wrapper_dict = {
        "resultDirName": [kwargs.get("resultDirName", "matlab_stitch"), "char"],
        "streaming": [kwargs.get("streaming", False), "logical"],
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0']), "cell"],
        "multiLoc": [kwargs.get("multiLoc", False), "logical"],
        "processedDirStr": [kwargs.get("processedDirStr", ""), "char"],
        "stitchInfoFullpath": [kwargs.get("stitchInfoFullpath", ""), "char"],
        "DS": [kwargs.get("DS", False), "logical"],
        "DSR": [kwargs.get("DSR", False), "logical"],
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "dz": [kwargs.get("dz", 0.5), "numericScalar"],
        "skewAngle": [kwargs.get("skewAngle", 32.45), "numericScalar"],
        "reverse": [kwargs.get("reverse", False), "logical"],
        "parseSettingFile": [kwargs.get("parseSettingFile", False), "logical"],
        "axisOrder": [kwargs.get("axisOrder", "x,y,z"), "char"],
        "dataOrder": [kwargs.get("dataOrder", "y,x,z"), "char"],
        "objectiveScan": [kwargs.get("objectiveScan", False), "logical"],
        "IOScan": [kwargs.get("IOScan", False), "logical"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "largeFile": [kwargs.get("largeFile", False), "logical"],
        "poolSize": [kwargs.get("poolSize", []), "numericScalar"],
        "batchSize": [kwargs.get("batchSize", [512,512,512]), "numericArr"],
        "blockSize": [kwargs.get("blockSize", [256,256,256]), "numericArr"],
        "shardSize": [kwargs.get("shardSize", []), "numericArr"],
        "resampleType": [kwargs.get("resampleType", "xy_isotropic"), "char"],
        "resampleFactor": [kwargs.get("resampleFactor", []), "numericArr"],
        "inputBbox": [kwargs.get("inputBbox", []), "numericArr"],
        "tileOutBbox": [kwargs.get("tileOutBbox", []), "numericArr"],
        "tileOffset": [kwargs.get("tileOffset", 0), "numericScalar"],
        "blendMethod": [kwargs.get("blendMethod", "feather"), "char"],
        "overlapType": [kwargs.get("overlapType", ""), "char"],
        "xcorrShift": [kwargs.get("xcorrShift", True), "logical"],
        "xyMaxOffset": [kwargs.get("xyMaxOffset", [300]), "numericArr"],
        "zMaxOffset": [kwargs.get("zMaxOffset", 50), "numericScalar"],
        "xcorrDownsample": [kwargs.get("xcorrDownsample", [2,2,1]), "numericArr"],
        "xcorrThresh": [kwargs.get("xcorrThresh", 0.25), "numericScalar"],
        "outBbox": [kwargs.get("outBbox", []), "numericArr"],
        "xcorrMode": [kwargs.get("xcorrMode", "primaryFirst"), "char"],
        "shiftMethod": [kwargs.get("shiftMethod", "grid"), "char"],
        "axisWeight": [kwargs.get("axisWeight", [1,0.1,10]), "numericArr"],
        "groupFile": [kwargs.get("groupFile", ""), "char"],
        "primaryCh": [kwargs.get("primaryCh", ""), "char"],
        "usePrimaryCoords": [kwargs.get("usePrimaryCoords", False), "logical"],
        "save16bit": [kwargs.get("save16bit", True), "logical"],
        "edgeArtifacts": [kwargs.get("edgeArtifacts", 0), "numericScalar"],
        "distBboxes": [kwargs.get("distBboxes", []), "numericArr"],
        "saveMIP": [kwargs.get("saveMIP", True), "logical"],
        "stitchMIP": [kwargs.get("stitchMIP", []), "logicalArr"],
        "onlineStitch": [kwargs.get("onlineStitch", False), "logical"],
        "processFunPath": [kwargs.get("processFunPath", ""), "cell"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 8), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "maxTrialNum": [kwargs.get("maxTrialNum", 3), "numericScalar"],
        "unitWaitTime": [kwargs.get("unitWaitTime", 0.1), "numericScalar"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "configFile": [kwargs.get("configFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    imageListFullpathsString = "{" + ",".join(f"'{item}'" for item in imageListFullpaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" \"{imageListFullpathsString}\" "
    
    for key, value in XR_matlab_stitching_wrapper_dict.items():
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
    