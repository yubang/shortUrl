#coding:UTF-8

from sqlalchemy import create_engine,MetaData,Table,Column
from sqlalchemy.sql.sqltypes import String,Integer,Text,TIMESTAMP
from sqlalchemy.orm import mapper,sessionmaker
import datetime
import config

db = create_engine("mysql://%s:%s@%s:%s/%s?charset=UTF8"%(config.MYSQL_USER,config.MYSQL_PASSWORD,config.MYSQL_HOST,config.MYSQL_PORT,config.MYSQL_DB))

urlTable = Table("shortUrl_urls",MetaData(db),
    Column("id",Integer,primary_key=True),
    Column("token",String(32),unique=True),
    Column("url",Text),
    Column("createTime",TIMESTAMP),
)

class UrlModel(object):
    "数据类"
    def __init__(self,token,url):
        self.token=token
        self.url=url
        self.createTime=datetime.datetime.now()
        
mapper(UrlModel,urlTable)
Session=sessionmaker(bind=db)
