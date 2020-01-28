import yaml
import os
#
# date: 20200124
# junhyeon.kim
#

class Argu():

    def __init__(self):

        ## 프로젝트 디렉토리 경로
        self._projDir = os.path.abspath(os.path.curdir)
        urgent = Argu.getInfo(self._projDir)
        comment = Argu.getCommentUrl(self._projDir)
        likeCount = Argu.getLikeCount(self._projDir)

        ## 댓글에 관한 정보
        self._userAgent = urgent["user_agent"]
        self._commentUrl = {"front": comment["front_param"], "rear": comment["rear_param"]}
        self._totalComment = list()
        self._apiUrl = comment["api_url"]

        ## 좋아요 싫어요에 대한 갯수 정보
        self._likeApiUrl = likeCount["api_url"]
        self._likePath = likeCount["path"]
        self._likeParams = {"front": likeCount["front_param"], "rear": likeCount["rear_param"]}
        self._likeParamArg = likeCount["value_param"]
        self._likeCount = None

    @classmethod
    def getInfo(cls, p):

        with open(r"../common/conf/url.yml", "r", encoding="utf-8") as f:
            info = yaml.safe_load(f)
            f.close()

        return info

    @classmethod
    def getCommentUrl(cls, p):

        with open(r"../common/conf/commenturl.yml", "r", encoding="utf-8") as f:
            info = yaml.safe_load(f)
            f.close()

        return info

    @classmethod
    def getLikeCount(cls, p):

        with open(r"../common/conf/likecounturl.yml", "r", encoding="utf-8") as f:
            info = yaml.safe_load(f)
            f.close()

        return info
