
import Connection
import csv
import datetime
import os
import GraphHopperUtils

db,cursor = Connection.get_connection()
dropdb_query = "drop database IF EXISTS ridesharing"
createdb_query = "create database IF NOT EXISTS ridesharing"
usedb_query = "use ridesharing"
droptable_query = "drop table IF EXISTS trips"
table_query = """create table IF NOT EXISTS trips (id int not null auto_increment primary key, trip_id int not null, trip_date date, pickup_time time,
              dropoff_time time, trip_time int, trip_distance float, pickup_lat varchar(15), pickup_long varchar(15), dropoff_lat varchar(15),
              dropoff_long varchar(15), passengers int, distance float, travel_time int)"""
cursor.execute(dropdb_query)
cursor.execute(createdb_query)
cursor.execute(usedb_query)
cursor.execute(droptable_query)
cursor.execute(table_query)
cursor.execute("use ridesharing")

curr_dir = os.getcwd()
#file_list = ["trip_data_1.csv","trip_data_2.csv","trip_data_3.csv","trip_data_4.csv","trip_data_5.csv","trip_data_6.csv","trip_data_7.csv","trip_data_8.csv","trip_data_9.csv","trip_data_10.csv","trip_data_11.csv","trip_data_12.csv"]
file_list = ["trip_data_1.csv"]
insert_count = 0
for file_name in file_list:
    rowCount = 0
    csv_data = csv.reader(open(curr_dir+"/CSVData/"+file_name))
    for data in csv_data:
        if rowCount > 0:
            if float(data[10]) != 0 and float(data[11]) != 0:
                result = GraphHopperUtils.distance_for_a_destination(data[11], data[10], 40.644104, -73.782665)
                if result[0] <= 4 and result[0] > 0:
                    try:
                        trip_id = int(data[0])
                        pickup_time = datetime.datetime.strptime(data[5], "%Y-%m-%d %H:%M:%S")
                        drop_time = datetime.datetime.strptime(data[6], "%Y-%m-%d %H:%M:%S")
                        trip_time = int(data[8])
                        trip_distance = float(data[9])
                        pickup_latitude = float(data[13])
                        pickup_longitude = float(data[12])
                        passengers = int(data[7])
                        sql = "insert into trips (trip_id, trip_date, pickup_time, dropoff_time, trip_time, trip_distance, pickup_lat, pickup_long, dropoff_lat, dropoff_long, passengers, distance, travel_time) values (%s, '%s', '%s', '%s', %s, %s, '40.644104', '-73.782665', '%s', '%s', %s, %s, %s)" % (trip_id, pickup_time.date().strftime("%Y-%m-%d"), pickup_time.time().strftime("%H:%M:%S"), drop_time.time().strftime("%H:%M:%S"), trip_time, trip_distance, pickup_latitude, pickup_longitude, passengers, result[0], result[1])
                        if passengers <=3:
                            insert_count+=1
                            cursor.execute(sql)
                    except:
                        pass                 
        rowCount=rowCount+1
Connection.close_connection(cursor,db)