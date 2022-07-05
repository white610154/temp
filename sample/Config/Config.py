class BasicSetting:
    projectName = ''
    runId = ''
    task = ''
    classNameList = []

class PrivateSetting:
    datasetPath = ''
    outputPath = f'projects/{BasicSetting.projectName}/runs/{BasicSetting.runId}'