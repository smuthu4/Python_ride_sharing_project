import Connection
import datetime
import Graph

class Trip:
	def __init__(self, trip_id, trip_date, pickup_time, dropoff_time, trip_time, trip_distance, pickup_latitude,pickup_longitude, dropoff_latitude, dropoff_longitude, passengers, distance, travel_time):
		self.trip_id = int(trip_id)
		self.trip_date = trip_date
		self.pickup_time = pickup_time
		self.pickup_time = datetime.datetime.strptime(str(self.pickup_time),"%H:%M:%S")
		self.pickup_time = datetime.datetime.strftime(self.pickup_time,"%H:%M:%S")
		self.dropoff_time = dropoff_time
		self.dropoff_time = datetime.datetime.strptime(str(self.dropoff_time),"%H:%M:%S")
		self.dropoff_time = datetime.datetime.strftime(self.dropoff_time,"%H:%M:%S")
		self.trip_time = int(trip_time)
		self.trip_distance = trip_distance
		self.pickup_latitude = pickup_latitude
		self.pickup_longitude = pickup_longitude
		self.dropoff_latitude = dropoff_latitude
		self.dropoff_longitude = dropoff_longitude
		self.passengers = int(passengers)
		self.distance = distance
		self.travel_time = int(travel_time)

def get_all(size):
	print "Establishing connection to the database..."
	db,cursor = Connection.get_connection()
	print "Connection established."
	print "Fetching records from database..."
	cursor.execute("use ridesharing")
	tripList=[]
	for i in range(31):
		start=0
		stop=size+start
		get=True
		start_date = datetime.datetime.strptime("2013-01-01", "%Y-%m-%d")
		start_date = start_date + datetime.timedelta(days=i)
		start_date = datetime.datetime.strftime(start_date.date(), "%Y-%m-%d")
		start_time = "00:00:00"
		end_time = datetime.timedelta(0,stop)
		end_time = datetime.datetime.strptime(str(end_time),"%H:%M:%S")
		end_time = datetime.datetime.strftime(end_time,"%H:%M:%S")
		while get == True:
			window_trip_list=[]
			query = "select * from trips where trip_date='%s' and pickup_time between '%s' and '%s' order by distance desc"%(start_date,start_time,end_time)
			cursor.execute(query)
			result = cursor.fetchall()
			for row in result:
				trip=Trip(row[0],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13])
				window_trip_list.append(trip)	
			tripList.append(window_trip_list)		
			start = stop+1	
			if start < 86400:
				start_time=datetime.timedelta(0,start)
				start_time = datetime.datetime.strptime(str(start_time),"%H:%M:%S")
				start_time = datetime.datetime.strftime(start_time,"%H:%M:%S")
			else:
				get=False
			if start+size < 86400:
				stop = start+size
			else:
				stop = 86399
			if stop < 86400:
				end_time = datetime.timedelta(0,stop)
				end_time = datetime.datetime.strptime(str(end_time),"%H:%M:%S")
				end_time = datetime.datetime.strftime(end_time,"%H:%M:%S")
	total_trips = 0
	for trip_set in tripList:
		total_trips+=len(trip_set)

	print str(total_trips) + " individual trips were found in the database."	
	Graph.create_graph(tripList)
