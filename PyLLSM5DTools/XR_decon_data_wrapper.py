import os
import subprocess


def XR_decon_data_wrapper(dataPaths, **kwargs):
    function_name = "XR_decon_data_wrapper"
    XR_decon_data_wrapper_dict = {
        "deconPathstr": [kwargs.get("deconPathstr", ""), "char"],
        "Overwrite": [kwargs.get("Overwrite", False), "logical"],
        "ChannelPatterns": [kwargs.get("ChannelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0']), "cell"],
        "Channels": [kwargs.get("Channels", [488,560,642]), "numericArr"],
        "SkewAngle": [kwargs.get("SkewAngle", 32.45), "numericScalar"],
        "dz": [kwargs.get("dz", 0.5), "numericScalar"],
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "Reverse": [kwargs.get("Reverse", True), "logical"],
        "ObjectiveScan": [kwargs.get("ObjectiveScan", False), "logical"],
        "sCMOSCameraFlip": [kwargs.get("sCMOSCameraFlip", False), "logical"],
        "Save16bit": [kwargs.get("Save16bit", False), "logical"],
        "onlyFirstTP": [kwargs.get("onlyFirstTP", False), "logical"],
        "parseSettingFile": [kwargs.get("parseSettingFile", False), "logical"],
        "flipZstack": [kwargs.get("flipZstack", False), "logical"],
        "Decon": [kwargs.get("Decon", True), "logical"],
        "cudaDecon": [kwargs.get("cudaDecon", False), "logical"],
        "cppDecon": [kwargs.get("cppDecon", False), "logical"],
        "cppDeconPath": [kwargs.get("cppDeconPath", "/global/home/groups/software/sl-7.x86_64/modules/RLDecon_CPU/20200718/build-cluster/cpuDeconv"), "char"],
        "loadModules": [kwargs.get("loadModules", "moduleloadgcc/4.8.5;moduleloadfftw/3.3.6-gcc;moduleloadboost/1.65.1-gcc;moduleloadlibtiff/4.1.0;"), "char"],
        "cudaDeconPath": [kwargs.get("cudaDeconPath", "/global/home/groups/software/sl-7.x86_64/modules/cudaDecon/bin/cudaDeconv"), "char"],
        "OTFGENPath": [kwargs.get("OTFGENPath", "/global/home/groups/software/sl-7.x86_64/modules/cudaDecon/bin/radialft"), "char"],
        "Background": [kwargs.get("Background", []), "numericScalar"],
        "dzPSF": [kwargs.get("dzPSF", 0.1), "numericScalar"],
        "EdgeErosion": [kwargs.get("EdgeErosion", 8), "numericScalar"],
        "ErodeByFTP": [kwargs.get("ErodeByFTP", True), "logical"],
        "deconRotate": [kwargs.get("deconRotate", False), "logical"],
        "psfFullpaths": [kwargs.get("psfFullpaths", ['','','']), "cell"],
        "rotatePSF": [kwargs.get("rotatePSF", False), "logical"],
        "DeconIter": [kwargs.get("DeconIter", 15), "numericScalar"],
        "RLMethod": [kwargs.get("RLMethod", "simplified"), "char"],
        "wienerAlpha": [kwargs.get("wienerAlpha", 0.005), "numericScalar"],
        "OTFCumThresh": [kwargs.get("OTFCumThresh", 0.9), "numericScalar"],
        "hanWinBounds": [kwargs.get("hanWinBounds", [0.8,1.0]), "numericArr"],
        "skewed": [kwargs.get("skewed", []), "logical"],
        "fixIter": [kwargs.get("fixIter", False), "logical"],
        "errThresh": [kwargs.get("errThresh", []), "numericScalar"],
        "debug": [kwargs.get("debug", False), "logical"],
        "saveStep": [kwargs.get("saveStep", 5), "numericScalar"],
        "psfGen": [kwargs.get("psfGen", True), "logical"],
        "GPUJob": [kwargs.get("GPUJob", False), "logical"],
        "BatchSize": [kwargs.get("BatchSize", [1024,1024,1024]), "numericArr"],
        "BlockSize": [kwargs.get("BlockSize", [256,256,256]), "numericArr"],
        "zarrSubSize": [kwargs.get("zarrSubSize", []), "numericArr"],
        "largeFile": [kwargs.get("largeFile", False), "logical"],
        "largeMethod": [kwargs.get("largeMethod", "inmemory"), "char"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "damper": [kwargs.get("damper", 1), "numericScalar"],
        "scaleFactor": [kwargs.get("scaleFactor", []), "numericScalar"],
        "deconOffset": [kwargs.get("deconOffset", 0), "numericScalar"],
        "deconMaskFns": [kwargs.get("deconMaskFns", []), "cell"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "parseParfor": [kwargs.get("parseParfor", False), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 2), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "maxTrialNum": [kwargs.get("maxTrialNum", 3), "numericScalar"],
        "unitWaitTime": [kwargs.get("unitWaitTime", 10), "numericScalar"],
        "maxWaitLoopNum": [kwargs.get("maxWaitLoopNum", 10), "numericScalar"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "ConfigFile": [kwargs.get("ConfigFile", ""), "char"],
        "GPUConfigFile": [kwargs.get("GPUConfigFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/LLSM5DTools/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2023a"
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
    