import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["IoT4safedb"]

gps_col = mydb["gps"]
imu_col = mydb["imu"]

gps_data={"latitud": 1, "longitud": 2, "latitud": 3}
imu_data={"yaw": 4, "pitch": 5, "roll": 6}

gps_col.insert_one(gps_data)
imu_col.insert_one(imu_data)

print(myclient.list_database_names())
