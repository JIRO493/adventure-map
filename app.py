from flask import Flask,render_template,request,jsonify
from geopy.distance import geodesic
import folium
app=Flask(__name__)

spots=[
        {"name":"明治神宮","location":[35.6764,139.6993], "desc":"東京を代表する神社。森林に囲まれた聖地。"},
        {"name":"芝大神宮","location":[35.6565,139.7517],"desc":"一千年以上の歴史を誇る神社。"}
    ]

@app.route("/")
def index():
 #東京の地図
 m=folium.Map(location=[35.68, 139.76], zoom_start=14)

 for spot in spots:
       folium.Marker(location=spot["location"],popup=f'{spot["name"]}:{spot["desc"]}').add_to(m)

 map_html=m._repr_html_()

 return render_template("index.html",map_html=map_html)

@app.route("/check")
def check():
#URLパラメータからユーザーの座標を取得
  user_lat=float(request.args.get("lat"))
  user_lon=float(request.args.get("lon"))
  user_loc=(user_lat,user_lon)

  result=[]
  for spot in spots:
      spot_loc=tuple(spot["location"])
      distance=geodesic(user_loc,spot_loc).meters
      result.append({"name":spot["name"],"can_clear":distance<50})
  return jsonify({"spot":result})

if __name__=="__main__":
    app.run(debug=True)
    
    


