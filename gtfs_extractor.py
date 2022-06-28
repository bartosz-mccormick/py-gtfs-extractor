import os
import pandas as pd
import geopandas as gpd

# START SET UP

## define study area
### study area must be a geopandas dataframe with at least 1 polygon
### note: geopandas is really flexible with support for different file types (.shp, .geojson, etc...)

study_area_path = "<path to geometry of study area>"

study_area = gpd.read_file(study_area_path)

### optional: may need to specify a CRS, check that it's correct by calling 'study_area.crs'
#study_area.crs = 'epsg:25832' 

## GTFS feed path
### (feed you're extracting from)
### path must be to an UNZIPPED feed!
gtfs_feed = "<path to feed>"

## specify path for output
output_path = "<output folder path>"

## name for the output GTFS feed
gtfs_feed_name = "GTFS_extracted"

# END SET UP



# create output folders if they don't exist
if not os.path.exists(output_path+'/'+gtfs_feed_name):
    os.makedirs(output_path+'/'+gtfs_feed_name)

# reproject datum to WGS84 (used by GTFS data)
study_area = study_area.to_crs("epsg:4326") 


# STOPS
print(gtfs_feed_name+": "+'[1/8] Processing stops file...')
## Opens stops file.
stops = pd.read_csv(gtfs_feed + "/stops.txt")

## convert to geopandas object with point geometry
stops_geo = gpd.GeoDataFrame(stops, geometry = gpd.points_from_xy(stops.stop_lon,stops.stop_lat))
stops_geo.crs = "epsg:4326"

## clip stops within study area
study_area_stops = gpd.clip(stops_geo,study_area)
stops_extracted = pd.DataFrame(study_area_stops.drop(columns = "geometry"))  

## Creates set of unique stop IDs.
stop_id_set = set(stops_extracted.stop_id.values)

## Writes new stops file to text file.
stops_extracted.to_csv(output_path + '/' + gtfs_feed_name +'/stops.txt', index = False)

# STOP_TIMES
print(gtfs_feed_name+": "+'[2/8] Processing stop_times file...')
## Opens stop_times.txt file.
stop_times = pd.read_csv(gtfs_feed + "/stop_times.txt")

## filter stop_times at extracted stop_ids
stop_times_extracted = stop_times.query("stop_id in @stop_id_set")

## Creates set of unique trip IDs.
trip_ids_set = set(stop_times_extracted.trip_id.values)

## Writes new stop_times file to text file.
stop_times_extracted.to_csv(output_path + '/' + gtfs_feed_name +'/stop_times.txt', index = False)

# TRIPS
print(gtfs_feed_name+": "+'[3/8] Processing trips file...')

trips = pd.read_csv(gtfs_feed + "/trips.txt")
trips_extracted = trips.query("trip_id in @trip_ids_set")

## Creates set of unique route / service IDs.
route_ids_set = set(trips_extracted.route_id.values)
service_ids_set = set(trips_extracted.service_id.values)

# Writes new trips file to text file.
trips_extracted.to_csv(output_path + '/' + gtfs_feed_name +'/trips.txt', index = False)

# ROUTES
print(gtfs_feed_name+": "+'[4/8] Processing routes file...')
## Opens routes file.
routes = pd.read_csv(gtfs_feed + "/routes.txt")
routes_extracted = routes.query("route_id in @route_ids_set")

## Creates set of unique agency IDs.
agency_ids_set = set(routes_extracted.agency_id.values)

## Writes new routes file to text file.
routes_extracted.to_csv(output_path + '/' + gtfs_feed_name +'/routes.txt', index = False)


# AGENCY
print(gtfs_feed_name+": "+'[5/8] Processing agency file...')
## Opens agency file.
agency = pd.read_csv(gtfs_feed + "/agency.txt")

## Extracts relevant items from agency file.
agency_extracted = agency.query("agency_id in @agency_ids_set")

## Writes new agency file to text file.
agency_extracted.to_csv(output_path + '/' + gtfs_feed_name +'/agency.txt', index = False)

# CALENDAR
print(gtfs_feed_name+": "+'[6/8] Processing calendar file...')
## Opens calendar file.
calendar = pd.read_csv(gtfs_feed + "/calendar.txt")

## Extracts relevant items from calendar file.
calendar_extracted = calendar.query("service_id in @service_ids_set")

## Writes new calendar file to text file.
calendar_extracted.to_csv(output_path + '/' + gtfs_feed_name +'/calendar.txt', index = False)

# CALENDAR_DATES
print(gtfs_feed_name+": "+'[7/8] Processing calendar_dates file...')
## Opens calendar_dates file.
calendar_dates = pd.read_csv(gtfs_feed + "/calendar_dates.txt")

## Extracts relevant items from calendar_dates file.
calendar_dates_extracted = calendar_dates.query("service_id in @service_ids_set")

## Writes new calendar_dates file to text file.
calendar_dates_extracted.to_csv(output_path + '/' + gtfs_feed_name +'/calendar_dates.txt', index = False)

# # FEED_INFO
# print(gtfs_feed_name+": "+'[8/8] Processing feed_info file...')
# ## Opens feed_info file.
# feed_info = pd.read_csv(gtfs_feed + "/feed_info.txt")

# ## Writes new feed_info file to text file.
# feed_info.to_csv(output_path + '/' + gtfs_feed_name +'/feed_info.txt', index = False)

print('')
print(gtfs_feed_name+": "+'Process complete!')


