import overpy
import pandas as pd
from geopy import distance
from datetime import datetime
pd.set_option('display.width', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)

def osm_rail(format, country, key, value, df_name):
	api = overpy.Overpass()
	railway = api.query(f"""[out:{format}][timeout:180];area[name='{country}'];nwr[{key}={value}](area);out center;""")
	list_of_data = []
	for way in railway.ways:
		temp = {'latitude': way.center_lat, 'longitude': way.center_lon, 'id': way.id}
		for key in way.tags.keys():
			temp[key] = way.tags[key]
		list_of_data.append(temp)
	data_frame = pd.DataFrame(list_of_data)
	data_frame.to_csv(df_name)

if __name__ == '__main__':
	start = datetime.now()
	# Just run for the first time
	# osm_rail("json", "Sverige", "railway", "rail", "sweden_railway.csv")
	# osm_rail("json", "Sverige", "railway", "narrow_gauge", "sweden_railway_narrow.csv")

	df = pd.read_csv("data.csv")
	osm = pd.read_csv("sweden_railway.csv", low_memory=False)
	osm = osm[osm['maxspeed'].notna()]
	osm = osm[['id', 'latitude', 'longitude', 'maxspeed']]

	df_point = []
	for i in range(len(df)):
		df_point.append((df["Lat"].iloc[i], df["Long"].iloc[i]))

	df["point"] = df_point
	osm_point = []
	for i in range(len(osm)):
		osm_point.append((osm["latitude"].iloc[i], osm["longitude"].iloc[i]))

	osm["point"] = osm_point

	min_distance = []
	max_speed = []
	id_list = []
	for i in range(len(df)):
		temp_list = []
		for j in range(len(osm)):
			point1 = df["point"].iloc[i]
			point2 = osm["point"].iloc[j]
			temp_list.append(distance.distance(point1, point2).km)
		min_distance.append(min(temp_list))
		max_speed.append(osm["maxspeed"].iloc[temp_list.index(min(temp_list))])
		id_list.append(osm["id"].iloc[temp_list.index(min(temp_list))])
		print(i) # the last i is 12604

	df['max_speed'] = max_speed
	df['distance'] = min_distance
	df['id_osm'] = id_list

	df.to_csv("final_df.csv")
	finish = datetime.now()
	operation = finish - start
	print("Operation Time in seconds =", operation.seconds)


