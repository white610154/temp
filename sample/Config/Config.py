class BasicSetting:
    projectName = ""
    runId       = ""
    task        = ""

class PrivateSetting:
    datasetPath  = ""
    outputPath   = f"projects/{BasicSetting.projectName}/runs/{BasicSetting.runId}"