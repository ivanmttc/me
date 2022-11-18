import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from flask import Flask, render_template, request
from datetime import datetime,timezone,timedelta
app = Flask(__name__)



@app.route("/")
def index():
    homepage = "<h1>莫天賜Python網頁</h1>"
    homepage += "<br><a href=/movie>天賜電影</a><br>"
    return homepage



@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        cond = request.form["keyword"]
        result = "請輸入您要查詢的課程關鍵字：" + cond

        db = firestore.client()
        collection_ref = db.collection("111")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if cond in dict["Course"]:
                #print("{}老師開的{}課程,每週{}於{}上課".format(dict["Leacture"], dict["Course"],  dict["Time"],dict["Room"]))
                result += dict["Leacture"] + "老師開的" + dict["Course"] + "課程,每週"
                result += dict["Time"] + "於" + dict["Room"] + "上課<br>"
        print(result)
        if result == "":
            result = "sorry....."
        return result
    else:
        return render_template("search.html")


if __name__ == "__main__":
    app.run()

    import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("firebase鎖匙.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

import requests
from bs4 import BeautifulSoup
url = "http://www.atmovies.com.tw/movie/next/"
Data = requests.get(url)
Data.encoding = "utf-8"
#print(Data.text)
sp = BeautifulSoup(Data.text, "html.parser")
result=sp.select(".filmListAllX li")
#print(result)
lastUpdate = sp.find("div", class_="smaller09").text[5:]

info = ""
for item in result:
  rate = None
  if item.find("div", class_="runtime").img != None:
    rate = item.find("div", class_="runtime").find("img").get("src")

  if rate == "/images/cer_R.gif":
    rate ="限制級（未滿十八歲之人不得觀賞）"
  elif rate == "/images/cer_F5.gif":
    rate = "輔導級(未滿十五歲之人不得觀賞)"
  elif rate == "/images/cer_F2.gif":
    rate = "輔導級(未滿十二歲之兒童不得觀賞)"
  elif rate =="/images/cer_P.gif":
    rate = "保護級(未滿六歲之兒童不得觀賞，六歲以上未滿十二歲之兒童須父母、師長或成年親友陪伴輔導觀賞)"
  elif rate =="/images/cer_G.gif":
    rate ="普遍級(一般觀眾皆可觀賞)"
  elif rate == None:
    rate ="尚無雷影分級資訊"

  picture = item.find("img").get("src").replace(" ", "")
  title = item.find("div", class_="filmtitle").text
  movie_id = item.find("div", class_="filmtitle").find("a").get("href").replace("/", "").replace("movie", "")
  hyperlink = "http://www.atmovies.com.tw" + item.find("div", class_="filmtitle").find("a").get("href")
  show = item.find("div", class_="runtime").text.replace("上映日期：", "")
  show = show.replace("片長：", "")
  show = show.replace("分", "")
  showDate = show[0:10]
  showLength = show[13:]
  info += title +"\n" + picture + "\n" + hyperlink +"\n"+showDate + "\n" + showLength +"\n"+ rate + "\n"
  doc = {
  "title": title,
  "picture": picture,
  "hyperlink": hyperlink,
  "showDate": showDate,
  "showLength": showLength,
  "lastUpdate": lastUpdate,
  "rate":rate
}
  doc_ref = db.collection("天賜電影").document(movie_id)
  doc_ref.set(doc)

print(info)
