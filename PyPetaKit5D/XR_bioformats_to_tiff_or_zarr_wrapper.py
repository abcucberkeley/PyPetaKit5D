import os
from ._mcc import matlab_array, matlab_cell, matlab_logical_array, run_mcc


def XR_bioformats_to_tiff_or_zarr_wrapper(dataPaths, **kwargs):
    function_name = "XR_bioformats_to_tiff_or_zarr_wrapper"
    XR_bioformats_to_tiff_or_zarr_wrapper_dict = {
        "resultDirName": [kwargs.get("resultDirName", "tiffs"), "char"],
        "channelPatterns": [kwargs.get("channelPatterns", ['.nd2','.czi']), "cell"],
        "nChannels": [kwargs.get("nChannels", 2), "numericScalar"],
        "dataFormats": [kwargs.get("dataFormats", ['.nd2','.czi']), "cell"],
        "saveZarr": [kwargs.get("saveZarr", False), "logical"],
        "blockSize": [kwargs.get("blockSize", [256,256,256]), "numericArr"],
        "overWrite": [kwargs.get("overWrite", False), "logical"],
        "uuid": [kwargs.get("uuid", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = matlab_cell(dataPaths)
    cmdArgs = [mccMasterLoc, matlabRuntimeLoc, function_name, dataPathsString]
    
    for key, value in XR_bioformats_to_tiff_or_zarr_wrapper_dict.items():
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
    