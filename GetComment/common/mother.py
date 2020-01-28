from abc import *
class Mother(metaclass=ABCMeta):

    def __init__(self):
        ## 디렉토리 경로
        self.dirpath = ""
        ## 로그 파일 경로
        self.logpath = ""

    @abstractmethod
    def listDir(self):
        pass