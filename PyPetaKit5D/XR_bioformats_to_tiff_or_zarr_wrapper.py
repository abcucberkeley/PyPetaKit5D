import os
import subprocess


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
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" "
    
    for key, value in XR_bioformats_to_tiff_or_zarr_wrapper_dict.items():
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
    