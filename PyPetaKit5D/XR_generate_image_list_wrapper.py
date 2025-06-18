import os
import subprocess


def XR_generate_image_list_wrapper(dataPaths, generationMethod, **kwargs):
    function_name = "XR_generate_image_list_wrapper"
    XR_generate_image_list_wrapper_dict = {
        "channelPatterns": [kwargs.get("channelPatterns", ['CamA_ch0','CamA_ch1','CamB_ch0']), "cell"],
        "mapTilename": [kwargs.get("mapTilename", True), "logical"],
        "tilePatterns": [kwargs.get("tilePatterns", ['0000t','ch0','000x','000y','000z']), "cell"],
        "tileFilenames": [kwargs.get("tileFilenames", []), "cell"],
        "tileIndices": [kwargs.get("tileIndices", []), "numericArr"],
        "tileInterval": [kwargs.get("tileInterval", []), "numericArr"],
        "DS": [kwargs.get("DS", False), "logical"],
        "DSR": [kwargs.get("DSR", False), "logical"],
        "xyPixelSize": [kwargs.get("xyPixelSize", 0.108), "numericScalar"],
        "dz": [kwargs.get("dz", 0.2), "numericScalar"],
        "skewAngle": [kwargs.get("skewAngle", 32.45), "numericScalar"],
        "axisOrder": [kwargs.get("axisOrder", "x,y,z"), "char"],
        "dataOrder": [kwargs.get("dataOrder", "y,x,z"), "char"],
        "objectiveScan": [kwargs.get("objectiveScan", False), "logical"],
        "IOScan": [kwargs.get("IOScan", False), "logical"],
        "zarrFile": [kwargs.get("zarrFile", False), "logical"],
        "overlapSize": [kwargs.get("overlapSize", [10,10,10]), "numericArr"],
        "overlapSizeType": [kwargs.get("overlapSizeType", "pixel"), "char"],
        "uuid": [kwargs.get("uuid", ""), "char"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    dataPathsString = "{" + ",".join(f"'{item}'" for item in dataPaths) + "}"
    cmdString = f"\"{mccMasterLoc}\" \"{matlabRuntimeLoc}\" {function_name} \"{dataPathsString}\" \"{generationMethod}\" "
    
    for key, value in XR_generate_image_list_wrapper_dict.items():
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
            separator = ","
            if key == "tileIndices":
                separator = ";"
            numericArrString = "[" + separator.join(str(item) for item in value[0]) + "]"
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
    