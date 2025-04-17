import os
import subprocess


def XR_psf_analysis_wrapper(dataPaths, **kwargs):
    function_name = "XR_psf_analysis_wrapper"
    XR_psf_analysis_wrapper_dict = {
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "dz": [kwargs.get("dz", 0.1), "numericScalar"],
        "skewAngle": [kwargs.get("skewAngle", 32.45), "numericScalar"],
        "deskew": [kwargs.get("deskew", True), "logical"],
        "flipZstack": [kwargs.get("flipZstack", False), "logical"],
        "objectiveScan": [kwargs.get("objectiveScan", False), "logical"],
        "zStageScan": [kwargs.get("zStageScan", False), "logical"],
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA_ch0','CamB_ch0']), "cell"],
        "channels": [kwargs.get("channels", [488,560]), "numericArr"],
        "save16bit": [kwargs.get("save16bit", True), "logical"],
        "bgFactor": [kwargs.get("bgFactor", 1.5), "numericScalar"],
        "RWFn": [kwargs.get("RWFn", ['','']), "cell"],
        "sourceStr": [kwargs.get("sourceStr", "test"), "char"],
        "visible": [kwargs.get("visible", True), "logical"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", False), "logical"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 8), "numericScalar"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "configFile": [kwargs.get("configFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux_with_jvm/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_psf_analysis_wrapper_dict.items():
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
    