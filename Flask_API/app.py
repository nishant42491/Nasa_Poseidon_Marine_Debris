from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import math
import ast
app = Flask(__name__)
api = Api(app)


def getDistance(lat1,lon1,lat2,lon2):
  R = 6373.0
  lat1 = math.radians(lat1)
  lon1 = math.radians(lon1)
  lat2 = math.radians(lat2)
  lon2 = math.radians(lon2)

  dlon = lon2 - lon1
  dlat = lat2 - lat1

  # Haversine Formula
  a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
  distance = R * c

  return round(distance,5)


class Pins(Resource):
    def get(self):
        data = pd.read_csv('../Final_Datset_Mss_Anomaly.csv')  # read CSV
        data = data.to_dict()  # convert dataframe to dictionary
        return {'data' :data},200


class NearestDistance(Resource):
    def post(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('lat', required=True)  # add args
        parser.add_argument('long', required=True)

        args = parser.parse_args()  # parse arguments to dictionary
        distances =50000000
        index1 =-1
        input_latitude = float(args['lat'])
        input_long = float(args['long'])

        print(input_latitude)
        print(input_long)
        df = pd.read_csv('modified.csv')
        for index, row in df.iterrows():
            wind_long = row['longitude']
            wind_lat = row['Latittude']

            dist = getDistance(wind_lat,wind_long,input_latitude,input_long)
            if (dist <distances):
                distances = dist
                index1 = index

        print(df.iloc[index1])
        send_data = {
            'longitude' : df.iloc[index1]['longitude'],
            'latitude' :df.iloc[index1]['Latittude'],
            'mss_p' :df.iloc[index1]['mss_p'],
            'mss_anom' : df.iloc[index1]['mss_anom'],
            'mss_anom_scaled' :df.iloc[index1]['mss_anom_scaled'],
            'pressure' : df.iloc[index1]['pressure'],
            'humidity' :df.iloc[index1]['humidity'],
            'wind_speed' :df.iloc[index1]['wind_speed'],
            'temperature' :df.iloc[index1]['temperature']
        }
        return {'data' :send_data},200


api.add_resource(Pins, '/pins')
api.add_resource(NearestDistance,'/distance')
if __name__ == '__main__':
    app.run()  # run our Flask app
