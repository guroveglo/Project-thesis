
import scipy.stats as stat
import pandas as pd
import csv
import numpy as np
import os
import matplotlib.pyplot as plt
from math import sqrt, cos, sin
from filter_data import HO_south, CRGW_south, OTGW_south, HO_west, CRGW_west, OTGW_west

# not clustered yet

#HO_clustered = pd.read_csv('HO_south.csv', sep=';', decimal='.')
#OTGW_clustered = pd.read_csv('OTGW_south.csv', sep=';', decimal='.')
#CRGW_clustered = pd.read_csv('CRGW_south.csv', sep=';', decimal='.')

def obstacleManeuver(data, parameters):
    man_obst = pd.DataFrame(data.loc[data['maneuver_made_obst'] == True])
    no_man_obst = pd.DataFrame(data.loc[data['maneuver_made_obst'] == False])
    man_obst['length_ratio'] = man_obst['own_length']/man_obst['obst_length']
    no_man_obst['length_ratio'] = no_man_obst['own_length']/no_man_obst['obst_length']
    data['length_ratio'] = data['own_length']/data['obst_length']

    plt.figure()
    plt.hist(no_man_obst['length_ratio'])
    plt.figure()
    plt.hist(man_obst['length_ratio'])
    plt.show()

    input((man_obst[parameters]).describe())
    input((no_man_obst[parameters]).describe())
    fig = plt.figure()
    plt.scatter(man_obst['length_ratio'], man_obst['r_maneuver_own'])
    fig = plt.figure()
    plt.scatter(no_man_obst['length_ratio'], no_man_obst['r_maneuver_own'])
    fig = plt.figure()
    plt.scatter(data['length_ratio'], data['r_maneuver_own'])
    plt.show()
    fig = plt.figure()
    plt.scatter(man_obst['length_ratio'], man_obst['delta_course_own'])
    fig = plt.figure()
    plt.scatter(no_man_obst['length_ratio'], no_man_obst['delta_course_own'])
    fig = plt.figure()
    plt.scatter(data['length_ratio'], data['delta_course_own'])
    plt.show()
    fig = plt.figure()
    plt.hist(man_obst['length_ratio'])
    fig = plt.figure()
    plt.hist(no_man_obst['length_ratio'])
    plt.show()

def distance_from_coast(lon,lat,coast_data_path,degree_in_km=111.12):
    D = np.load(coast_data_path, allow_pickle = True).tolist()
    lons,lats = D['lons'],D['lats']
    dists = np.sqrt((lons-lon)**2+(lats-lat)**2)
    min_dist = np.min(dists)*degree_in_km
    return min_dist


def lengthsAndDistances(data, coast_data_path):
    own_lengths = data['own_length'] # every row in this column 
    obst_lengths = data['obst_length'] 
    r_cpa = data['r_cpa']
    r_maneuver = data['r_maneuver_own']
    length_ratio = obst_lengths/own_lengths
    mean_length = (obst_lengths+own_lengths)/2
    #print('Correlation r_cpa and mean length ' + str(stat.spearmanr(r_cpa, mean_length)))
    #print('Correlation r_maneuver and mean length ' + str(stat.spearmanr(r_maneuver, mean_length)))
    #print('Correlation r_cpa and length_ratio ' + str(stat.spearmanr(r_cpa, length_ratio)))
    #print('Correlation r_maneuver and length_ratio ' + str(stat.spearmanr(r_maneuver, length_ratio)))
    #print('Correlation r_cpa and own length ' + str(stat.spearmanr(r_cpa, own_lengths)))
    #print('Correlation r_cpa and obst length ' + str(stat.spearmanr(r_cpa, obst_lengths)))
    speed_own = data['own_speed']
    speed_obst = data['obst_speed']
    
    #relative_speed_own = np.sqrt((speed_obst*np.cos(contact_angle)- speed_own)**2 + (speed_obst*np.sin(contact_angle))**2 )  #MAKE THIS WORK (maybe by using a loop instead of numpy)
    #dists_to_shore = data['dist_to_coast']
    #obs vi har mange arrays vi opererer på 
    rel_speeds = []
    dists = []
    cpas = []
    mans = []
    for index, row in data.iterrows():
        v_own = row['own_speed']
        v_obst = row['obst_speed']
        rel_b_cpa = row['beta_cpa']
        relative_speed_cpa = sqrt(v_own**2 + v_obst**2 - 2*v_own*v_obst*cos(rel_b_cpa))
        rel_speeds.append(relative_speed_cpa)
        
        lon_man = row['lon_maneuver']
        lat_man = row['lat_maneuver']
        
        #print('own_mmsi: ', own_mmsi, 'obst_mmsi: ', obst_mmsi, ' lon_man: ', lon_man, ' lat_man: ', lat_man, ' colreg_type: ', colreg_type )
        dist_to_coast = distance_from_coast(lon_man,lat_man,coast_data_path,degree_in_km=111.1)
        if(dist_to_coast < 30):# we want to remove the outliers 
            dists.append(dist_to_coast)
            cpas.append(row['r_cpa'])
            mans.append(row['r_maneuver_own'])

    #Plotting
    print('Correlation r_cpa and dists ' + str(stat.spearmanr(r_cpa, rel_speeds)))

    fig = plt.figure()
    plt.title('r_cpa vs distance to coast')
    plt.xlabel('r cpa')
    plt.ylabel('r_maneuver vs distance to coast')
    #plt.scatter(r_cpa, dists, alpha=0.5, c ='#EA3245')
    plt.scatter(cpas, dists, alpha=0.5, c ='#EA3245')

    fig = plt.figure()
    #plt.scatter(r_maneuver, dists, alpha=0.5, c='#24C459')
    plt.scatter(mans, dists, alpha=0.5, c='#24C459')

    plt.title('distance to coast')
    plt.xlabel('r maneuver')
    plt.ylabel('distance to coast')

    plt.show()

def try_(namefile):
    #types = {'own_name' : 'str','obst_name' : 'str','date_cpa' : 'str','start_idx': np.int32,'stop_idx': np.int32,'case' : 'str','img_name' : 'str','img_class' : 'str', 'COLREG': np.float64,'own_length': np.float64,'obst_length': np.float32, 'own_type': np.float32,'obst_type': np.float32,'own_nav_status': np.float32,'obst_nav_status': np.float32,'own_speed': np.float32,'obst_speed': np.float32,'maneuver_index_own': np.float32,'r_maneuver_own': np.float32,'pre_man_dist_own': np.float32,'post_man_dist_own': np.float32,'delta_speed_own': np.float32,'delta_course_own': np.float32,'alpha_start': np.float32,'beta_start': np.float32,'r_cpa': np.float32,'alpha_cpa': np.float32,'beta_cpa': np.float32, 'dist_to_coast': np.float32}
    #n = {'n_ships','own_mmsi','obst_mmsi','own_name','obst_name','own_callsign','obst_callsign','own_length','obst_length','own_width','obst_width','own_type','obst_type','own_nav_status','obst_nav_status','own_speed','obst_speed','multi_man_own','maneuver_made_own','maneuver_index_own','maneuver_stop_idx_own','r_maneuver_own','pre_man_dist_own','pre_man_t_cpa_own','post_man_dist_own','post_man_t_cpa_own','delta_speed_own','delta_course_own','multi_man_obst','maneuver_made_obst','maneuver_index_obst','maneuver_stop_idx_obst','r_maneuver_obst','pre_man_dist_obst','pre_man_t_cpa_obst','post_man_dist_obst','post_man_t_cpa_obst','delta_speed_obst','delta_course_obst','alpha_start','beta_start','r_cpa','alpha_cpa','beta_cpa','lon_maneuver','lat_maneuver','COLREG','single_COLREG_type','time','date_cpa','cpa_idx','start_idx','stop_idx','case','dataset','COLREGS_not_filt','COLREGS_filt','img_name','img_class','dist_to_coast'}
    #data = pd.read_csv(namefile,  sep=";", decimal=".", header=None, names = n)
    #input(data)
    #HO = 3
    # HO_df = data.loc[(data['COLREG'] == HO)]

    with open(namefile, 'r') as file:
        read = file.read()
    #txt file to a list of list. Inner list means each hunk lines. Outer list means different hunks:
    records = [list(map(str.strip, line.strip().split('\n'))) for line in read.split('\n\n')]
    data = []
    
    
            
    

def dist_to_coast(namefile):

    with open(namefile, 'r') as infile:
        reader = csv.DictReader(infile)
        data = {}
        for row in reader:
            #print('row: {}'.format(row))
            for header, value in row.items():
                try:
                    data[header].append(value)
                except KeyError:
                    data[header] = [value]
    df = data
    HO = 3  # Head on situation
    #we have all data in data, a dict
    r_cpas = []
    r_mans = []
    dists = []
    #for (key, value) in data.items():
       # if (key == 'COLREG' and value)
   #if data['COLREG'] == HO and data['dataset'] == 'encs_west':

    #HO_df = data.loc[(data['COLREG'] == HO)]
    #HO_west = HO_df.loc[HO_df['dataset'] == 'encs_west']

    r_cpas = data['r_cpa']
    r_mans = HO_west['r_maneuver_own']
    dists = HO_west['dist_to_coast']

    #Plotting
    print('Correlation r_cpa and dist_to_coast ' + str(stat.spearmanr(r_cpas, dists)))

    fig = plt.figure()
    plt.title('r_cpa vs relative dist_to_coast ')
    plt.xlabel('r cpa')
    plt.ylabel('relative speed ')
    plt.scatter(r_cpas, dists , alpha=0.5, c ='#EA3245')

    fig = plt.figure()
    plt.scatter(r_mans, dists , alpha=0.5, c='#24C459')
    plt.title('r_maneuver vs dist_to_coast ')
    plt.xlabel('r maneuver')
    plt.ylabel('relative speed')

    plt.show()

def distance_from_coast(lon,lat,coast_data_path,degree_in_km=111.12):
    D = np.load(coast_data_path, allow_pickle = True).tolist()
    lons,lats = D['lons'],D['lats']
    dists = np.sqrt((lons-lon)**2+(lats-lat)**2)
    min_dist = np.min(dists)*degree_in_km
    return min_dist

def find_dist_to_coast_corr(df):
    for index, row in df.iterrows():
        own_mmsi = row['own_mmsi']
        obst_mmsi = row['obst_mmsi']
        lon_man = row['lon_maneuver']
        lat_man = row['lat_maneuver']
        colreg_type = row['COLREG']
        #print('own_mmsi: ', own_mmsi, 'obst_mmsi: ', obst_mmsi, ' lon_man: ', lon_man, ' lat_man: ', lat_man, ' colreg_type: ', colreg_type )
        dist_to_coast = distance_from_coast(lon_man,lat_man,coast_data_path,degree_in_km=111.1)
        print(dist_to_coast)
        colreg_dict = {
            -2.0: [], 
            3.0: [], 
            -1.0: []
        }
        colreg_dict[colreg_type].insert(0, dist_to_coast)

        r_cpa = row['r_cpa']


    

def poseStartVsParam(data, param):
    alpha_start = data['alpha_start']
    beta_start = data['beta_start']
    params = data[param]

    print('Correlation between alpha_start and ' + param + ' : ' + str(stat.spearmanr(alpha_start, params)))
    print('Correlation between beta_start and ' + param + ' : ' + str(stat.spearmanr(beta_start, params)))
    fig = plt.figure()
    plt.title(param + ' vs ' + 'alpha_start')
    plt.xlabel('alpha_start')
    plt.ylabel(param)
    plt.scatter(alpha_start, params)
    fig = plt.figure()
    plt.title(param + ' vs ' + 'beta_start')
    plt.xlabel('beta_start')
    plt.ylabel(param)
    plt.scatter(beta_start, params)
    plt.show()

def lengthVsParam(data, param):
    lwngth = data['alpha_start']
    beta_start = data['beta_start']
    params = data[param]

    print('Correlation between alpha_start and ' + param + ' : ' + str(stat.spearmanr(alpha_start, params)))
    print('Correlation between beta_start and ' + param + ' : ' + str(stat.spearmanr(beta_start, params)))
    fig = plt.figure()
    plt.title(param + ' vs ' + 'alpha_start')
    plt.xlabel('alpha_start')
    plt.ylabel(param)
    plt.scatter(alpha_start, params)
    fig = plt.figure()
    plt.title(param + ' vs ' + 'beta_start')
    plt.xlabel('beta_start')
    plt.ylabel(param)
    plt.scatter(beta_start, params)
    plt.show()

def speedVsPram(data, param):
    own_speed = data['own_speed']
    obst_speed = data['obst_speed']

    if len(param) > 1:
        for para in param:
            plt.figure()
            plt.title(para + ' vs ' + 'own_speed')
            plt.scatter(own_speed, data[para])
            plt.xlabel('own_speed')
            plt.ylabel(para)
            plt.figure()
            plt.title(para + ' vs ' + 'obst_speed')
            plt.scatter(obst_speed, data[para])
            plt.xlabel('own_speed')
            plt.ylabel(para)
            print('Correlation between own_speed and ' + para + ' : ' + str(stat.spearmanr(own_speed, data[para])))
            print('Correlation between obst_speed and ' + para + ' : ' + str(stat.spearmanr(obst_speed, data[para])))
    else:
        plt.figure()
        plt.title(param + ' vs ' + 'own_speed')
        plt.scatter(own_speed, data[param])
        plt.xlabel('own_speed')
        plt.ylabel(param)
        plt.figure()
        plt.title(param + ' vs ' + 'obst_speed')
        plt.scatter(obst_speed, data[param])
        plt.xlabel('own_speed')
        plt.ylabel(param)
        print('Correlation between own_speed and ' + param + ' : ' + str(stat.spearmanr(own_speed, param)))
        print('Correlation between obst_speed and ' + param + ' : ' + str(stat.spearmanr(obst_speed, param)))



if __name__ == '__main__':
    #data = HO_clustered.loc[HO_clustered['label'] == 0]
    #parameters = ['alpha_cpa', 'beta_cpa', 'delta_course_own', 'delta_speed_own', 'own_length', 'obst_length', 'r_cpa', 'r_maneuver_own', 'r_maneuver_obst', 'length_ratio']
    #obstacleManeuver(data, parameters)
    #lengthsAndDistances(data)
    #plt.show()

    #types = {'own_name' : 'str','obst_name' : 'str','date_cpa' : 'str','start_idx': np.int32,'stop_idx': np.int32,'case' : 'str','img_name' : 'str','img_class' : 'str', 'COLREG': np.float64,'own_length': np.float64,'obst_length': np.float32, 'own_type': np.float32,'obst_type': np.float32,'own_nav_status': np.float32,'obst_nav_status': np.float32,'own_speed': np.float32,'obst_speed': np.float32,'maneuver_index_own': np.float32,'r_maneuver_own': np.float32,'pre_man_dist_own': np.float32,'post_man_dist_own': np.float32,'delta_speed_own': np.float32,'delta_course_own': np.float32,'alpha_start': np.float32,'beta_start': np.float32,'r_cpa': np.float32,'alpha_cpa': np.float32,'beta_cpa': np.float32, 'dist_to_coast': np.float32}
    #types = {'own_name' : 'str','obst_name' : 'str','date_cpa' : 'str','start_idx': np.int32,'stop_idx': np.int32,'case' : 'str','img_name' : 'str','img_class' : 'str', 'COLREG': np.float64,'own_length': np.float64,'obst_length': np.float32, 'own_type': np.float32,'obst_type': np.float32,'own_nav_status': np.float32,'obst_nav_status': np.float32,'own_speed': np.float32,'obst_speed': np.float32,'maneuver_index_own': np.float32,'r_maneuver_own': np.float32,'pre_man_dist_own': np.float32,'post_man_dist_own': np.float32,'delta_speed_own': np.float32,'delta_course_own': np.float32,'alpha_start': np.float32,'beta_start': np.float32,'r_cpa': np.float32,'alpha_cpa': np.float32,'beta_cpa': np.float32, 'dist_to_coast': np.float32}

    #df = pd.read_csv('COLREG_w_land.csv',  sep=";", decimal=".",  dtype=types) 
    #dist_to_coast('COLREG_w_land.csv')
    #try_('COLREG_w_land.csv')
    path = 'Data/'
    data = OTGW_south 
    lengthsAndDistances(data, os.path.join(path,'coastal_basemap_data.npy'))
    #obstacleManeuver(data, 'own_length')
    #param = 'delta_course_own'
    #poseStartVsParam(HO_df, param)
    #lengthVsParam(data, param)
    #speedVsPram(data, param)
    plt.show()