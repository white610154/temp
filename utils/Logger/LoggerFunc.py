from .ConsoleLogger import ConsoleLogConfig, ConsoleLogger
from .FileLogger import FileLogConfig, FileLogger


def console_logger(config: ConsoleLogConfig) -> ConsoleLogger:
    return ConsoleLogger(config)

def file_logger(config: FileLogConfig) -> FileLogger:
    return FileLogger(config)
