import json
from pathlib import Path


def generateConfigFile(out_file, **kwargs):
    config_file_dict = {
        "BashLaunchStr": kwargs.get("BashLaunchStr", ""),
        "GNUparallel": kwargs.get("GNUparallel", True),
        "MCCMasterStr": kwargs.get("MCCMasterStr", "/home/matt/LLSM_Processing_GUI/LLSM5DTools/mcc/linux/run_mccMaster.sh"),
        "MCRParam": kwargs.get("MCRParam", "/home/matt/LLSM_Processing_GUI/MATLAB_Runtime/R2023a"),
        "MemPerCPU": kwargs.get("MemPerCPU", .01),
        "SlurmParam": kwargs.get("BashLaunchStr", ""),
        "jobTimeLimit": kwargs.get("jobTimeLimit", 12),
        "masterCompute": kwargs.get("masterCompute", True),
        "minCPUNum": kwargs.get("minCPUNum", 1),
        "maxCPUNum": kwargs.get("maxCPUNum", 24),
        "maxJobNum": kwargs.get("maxJobNum", 5000),
        "wholeNodeJob": kwargs.get("wholeNodeJob", False),
    }
    output_file = Path(f"{out_file}")
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(json.dumps(config_file_dict, ensure_ascii=False, indent=4))
    return


if __name__ == "__main__":
    generateConfigFile("testConfig.json")
