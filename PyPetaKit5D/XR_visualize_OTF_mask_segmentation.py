import os
from ._mcc import matlab_array, matlab_cell, matlab_logical_array, run_mcc


def XR_visualize_OTF_mask_segmentation(psfFn, OTFCumThresh, skewed, **kwargs):
    function_name = "XR_visualize_OTF_mask_segmentation"
    XR_visualize_OTF_mask_segmentation_dict = {
        "minIntThrsh": [kwargs.get("minIntThrsh", 1e-3), "numericScalar"],
        "visible": [kwargs.get("visible", True), "logical"],
        "saveFig": [kwargs.get("saveFig", False), "logical"]
    }

    mccMasterLoc = f"{os.path.dirname(os.path.abspath(__file__))}/PetaKit5D/mcc/linux_with_jvm/run_mccMaster.sh"
    matlabRuntimeLoc = f"{os.path.dirname(os.path.abspath(__file__))}/MATLAB_Runtime/R2024b"
    cmdArgs = [mccMasterLoc, matlabRuntimeLoc, function_name, psfFn, OTFCumThresh, str(skewed).lower()]
    
    for key, value in XR_visualize_OTF_mask_segmentation_dict.items():
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
    