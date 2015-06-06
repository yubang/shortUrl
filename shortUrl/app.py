#coding:UTF-8

"""
短网址生成器
@author:yubang
2015-06-06
"""


from flask import Blueprint,render_template,make_response,request,abort,redirect
from werkzeug.contrib.cache import SimpleCache
from models import Session,UrlModel
import hashlib,json

sApp=Blueprint("shortUrl",__name__)
cache=SimpleCache()

@sApp.route("/")
def index():
    "主界面"
    return render_template("shortUrl/index.html")

@sApp.route("/buildUrl",methods=['POST'])
def buildUrl():
    "生成短网址"
    
    url = request.form.get("url",None)
    token=hashlib.md5(url).hexdigest()
    
    dbSession=Session()
    query=dbSession.query(UrlModel)
    obj=query.filter(UrlModel.token == token).first()
    
    if obj == None:
        obj = UrlModel(token,url)
        dbSession.add(obj)
        dbSession.commit()
        key = obj.id 
    else:
        key = obj.id    
    dbSession.close()
    
    key=str(hex(key))[2:]
    key=key[:len(key)-1]
    key="http://"+request.headers['host']+"/shortUrl/s/"+key
    
    response = make_response(json.dumps({"key":key}))
    response.headers['Content-Type']="application/json"
    return response
    

@sApp.route("/s/<key>")
def s(key):
    "转到指定网址"
    key=int("0x"+key,16)
    
    global cache
    cacheKey="shortUrl_"+str(key)
    r=cache.get(cacheKey)
    
    if r == None:
        dbSession=Session()
        obj=dbSession.query(UrlModel).filter(UrlModel.id == key).first()
    
        if obj == None:
            r = None
        else:
            r = obj.url
            cache.set(cacheKey,r)
        dbSession.close()
    
    if r == None:
        return abort(404)
    
    return redirect(r)
