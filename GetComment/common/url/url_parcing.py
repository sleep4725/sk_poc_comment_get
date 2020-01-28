from urllib.parse import urlparse

def jsonParcing(raw):

    result = {"comment": None, "like": None, "index_name": None, "document_id": None}

    ## 인덱스 이름 규칙 : sk_poc_news_cat1_cat2
    _indexName = "sk_poc_news_" + raw["cat1"] + "_" + raw["cat2"] + "_comment"
    result["index_name"] = _indexName

    article_url = str(raw["article_url"]).replace("https", "http")

    ## document id 규칙 : sid1{}oid{}aid{}
    queryDict = dict()
    query = urlparse(article_url).query
    q = query.split("&")

    for i in q:
        k, v = i.split("=")
        queryDict[k] = v

    _documentId = "sid1{}oid{}aid{}".format(queryDict["sid1"], queryDict["oid"], queryDict["aid"])
    result["document_id"] = _documentId

    ## comment param
    _objectId = "news" + queryDict["oid"] + "%2C" + queryDict["aid"]
    result["comment"] = _objectId

    ## --------------------------------------------------------
    ## params = commentUrl["front"] + objectId_ + commentUrl["rear"]

    ## like param
    ne = "ne_{}_{}".format(queryDict["oid"], queryDict["aid"])
    value = "NEWS" + "%5B" + ne + "%5D%7C" + "NEWS_MAIN" + "%5B" + ne + "%5D"
    ##value_param = self._likeParamArg.format(value)
    result["like"] = value

    return result