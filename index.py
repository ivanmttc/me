from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>莫天賜個人網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=tcyang>傳送使用者暱稱</a><br>"
    homepage += "<a href=/about>莫天賜簡介網頁</a><br>"
    homepage += "<a href=/work>工作需求</a><br>"
    homepage += "<br><a href=/read>讀取Firestore資料</a><br>"
    return homepage

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html", datetime = str(now))

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)


@app.route("/about")
def account():
    
        return render_template("about.html")

@app.route("/work")
def work():
    
        return render_template("work.html")
    
   

#if __name__ == "__main__":
#   app.run()

