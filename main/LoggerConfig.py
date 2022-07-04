from utils.Logger import *

def set_logger_config():
    Logger.config(
    logTypes=LogType.Console | LogType.File,
    consoleLogConfig=ConsoleLogConfig(
        level=LogLevel.WARNING,
        ),
    fileLogConfig=FileLogConfig(
        level=LogLevel.INFO,
        newline=False,
        dirname="logs",
        suffix="",
        ),
    )
