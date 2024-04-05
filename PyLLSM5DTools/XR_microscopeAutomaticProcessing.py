import os
import subprocess


def XR_microscopeAutomaticProcessing(dataPaths, **kwargs):
    function_name = "XR_microscopeAutomaticProcessing"
    XR_microscopeAutomaticProcessing_dict = {
        "Overwrite": [kwargs.get("Overwrite", False), "logical"],
        "Streaming": [kwargs.get("Streaming", True), "logical"],
        "ChannelPatterns": [kwargs.get("ChannelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0']), "cell"],
        "Channels": [kwargs.get("Channels", [488,560,642]), "numericArr"],
        "SkewAngle": [kwargs.get("SkewAngle", 32.45), "numericScalar"],
        "dz": [kwargs.get("dz", 0.5), "numericScalar"],
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "Reverse": [kwargs.get("Reverse", True), "logical"],
        "ObjectiveScan": [kwargs.get("ObjectiveScan", False), "logical"],
        "ZstageScan": [kwargs.get("ZstageScan", False), "logical"],
        "sCMOSCameraFlip": [kwargs.get("sCMOSCameraFlip", False), "logical"],
        "Save16bit": [kwargs.get("Save16bit", [False,False,False,False]), "logicalArr"],
        "onlyFirstTP": [kwargs.get("onlyFirstTP", False), "logical"],
        "dzFromEncoder": [kwargs.get("dzFromEncoder", False), "logical"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "save3DStack": [kwargs.get("save3DStack", True), "logical"],
        "Deskew": [kwargs.get("Deskew", True), "logical"],
        "Rotate": [kwargs.get("Rotate", True), "logical"],
        "Stitch": [kwargs.get("Stitch", False), "logical"],
        "Decon": [kwargs.get("Decon", True), "logical"],
        "RotateAfterDecon": [kwargs.get("RotateAfterDecon", False), "logical"],
        "parseSettingFile": [kwargs.get("parseSettingFile", False), "logical"],
        "flipZstack": [kwargs.get("flipZstack", False), "logical"],
        "DSRCombined": [kwargs.get("DSRCombined", True), "logical"],
        "LLFFCorrection": [kwargs.get("LLFFCorrection", False), "logical"],
        "BKRemoval": [kwargs.get("BKRemoval", False), "logical"],
        "LowerLimit": [kwargs.get("LowerLimit", 0.4), "numericScalar"],
        "constOffset": [kwargs.get("constOffset", []), "numericScalar"],
        "LSImagePaths": [kwargs.get("LSImagePaths", ['','','']), "cell"],
        "BackgroundPaths": [kwargs.get("BackgroundPaths", ['','','']), "cell"],
        "resampleType": [kwargs.get("resampleType", "isotropic"), "char"],
        "resample": [kwargs.get("resample", []), "numericArr"],
        "InputBbox": [kwargs.get("InputBbox", []), "numericArr"],
        "stitchPipeline": [kwargs.get("stitchPipeline", "zarr"), "char"],
        "stitchResultDir": [kwargs.get("stitchResultDir", ""), "char"],
        "imageListFullpaths": [kwargs.get("imageListFullpaths", ), "cell"],
        "axisOrder": [kwargs.get("axisOrder", "xyz"), "char"],
        "BlendMethod": [kwargs.get("BlendMethod", "none"), "char"],
        "xcorrShift": [kwargs.get("xcorrShift", False), "logical"],
        "xcorrMode": [kwargs.get("xcorrMode", "primaryFirst"), "char"],
        "xyMaxOffset": [kwargs.get("xyMaxOffset", 300), "numericScalar"],
        "zMaxOffset": [kwargs.get("zMaxOffset", 50), "numericScalar"],
        "EdgeArtifacts": [kwargs.get("EdgeArtifacts", 2), "numericScalar"],
        "timepoints": [kwargs.get("timepoints", []), "numericArr"],
        "boundboxCrop": [kwargs.get("boundboxCrop", []), "numericArr"],
        "primaryCh": [kwargs.get("primaryCh", ""), "char"],
        "stitchMIP": [kwargs.get("stitchMIP", []), "logicalArr"],
        "onlineStitch": [kwargs.get("onlineStitch", False), "logical"],
        "generateImageList": [kwargs.get("generateImageList", ""), "char"],
        "cudaDecon": [kwargs.get("cudaDecon", False), "logical"],
        "cppDecon": [kwargs.get("cppDecon", False), "logical"],
        "cppDeconPath": [kwargs.get("cppDeconPath", "/global/home/groups/software/sl-7.x86_64/modules/RLDecon_CPU/20200718/build-cluster/cpuDeconv"), "char"],
        "loadModules": [kwargs.get("loadModules", "moduleloadgcc/4.8.5;moduleloadfftw/3.3.6-gcc;moduleloadboost/1.65.1-gcc;moduleloadlibtiff/4.1.0;"), "char"],
        "cudaDeconPath": [kwargs.get("cudaDeconPath", "/global/home/groups/software/sl-7.x86_64/modules/cudaDecon/bin/cudaDeconv"), "char"],
        "OTFGENPath": [kwargs.get("OTFGENPath", "/global/home/groups/software/sl-7.x86_64/modules/cudaDecon/bin/radialft"), "char"],
        "DS": [kwargs.get("DS", False), "logical"],
        "DSR": [kwargs.get("DSR", False), "logical"],
        "Background": [kwargs.get("Background", []), "numericScalar"],
        "dzPSF": [kwargs.get("dzPSF", 0.1), "numericScalar"],
        "EdgeErosion": [kwargs.get("EdgeErosion", 8), "numericScalar"],
        "ErodeByFTP": [kwargs.get("ErodeByFTP", True), "logical"],
        "deconRotate": [kwargs.get("deconRotate", False), "logical"],
        "psfFullpaths": [kwargs.get("psfFullpaths", ['','','']), "cell"],
        "DeconIter": [kwargs.get("DeconIter", 15), "numericScalar"],
        "rotatedPSF": [kwargs.get("rotatedPSF", False), "logical"],
        "RLMethod": [kwargs.get("RLMethod", "simplified"), "char"],
        "fixIter": [kwargs.get("fixIter", False), "logical"],
        "errThresh": [kwargs.get("errThresh", []), "numericScalar"],
        "debug": [kwargs.get("debug", False), "logical"],
        "GPUJob": [kwargs.get("GPUJob", False), "logical"],
        "largeFile": [kwargs.get("largeFile", False), "logical"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 1), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "maxTrialNum": [kwargs.get("maxTrialNum", 3), "numericScalar"],
        "unitWaitTime": [kwargs.get("unitWaitTime", 1), "numericScalar"],
        "minModifyTime": [kwargs.get("minModifyTime", 1), "numericScalar"],
        "maxModifyTime": [kwargs.get("maxModifyTime", 10), "numericScalar"],
        "maxWaitLoopNum": [kwargs.get("maxWaitLoopNum", 10), "numericScalar"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "ConfigFile": [kwargs.get("ConfigFile", ""), "char"],
        "GPUConfigFile": [kwargs.get("GPUConfigFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/LLSM5DTools/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2023a"
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
    