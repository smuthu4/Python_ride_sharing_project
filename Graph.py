import networkx as nx
import GraphHopperUtils
import math
def create_graph(tripList):
	print "Merging..."
	merged_history = {}
	merged_trip_id_list = []
	merged_trip_list = []
	total_trips = 0
	for i in range(len(tripList)):
	#for i in range(1):
		trip_set = tripList[i]
		total_trips+=len(trip_set)
		merged_trip_id_set = []
		merged_trip_set = []
		for j in range(len(trip_set)):
			merged_trip_id = []
			merged_trip = []
			shouldAppend = False  
			if trip_set[j].trip_id not in merged_history:
				first_add = True
				trip_id = 0
				existing_passengers = trip_set[j].passengers
				previous_trip = trip_set[j]
				previous_trip_id = trip_set[j].trip_id
				isContinue = True
				while existing_passengers < 4 and isContinue == True:
					gain = 0.0
					for k in range(len(trip_set)):
						if (trip_set[k].trip_id not in merged_history) and (trip_set[k].trip_id != previous_trip_id):
							if (existing_passengers + trip_set[k].passengers) > 4:
								pass
							else:
								new_gain = distance_gain(previous_trip,trip_set[k])
								if new_gain > gain and new_gain < 1:
									gain=new_gain
									trip = trip_set[k]
									trip_id = trip.trip_id							
					if gain != 0.0:
						shouldAppend = True
						if first_add == True:
							merged_history[previous_trip_id] = previous_trip_id
							merged_trip_id.append(previous_trip_id)
							merged_trip.append(previous_trip)
							first_add = False
						merged_history[trip_id] = trip_id
						previous_trip = trip
						previous_trip_id = 	trip_id
						merged_trip_id.append(trip_id)
						merged_trip.append(trip)
						existing_passengers = existing_passengers + trip.passengers
					else:
						isContinue = False				
			if shouldAppend == True: 
				merged_trip_id_set.append(merged_trip_id)
				merged_trip_set.append(merged_trip)		
		merged_trip_id_list.append(merged_trip_id_set)
		merged_trip_list.append(merged_trip_set)
	merged_trips_count=0
	lone_trips_count = 0
	lone_trips_distance = 0
	for trip_set in merged_trip_id_list:
		merged_trips_count+=len(trip_set)
	total_original_distance = 0;
	for i in range(len(tripList)):
	#for i in range(1):
		for trips in tripList[i]:
			total_original_distance+=trips.distance
			if trips.trip_id not in merged_history:
				lone_trips_count+=1
				lone_trips_distance+=trips.distance				
	print "Now we have " + str(merged_trips_count + lone_trips_count) + " trips after merging."
	print str(lone_trips_count) + " trips are unmerged"
	print "Calculating cost saved..."
	print str(total_original_distance) + " miles was travelled by the taxis before merging"
	total_original_cost = total_original_distance + (total_trips * 0.25)
	print "Total original cost: $" + str(total_original_cost)
	print "No Walking"
	print "----------"
	data = estimate_cost_saved(merged_trip_list)
	print "After merging, the taxis will have to travel " + str(data[0] + lone_trips_distance) + " miles."			
	print "Total cost after merging :$" + str(data[1] + (lone_trips_distance + (lone_trips_count * 0.25)))

	print "With Walking"
	print "------------"
	optimize_path(merged_trip_list)
	data = estimate_cost_saved(merged_trip_list)
	print "After merging, the taxis will have to travel " + str(data[0] + lone_trips_distance) + " miles."			
	print "Total cost after merging :$" + str(data[1] + (lone_trips_distance + (lone_trips_count * 0.25)))

def distance_gain(first_trip,second_trip):
	result = GraphHopperUtils.distance_for_multiple_destinations(40.644104, -73.782665, first_trip.dropoff_latitude,first_trip.dropoff_longitude,second_trip.dropoff_latitude,second_trip.dropoff_longitude)
	first_distance = first_trip.distance
	second_distance = second_trip.distance
	new_distance = result[0]
	gain = float((first_distance + second_distance - new_distance)/(first_distance + second_distance))
	return gain

def estimate_cost_saved(merged_trip_list):
	total_merged_trip_cost = 0
	total_merged_trip_distance = 0
	for merged_trip_set in merged_trip_list:
		for trips in merged_trip_set:
			merged_trip_cost = 0
			total_individual_distance = 0
			coordinates = (40.644104, -73.782665)
			for trip in trips:
				total_individual_distance+=trip.distance
				coordinates = coordinates + (trip.dropoff_latitude,trip.dropoff_longitude) 
			result = GraphHopperUtils.distance_from_jfk(coordinates)
			merged_trip_distance = result[0]
			total_merged_trip_distance+=merged_trip_distance
			fraction = merged_trip_distance/total_individual_distance
			for trip in trips:
				merged_trip_cost+=(fraction*trip.distance) + 0.5
			total_merged_trip_cost+=merged_trip_cost
	return [total_merged_trip_distance,total_merged_trip_cost]		

def optimize_path(merged_trip_list):
	result = []
	for merged_trip_set in merged_trip_list:
		for trips in merged_trip_set:
			total_individual_distance = 0
			coordinates = (40.644104, -73.782665)
			for trip in trips:
				total_individual_distance+=trip.distance
				coordinates = coordinates + (trip.dropoff_latitude,trip.dropoff_longitude) 
			result = GraphHopperUtils.distance_from_jfk(coordinates)
			merged_trip_distance = result[0]
			source = (40.644104, -73.782665)
			reversed_trips = list(reversed(trips))
			for id, trip in enumerate(reversed_trips):
				coordinates = source
				coordinates = coordinates + (trip.dropoff_latitude,trip.dropoff_longitude)
				result = GraphHopperUtils.get_coordinates(coordinates)
				if "coordinates" in result:
					reversed_coordinates = list(reversed(result["coordinates"]))
					for i in range(len(reversed_coordinates)): 
						intersection_coordinate = tuple([reversed_coordinates[i][1],reversed_coordinates[i][0]])
						intermediate_coordinate = intersection_coordinate + (trip.dropoff_latitude,trip.dropoff_longitude)
						intermediate_result = GraphHopperUtils.distance_from_source(intermediate_coordinate)
						distance = intermediate_result[0]																																																		
						if(distance < 0.26):
							if (id+1 == len(reversed_trips)):
								trip.dropoff_latitude = intersection_coordinate[0]
								trip.dropoff_longitude = intersection_coordinate[1]
							else:	
								for i in range(id+1,len(reversed_trips)):
									coordinates = coordinates + (reversed_trips[i].dropoff_latitude,reversed_trips[i].dropoff_longitude)
								result = GraphHopperUtils.distance_from_jfk(coordinates)
								reroute_distance = result[0]
								if reroute_distance < merged_trip_distance:
									trip.dropoff_latitude = intersection_coordinate[0]
									trip.dropoff_longitude = intersection_coordinate[1]
						else:
							break			
						source = (trip.dropoff_latitude,trip.dropoff_longitude)

