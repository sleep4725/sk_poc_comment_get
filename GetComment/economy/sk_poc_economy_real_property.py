import json
import os

from GetComment.economy.commcode import *
from GetComment.common.mother import Mother
from GetComment.common.url.url_parcing import jsonParcing
from GetComment.common.url.get_comment import Url


class ECONOY_REALPROPERTY(Mother, Url):

    def __init__(self):
        Url.__init__(self)
        Mother.__init__(self)
        self.dirpath = path + "\\real_property"
        self.logpath = path + "\\log\\real_property"
        self.writefilepathComment = r"C:\Users\ezfarm\PycharmProjects\sk_poc_comment_get\GetComment\economy\filew\comment\economy_real_property.json"
        self.writefilepathLike = r"C:\Users\ezfarm\PycharmProjects\sk_poc_comment_get\GetComment\economy\filew\like\economy_real_property.json"

    def listDir(self):

        print("수집 시작")
        for f in os.listdir(self.dirpath):
            with open(self.dirpath+"\\"+f, "r", encoding="utf-8") as f:
                for i in f.readlines():
                    i = json.loads(str(i).replace("\n", ""))

                    d = {"news_date": i["news_date"], "cat1": i["cat1"], "cat2": i["cat2"], "collect_time": i["collect_time"],
                         "article_url": i["article_url"]}

                    ## 분리
                    total_data = jsonParcing(d)
                    ## 댓글 요청
                    self.url_request(referer=d["article_url"], rpath=total_data)
                    ## 좋아요 요청
                    self.like_and_hate_count(referer=d["article_url"], rpath=total_data)
                    ## 파일 쓰기 ( 댓글)
                    with open(self.writefilepathComment, "a", encoding="utf-8") as fw:
                        for i in self._totalComment:
                            fw.write(json.dumps({"comment": i,
                                      "cat1": d["cat1"],
                                      "cat2": d["cat2"],
                                      "collect_time": d["collect_time"],
                                      "commentid": total_data["document_id"]}, ensure_ascii=False) + "\n")

                        fw.close()

                    ## 파일 쓰기 ( 좋아요)
                    bodyLike = json.dumps({"emotion": self._likeCount,
                                              "cat1": d["cat1"],
                                              "cat2": d["cat2"],
                                              "collect_time": d["collect_time"],
                                              "commentid": total_data["document_id"]}, ensure_ascii=False)

                    with open(self.writefilepathLike, "a", encoding="utf-8") as fw:
                        fw.write(bodyLike + "\n")
                    fw.close()

                    self._totalComment.clear()
                    self._likeCount = None

            f.close()
        print("수집 끝")

if __name__ == "__main__":
    o = ECONOY_REALPROPERTY()
    o.listDir()