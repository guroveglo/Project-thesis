
import scipy.stats as stat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, cos, sin
from filter_data import HO_south, CRGW_south, OTGW_south

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
    
def lengthsAndDistances(data):
    own_lengths = data['own_length'] # every row in this column 
    obst_lengths = data['obst_length'] 
    r_cpa = data['r_cpa']
    r_maneuver = data['r_maneuver_own']
    length_ratio = obst_lengths/own_lengths
    mean_length = (obst_lengths+own_lengths)/2
    print('Correlation r_cpa and mean length ' + str(stat.spearmanr(r_cpa, mean_length)))
    print('Correlation r_maneuver and mean length ' + str(stat.spearmanr(r_maneuver, mean_length)))
    #print('Correlation r_cpa and length_ratio ' + str(stat.spearmanr(r_cpa, length_ratio)))
    #print('Correlation r_maneuver and length_ratio ' + str(stat.spearmanr(r_maneuver, length_ratio)))
    #print('Correlation r_cpa and own length ' + str(stat.spearmanr(r_cpa, own_lengths)))
    #print('Correlation r_cpa and obst length ' + str(stat.spearmanr(r_cpa, obst_lengths)))
    speed_own = data['own_speed']
    speed_obst = data['obst_speed']
    contact_angle = ['alpha_cpa']  #in degrees
    #relative_speed_own = np.sqrt((speed_obst*np.cos(contact_angle)- speed_own)**2 + (speed_obst*np.sin(contact_angle))**2 )  #MAKE THIS WORK (maybe by using a loop instead of numpy)

    fig = plt.figure()
    plt.title('r_cpa vs mean length')
    plt.xlabel('r cpa')
    plt.ylabel('mean length ')
    plt.scatter(r_cpa, mean_length, alpha=0.5, c ='#EA3245')

    fig = plt.figure()
    plt.scatter(r_maneuver, mean_length, alpha=0.5, c='#24C459')
    plt.title('r_maneuver vs mean length')
    plt.xlabel('r maneuver')
    plt.ylabel('mean length')

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

    types = {'own_name' : 'str','obst_name' : 'str','date_cpa' : 'str','start_idx': np.int32,'stop_idx': np.int32,'case' : 'str','img_name' : 'str','img_class' : 'str', 'COLREG': np.float64,'own_length': np.float64,'obst_length': np.float32, 'own_type': np.float32,'obst_type': np.float32,'own_nav_status': np.float32,'obst_nav_status': np.float32,'own_speed': np.float32,'obst_speed': np.float32,'maneuver_index_own': np.float32,'r_maneuver_own': np.float32,'pre_man_dist_own': np.float32,'post_man_dist_own': np.float32,'delta_speed_own': np.float32,'delta_course_own': np.float32,'alpha_start': np.float32,'beta_start': np.float32,'r_cpa': np.float32,'alpha_cpa': np.float32,'beta_cpa': np.float32, 'dist_to_coast': np.float32}

    df = pd.read_csv('COLREG_classified_dist_to_shore.csv',  sep=";", decimal=".") 
    

    #data = OTGW_south
    #lengthsAndDistances(data)

    #obstacleManeuver(data, 'own_length')
    #param = 'delta_course_own'
    #poseStartVsParam(HO_df, param)
    #lengthVsParam(data, param)
    #speedVsPram(data, param)
    plt.show()