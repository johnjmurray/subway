# add time step functionality
#   - iter_time goes at 1 min always

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


class Train:
    def __init__(self,start_time,start_station,exp_flag):
        self.start_time = start_time
        self.start_station = start_station
        self.route_counter = 0
        self.loc = [route_lats[self.route_counter], route_lons[self.route_counter]]
        self.exp_flag = exp_flag

    def move(self):
        if self.route_counter < len(route_lats)-1:
            self.route_counter+=1
            self.loc = [route_lats[self.route_counter], route_lons[self.route_counter]]
        else:
            self.loc = [0,0]


class Station:
    def __init__(self,name,lat,lon,exp_flag):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.exp = exp_flag

def add_train_to_current(t):
	current_trains[t] = train(t, flushing,0)


midnight = 0
zero_time = midnight
time_step = 1 # 6 seconds
iter_time = zero_time

# Station Names
station_names_south = ['Flushing - Main St.','Mets - Willets Pt.','111th St.','74th St. - Broadway','Woodside - 61st St.','Queensboro Plaza','Times Sq. - 42nd St.','34th St. - Hudson Yards']

# Station Locations
station_lats_south = [40.759605,40.754741,40.751662,40.746836,40.745669,40.750618,40.755988,40.755019]
station_lons_south = [-73.829954,-73.845686,-73.855323,-73.891225,-73.902816,-73.940214,-73.986967,-74.000943]

# Create train route by interpolation
route_lats = []
route_lons = []

# Times
trip_durations_south = [0,2,4,9,13,20,29,35]
start_times_south_str = ['12','26','40','1:00','1:20','1:40','2:00','2:20','2:40','3:00','3:20','3:40','4:00','4:20','4:35','4:47','4:58','5:10','5:20','5:30','5:38','5:44','5:50','5:56','6:01','6:06','6:10','6:14','6:18']
start_times_south = []
for t in start_times_south_str:
    if len(t) < 3:
        start_times_south.append(int(t))
    elif len(t) < 5:
        start_times_south.append(60*int(t[0])+int(t[2:4]))
    else:
        start_times_south.append(60*int(t[0:2])+int(t[3:5]))

# Interpolate pts between stations
for ii in range(1,len(station_lats_south)):
	station_1_lat = station_lats_south[ii-1]
	station_1_lon = station_lons_south[ii-1]
	station_2_lat = station_lats_south[ii]
	station_2_lon = station_lons_south[ii]
	for lat_iter in np.linspace(station_1_lat,station_2_lat,(trip_durations_south[ii]-trip_durations_south[ii-1])*(1/time_step)):
		route_lats.append(lat_iter)
	for lon_iter in np.linspace(station_1_lon,station_2_lon,(trip_durations_south[ii]-trip_durations_south[ii-1])*(1/time_step)):
		route_lons.append(lon_iter)

# Define stations
flushing = Station(station_names_south[0],station_lats_south[0],station_lons_south[0],1)
mets = Station(station_names_south[1],station_lats_south[1],station_lons_south[1],1)
st111 = Station(station_names_south[2],station_lats_south[2],station_lons_south[2],0)
bway = Station(station_names_south[3],station_lats_south[3],station_lons_south[3],0)
wood = Station(station_names_south[4],station_lats_south[4],station_lons_south[4],1)
qplz = Station(station_names_south[5],station_lats_south[5],station_lons_south[5],1)
tsq = Station(station_names_south[6],station_lats_south[6],station_lons_south[6],1)
hudson = Station(station_names_south[7],station_lats_south[7],station_lons_south[7],1)


def train_gen():
	"""Yield dictionary of currently operating trains per iteration."""
	iter_time = 0
	# Train instances are added to and removed from this dictionary over time.
	# This dictionary is passed on to the `animate` function.
	current_trains = {}
	while iter_time < start_times_south[-1] + trip_durations_south[-1]:
		for start_time in start_times_south:
			if iter_time >= start_time and iter_time < start_time+trip_durations_south[-1] and start_time not in current_trains:
				current_trains[start_time] = Train(start_time,flushing,0)
			elif iter_time > start_time+trip_durations_south[-1] and start_time in current_trains:
				del current_trains[start_time]
		yield current_trains
		iter_time += time_step
		print('{:02d}:{:02d}'.format(*divmod(iter_time, 60)))


fig = plt.figure()
ax = plt.axes(xlim=(-74.027,-73.761),ylim=(40.572,40.870))
scat = plt.scatter(0,0)
line, = ax.plot(route_lons, route_lats, lw=2)


def animate(current_trains):
	"""Set the data for one frame of the animation.

	Parameters
	----------
	current_trains: dictionary of `Train` instances.

	Returns
	-------
	Updated scatterplot.
	"""
	coords = []
	for train_ii in current_trains.values():
		this_x = train_ii.loc[1]
		this_y = train_ii.loc[0]
		coords.append((this_x, this_y))
		train_ii.move()
	if coords:
		scat.set_offsets(coords)
	return scat,


ani = animation.FuncAnimation(fig=fig, func=animate, frames=train_gen(), interval=200, blit=True)
plt.show()
