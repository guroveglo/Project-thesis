from math import dist
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd


def save_coastal_data(path,resolution='f'):

    m = Basemap(projection='robin',lon_0=0,resolution=resolution)

    coast = m.drawcoastlines()

    coordinates = np.vstack(coast.get_segments())
    lons,lats = m(coordinates[:,0],coordinates[:,1],inverse=True)

    D = {'lons':lons,'lats':lats}

    np.save(os.path.join(path,'coastal_basemap_data.npy'),D)

def get_ais_distances(ais_path, coast_data_path):
    df = pd.read_csv(ais_path, sep=";", decimal=".")
    #fig = plt.figure()
    #plt.title('r_cpa vs dist_to_shore')
    #plt.xlabel('r cpa')
    #plt.ylabel('mean length ')
    
    for index, row in df.iterrows():
        if row['dataset'] == 'encs_west':
            own_mmsi = row['own_mmsi']
            obst_mmsi = row['obst_mmsi']
            
            lon_man = row['lon_maneuver']
            lat_man = row['lat_maneuver']
            colreg_type = row['COLREG']
            #print('own_mmsi: ', own_mmsi, 'obst_mmsi: ', obst_mmsi, ' lon_man: ', lon_man, ' lat_man: ', lat_man, ' colreg_type: ', colreg_type )
            dist_to_coast = distance_from_coast(lon_man,lat_man,coast_data_path,degree_in_km=111.1)
            #print(dist_to_coast)
            dists = []
            dists.append(dist_to_coast) # could try to use dict instead! connecting r_cpa to distance 
            colreg_dict = {
                -2.0: [], 
                3.0: [], 
                -1.0: []
            }
            colreg_dict[colreg_type].insert(0, dist_to_coast)

            r_cpa = row['r_cpa']

    df['dist_to_coast'] = dists     # as per now it overwrites, and only uses the last element in the csv // NOW it says that ValueError: Length of values (1) does not match length of index (34912)
        #if row['dataset'] == 'encs_west':
            #plt.scatter(r_cpa, dist_to_coast, alpha=0.5, c ='#FF5733')
        #print(dist_to_coast)
   
    #df.to_csv("new_csv.csv", index = False)

# Get distance for all ais data in file
def distance_from_coast(lon,lat,coast_data_path,degree_in_km=111.12):
    D = np.load(coast_data_path, allow_pickle = True).tolist()
    lons,lats = D['lons'],D['lats']
    dists = np.sqrt((lons-lon)**2+(lats-lat)**2)
    min_dist = np.min(dists)*degree_in_km
    return min_dist

# Plot all ais cases 
def plot_all_ais_cases(ais_data_path, coast_data_path):

    df = pd.read_csv(ais_data_path, sep=";", decimal=".")

    dist_to_land = []
    
    for index, row in df.iterrows():
        own_mmsi = row['own_mmsi']
        obst_mmsi = row['obst_mmsi']
        # Lon and lat of own 
        lon_man = row['lon_maneuver']
        lat_man = row['lat_maneuver']
        dist_to_coast = distance_from_coast(lon_man,lat_man,coast_data_path,degree_in_km=111.1)

        print('own_mmsi: ', own_mmsi, 'obst_mmsi: ', obst_mmsi, ' lon_man: ', lon_man, ' lat_man: ', lat_man)
        print('Closest distance to shore: ', dist_to_coast)
        
        # Plot map
        m = Basemap(projection='gnom', resolution='h', area_thresh=0.01, lat_0=lat_man, lon_0=lon_man, width=2E4, height=2E4)
        m.drawmapboundary(fill_color='#A5D7D7')
        m.fillcontinents(color='#EFEFDB')
        m.scatter(lon_man, lat_man, latlon=True, alpha=0.5, c='#F08585')
        plt.title('Own_mmsi: ' + str(own_mmsi) + ' - Obst_mmsi: ' + str(obst_mmsi))
        plt.xlabel( 'Min distance to shore: ' + str(dist_to_coast))
        plt.show()
           
    

if __name__ == '__main__':

    #Define path
    path = 'Data/'

    #Run only one time to save the data. Will cost less time
    #save_coastal_data(path,resolution='h')  
    print("Adding dists to csv: ")
    get_ais_distances(os.path.join(path,'classified.csv'), os.path.join(path,'coastal_basemap_data.npy'))

    #plot_all_ais_cases(os.path.join(path,'classified.csv'), os.path.join(path,'coastal_basemap_data.npy'))


