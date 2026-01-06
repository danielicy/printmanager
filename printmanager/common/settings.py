from enum import Enum


class JOB_STATUS(Enum):
    Processing = 'Processing'
    Future = 'Future'
    Completed  = 'Completed'
    Failed = 'Failed'
    Terminated = 'Terminated'