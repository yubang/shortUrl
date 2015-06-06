#coding:UTF-8

"""
短网址生成小应用
"""


from flask import Flask,redirect
from shortUrl.app import sApp


app=Flask(__name__)
app.register_blueprint(sApp,url_prefix="/shortUrl")


@app.route("/")
def index():
    "主页面"
    return redirect("/shortUrl")


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=8000)
