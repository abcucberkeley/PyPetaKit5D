import os
import subprocess


def XR_matlab_stitching_wrapper(dataPath, imageListFileName, **kwargs):
    function_name = "XR_matlab_stitching_wrapper"
    XR_matlab_stitching_wrapper_dict = {
        "Streaming": [kwargs.get("Streaming", False), "logical"],
        "ChannelPatterns": [kwargs.get("ChannelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0']), "cell"],
        "multiLoc": [kwargs.get("multiLoc", False), "logical"],
        "ProcessedDirStr": [kwargs.get("ProcessedDirStr", ""), "char"],
        "stitchInfoFullpath": [kwargs.get("stitchInfoFullpath", ""), "char"],
        "DS": [kwargs.get("DS", False), "logical"],
        "DSR": [kwargs.get("DSR", False), "logical"],
        "SkewAngle": [kwargs.get("SkewAngle", 32.45), "numericScalar"],
        "Reverse": [kwargs.get("Reverse", False), "logical"],
        "parseSettingFile": [kwargs.get("parseSettingFile", False), "logical"],
        "axisOrder": [kwargs.get("axisOrder", "x,y,z"), "char"],
        "dataOrder": [kwargs.get("dataOrder", "y,x,z"), "char"],
        "ObjectiveScan": [kwargs.get("ObjectiveScan", False), "logical"],
        "IOScan": [kwargs.get("IOScan", False), "logical"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "largeZarr": [kwargs.get("largeZarr", False), "logical"],
        "poolSize": [kwargs.get("poolSize", []), "numericScalar"],
        "batchSize": [kwargs.get("batchSize", [500,500,500]), "numericArr"],
        "blockSize": [kwargs.get("blockSize", [500,500,500]), "numericArr"],
        "shardSize": [kwargs.get("shardSize", []), "numericArr"],
        "zarrSubSize": [kwargs.get("zarrSubSize", []), "numericArr"],
        "resampleType": [kwargs.get("resampleType", "xy_isotropic"), "char"],
        "resample": [kwargs.get("resample", []), "numericArr"],
        "InputBbox": [kwargs.get("InputBbox", []), "numericArr"],
        "tileOutBbox": [kwargs.get("tileOutBbox", []), "numericArr"],
        "TileOffset": [kwargs.get("TileOffset", 0), "numericScalar"],
        "Resolution": [kwargs.get("Resolution", [0.108,0.5]), "numericArr"],
        "resultDir": [kwargs.get("resultDir", "matlab_stitch"), "char"],
        "BlendMethod": [kwargs.get("BlendMethod", "none"), "char"],
        "overlapType": [kwargs.get("overlapType", ""), "char"],
        "xcorrShift": [kwargs.get("xcorrShift", True), "logical"],
        "xyMaxOffset": [kwargs.get("xyMaxOffset", 300), "numericScalar"],
        "zMaxOffset": [kwargs.get("zMaxOffset", 50), "numericScalar"],
        "xcorrDownsample": [kwargs.get("xcorrDownsample", [2,2,1]), "numericArr"],
        "xcorrThresh": [kwargs.get("xcorrThresh", 0.25), "numericScalar"],
        "padSize": [kwargs.get("padSize", []), "numericArr"],
        "boundboxCrop": [kwargs.get("boundboxCrop", []), "numericArr"],
        "zNormalize": [kwargs.get("zNormalize", False), "logical"],
        "onlyFirstTP": [kwargs.get("onlyFirstTP", False), "logical"],
        "timepoints": [kwargs.get("timepoints", []), "numericArr"],
        "subtimepoints": [kwargs.get("subtimepoints", []), "numericArr"],
        "xcorrMode": [kwargs.get("xcorrMode", "primaryFirst"), "char"],
        "shiftMethod": [kwargs.get("shiftMethod", "grid"), "char"],
        "axisWeight": [kwargs.get("axisWeight", [1,0.1,10]), "numericArr"],
        "groupFile": [kwargs.get("groupFile", ""), "char"],
        "primaryCh": [kwargs.get("primaryCh", ""), "char"],
        "usePrimaryCoords": [kwargs.get("usePrimaryCoords", False), "logical"],
        "Save16bit": [kwargs.get("Save16bit", False), "logical"],
        "EdgeArtifacts": [kwargs.get("EdgeArtifacts", 0), "numericScalar"],
        "distBboxes": [kwargs.get("distBboxes", []), "numericArr"],
        "saveMIP": [kwargs.get("saveMIP", True), "logical"],
        "stitchMIP": [kwargs.get("stitchMIP", []), "logicalArr"],
        "onlineStitch": [kwargs.get("onlineStitch", False), "logical"],
        "bigStitchData": [kwargs.get("bigStitchData", False), "logical"],
        "pipeline": [kwargs.get("pipeline", "zarr"), "char"],
        "processFunPath": [kwargs.get("processFunPath", ), "cell"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 8), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "maxTrialNum": [kwargs.get("maxTrialNum", 3), "numericScalar"],
        "unitWaitTime": [kwargs.get("unitWaitTime", 0.1), "numericScalar"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "ConfigFile": [kwargs.get("ConfigFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/LLSM5DTools/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2023a"
    dataPathString = "{" + ",".join(f"'{item}'" for item in dataPath) + "}"
    imageListFileNameString = "{" + ",".join(f"'{item}'" for item in imageListFileName) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathString}\" \"{imageListFileNameString}\" "
    
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
    