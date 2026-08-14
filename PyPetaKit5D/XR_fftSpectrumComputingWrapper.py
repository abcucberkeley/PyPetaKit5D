import os
from ._mcc import matlab_array, matlab_cell, matlab_logical_array, run_mcc


def XR_fftSpectrumComputingWrapper(dataPaths, **kwargs):
    function_name = "XR_fftSpectrumComputingWrapper"
    XR_fftSpectrumComputingWrapper_dict = {
        "resultDirName": [kwargs.get("resultDirName", "FFT"), "char"],
        "overwrite": [kwargs.get("overwrite", False), "logical"],
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "dz": [kwargs.get("dz", 0.1), "numericScalar"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "outPixelSize": [kwargs.get("outPixelSize", []), "numericScalar"],
        "outSize": [kwargs.get("outSize", [1001,1001,1001]), "numericArr"],
        "channelPatterns": [kwargs.get("channelPatterns", []), "cell"],
        "save3DStack": [kwargs.get("save3DStack", False), "logical"],
        "background": [kwargs.get("background", 0), "numericScalar"],
        "interpMethod": [kwargs.get("interpMethod", "linear"), "char"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 3), "numericScalar"],
        "debug": [kwargs.get("debug", False), "logical"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "configFile": [kwargs.get("configFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = matlab_cell(dataPaths)
    cmdArgs = [mccMasterLoc, matlabRuntimeLoc, function_name, dataPathsString]
    
    for key, value in XR_fftSpectrumComputingWrapper_dict.items():
        if value[1] == "char":
            if not value[0]:
                continue
            cmdArgs += [key, value[0]]
        elif value[1] == "cell":
            if not value[0]:
                continue
            cmdArgs += [key, matlab_cell(value[0])]
        elif value[1] == "logicalArr":
            cmdArgs += [key, matlab_logical_array(value[0])]
        elif value[1] == "logical":
            cmdArgs += [key, str(value[0]).lower()]
        elif value[1] == "numericArr":
            if not value[0]:
                continue
            if type(value[0]) is not list:
                value[0] = [value[0]]
            numericArrString = matlab_array(value[0])
            cmdArgs += [key, numericArrString]
        elif value[1] == "numericScalar":
            if type(value[0]) is list:
                if not value[0]:
                    continue
                else:
                    value[0] = value[0][0]
            cmdArgs += [key, value[0]]
        else:
            continue
    run_mcc(cmdArgs, function_name)
    