from enum import Enum


class DBCollectionsEnum(str, Enum):
    PROJECTS = 'projects'
    DATACHUNK = 'data_chunks'