import os
from ._mcc import matlab_array, matlab_cell, matlab_logical_array, run_mcc


def XR_resample_dataset(dataPaths, resampleFactor, **kwargs):
    function_name = "XR_resample_dataset"
    XR_resample_dataset_dict = {
        "resultDirName": [kwargs.get("resultDirName", "resampled"), "char"],
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0','CamB_ch1']), "cell"],
        "inputBbox": [kwargs.get("inputBbox", []), "numericArr"],
        "interpMethod": [kwargs.get("interpMethod", "linear"), "char"],
        "save16bit": [kwargs.get("save16bit", True), "logical"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "largeFile": [kwargs.get("largeFile", False), "logical"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "blockSize": [kwargs.get("blockSize", [256,256,256]), "numericArr"],
        "batchSize": [kwargs.get("batchSize", [512,512,512]), "numericArr"],
        "borderSize": [kwargs.get("borderSize", [5,5,5]), "numericArr"],
        "parseCluster": [kwargs.get("parseCluster", False), "logical"],
        "jobLogDir": [kwargs.get("jobLogDir", "../job_logs"), "char"],
        "masterCompute": [kwargs.get("masterCompute", True), "logical"],
        "cpusPerTask": [kwargs.get("cpusPerTask", 2), "numericScalar"],
        "uuid": [kwargs.get("uuid", ""), "char"],
        "mccMode": [kwargs.get("mccMode", False), "logical"],
        "configFile": [kwargs.get("configFile", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = matlab_cell(dataPaths)
    resampleFactorString = matlab_array(resampleFactor)
    cmdArgs = [mccMasterLoc, matlabRuntimeLoc, function_name, dataPathsString, resampleFactorString]
    
    for key, value in XR_resample_dataset_dict.items():
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
    