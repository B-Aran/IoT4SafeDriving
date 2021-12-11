from flask import Flask, request, jsonify
import json, pymongo, time, calendar
#API KEY
#AIzaSyBKn5YAFZK_y3LfVVDRhTXGRz-0SZE5EN0
app = Flask(__name__)
mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")
mydb = mongo_client["IoT4safedb"]
gps_col = mydb["gps_col"]
imu_col = mydb["imu_col"]
geo_col = mydb["geo_col"]
dat_col = mydb["datos_col"]

@app.route('/')
def index():
    return "API for Iot4safe"

@app.route('/datos',methods=['POST', 'GET'])
def datos():
    if request.method=='POST':
        content = request.get_json()
        geojson = {
                      "type": "Feature",
                      "geometry": {
                        "type": "Point",
                        "coordinates": [content["lon"], content["lat"]]
                      },
                      "properties": {"yaw": content["yaw"],
                                    "pitch": content["pit"],
                                    "roll": content["rol"],
                                    "altitude": content["alt"],
                                    "vehiculo": content["veh"],
                                    "timestamp": time.time()
                                    }
                    }

        dat_col.insert_one(geojson)
        return content

    elif request.method=='GET':
        result = dat_col.find_one(sort=[("_id", -1)])
        del result["_id"]
        response = jsonify(dict(result))
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/get_all', methods=["GET"])
def get_all():
    if request.method=='GET':
        result = list(dat_col.find({}))
        response = []
        for doc in result:
            del doc["_id"]
            response.append(doc)
        response = jsonify(response)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/charge', methods=["GET"])
def charge():
    if request.method=='GET':
        seconds = 60*30
        aux = time.time() - seconds
        result = list(dat_col.find({"properties.timestamp" : {"$gte":aux}}))
        response = []
        for doc in result:
            del doc["_id"]
            response.append(doc)
        response = jsonify(response)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/get_interval', methods=["GET"])
def get_interval():
    if request.method=='GET':
        fecha_ini = request.args.get("fecha_ini")
        fecha_fin = request.args.get("fecha_fin")
        fecha_ini = fecha_ini[:-3]
        fecha_fin = fecha_fin[:-3]
        result = list(dat_col.find({"$and" :[{"properties.timestamp":{"$gte":int(fecha_ini)}},{"properties.timestamp":{"$lte":int(fecha_fin)}} ]}))
        response = []
        for doc in result:
            del doc["_id"]
            response.append(doc)
        response = jsonify(response)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

if __name__ == ("__main__"):
    app.run(host='0.0.0.0',debug=True)
