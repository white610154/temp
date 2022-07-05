class BasicSetting:
    projectName = ''
    runId = ''
    task = ''
    classNameList = ['NG', 'OK']

class PrivateSetting:
    datasetPath = ''
    outputPath = f'projects/{BasicSetting.projectName}/runs/{BasicSetting.runId}'