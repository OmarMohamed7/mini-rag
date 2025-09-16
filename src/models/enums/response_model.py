from enum import Enum


class ResponseModel(Enum):
    SUCCESS = "success"
    FILE_UPLOADED = "file uploaded successfully"
    FILE_VALIDATED = "file validated successfully"
    FILE_NOT_VALIDATED = "file not validated"
    FILE_SIZE_TOO_LARGE = "file size is too large"
    FILE_EMPTY = "file is empty"
    FILE_TYPE_NOT_ALLOWED = "file type not allowed"
    FILE_NOT_FOUND = "file not found"
    FILE_NOT_UPLOADED = "file not uploaded"
    FILE_NOT_PROCESSED = "file not processed"
    PROJECT_CREATED = "project created successfully"
    PROJECT_FOUND = "project found"
    PROJECT_NOT_FOUND = "project not found"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    TRACE = "trace"
    FATAL = "fatal"
