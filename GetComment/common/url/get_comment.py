import requests
from bs4 import BeautifulSoup
import json
from GetComment.common.url.Arg import Argu

class Url(Argu):

    def __init__(self):
        Argu.__init__(self)

    def url_request(self, referer, rpath):
        request_header = {
            "referer": referer, "User-agent": self._userAgent
        }

        page_ = 1

        while True:

            p = self._commentUrl["front"] + rpath["comment"] + self._commentUrl["rear"]
            url = self._apiUrl + p.format(page_)
            #print(url)
            html = requests.get(url, headers=request_header)
            if html.status_code == 200:

                #print("requests success")
                bsObject = BeautifulSoup(html.text, "html.parser")
                total_comm = str(bsObject).split('comment":')[1].split(",")[0]
                response = str(bsObject).replace("jQuery112406597307147215103_1579692795671(", "").replace(");", "")
                jsonDoc = json.loads(response)["result"]["commentList"]

                for i in jsonDoc:
                    c = str(i["contents"])
                    if c:
                        c = c.replace("\n", "").strip()
                        self._totalComment.append(c)

                ## 한번에 댓글이 20개씩 보이기 때문에 한 페이지씩 몽땅 댓글을 긁어 옵니다.
                if int(total_comm) <= ((page_) * 20):
                    break
                else:
                    page_ += 1

        #print(self._totalComment)


    def like_and_hate_count(self, referer, rpath):

        headers = {
            "referer": referer, "User-agent": self._userAgent
        }
        value_param = self._likeParamArg.format(rpath["like"])

        section = {"like": 0, "sad": 0, "angry": 0, "want": 0, "warm": 0}

        requrl = self._likeApiUrl + self._likePath + self._likeParams["front"] + value_param + self._likeParams["rear"]
        with requests.get(requrl, headers=headers) as html:
            if html.status_code == 200:
                response = BeautifulSoup(html.text, "html.parser")
                response = str(response).replace("/**/jQuery112407620232249431651_1579779150521(", "").rstrip(");")
                jsonDoc = json.loads(response)
                contents = jsonDoc["contents"]

                reactions = [c["reactions"] for c in contents][0]
                # self._likeCount = [{r["reactionType"]: r["count"]} for r in reactions]
                # print(self._likeCount)

                for r in reactions:
                    section[r["reactionType"]] = r["count"]
                # print(section)
                self._likeCount = section

            html.close()