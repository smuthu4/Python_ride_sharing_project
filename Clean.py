import Connection
import Trips
import GraphHopperUtils

def clean_db():
    db,cursor = Connection.get_connection()
    cursor.execute("use ridesharing")
    cursor.execute("select * from trips")
    rows = cursor.fetchall()
    tripList=[]
    for row in rows:
    	trip=Trips.Trip(row[0],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13])
    	tripList.append(trip)
    for i in range(len(tripList)):
    	print "Cleaning " + str(i)
    	result = GraphHopperUtils.distance_for_a_destination(tripList[i].pickup_latitude,tripList[i].pickup_longitude,tripList[i].dropoff_latitude,tripList[i].dropoff_longitude)
    	if tripList[i].trip_distance == 0 or tripList[i].trip_time == 0:
    		query="update trips set trip_time=%s,trip_distance=%s,distance=%s,travel_time=%s where id=%s"%(result[1],result[0],result[0],result[1],tripList[i].trip_id)
    		cursor.execute(query)
    	else:
    		query="update trips set distance=%s,travel_time=%s where id=%s"%(result[0],result[1],tripList[i].trip_id)
    		cursor.execute(query)	
    print "Cleaned"
    Connection.close_connection(cursor,db)
clean_db()