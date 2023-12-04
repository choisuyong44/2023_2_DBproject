from flask import Flask ,render_template
import showMap

# Flask 클래스 인스턴스화
app = Flask(__name__)

# 사용자의 주소 읽어와서 지도로 표시
showMap.showToiletMap()

@app.route("/")
def start():
    return render_template("main.html")

@app.route("/my_map.html")
def findToilet():
    return render_template("my_map.html")

if __name__ == '__main__':
    app.run(port=5050)