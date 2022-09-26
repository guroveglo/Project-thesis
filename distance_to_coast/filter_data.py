from xmlrpc.client import Boolean
import pandas as pd
import numpy as np

OP = -3  # Obstacle passed
OTGW = -2  # Overtaking situation - own ship is give way vessel
CRGW = -1  # Crossing situation - own ship is give way vessel
NAR = 0  # No applicable rules
CRSO = 1  # Crossing situation - own ship is stand on vessel
OTSO = 2  # Overtaking situation - own ship is stand on vessel
HO = 3  # Head on situation
STAT = 4  # Static obstacle

types = {'own_name' : 'str','obst_name' : 'str','date_cpa' : 'str','start_idx': np.int32,'stop_idx': np.int32,'case' : 'str','img_name' : 'str','img_class' : 'str', 'COLREG': np.float64,'own_length': np.float64,'obst_length': np.float32, 'own_type': np.float32,'obst_type': np.float32,'own_nav_status': np.float32,'obst_nav_status': np.float32,'own_speed': np.float32,'obst_speed': np.float32,'maneuver_index_own': np.float32,'r_maneuver_own': np.float32,'pre_man_dist_own': np.float32,'post_man_dist_own': np.float32,'delta_speed_own': np.float32,'delta_course_own': np.float32,'alpha_start': np.float32,'beta_start': np.float32,'r_cpa': np.float32,'alpha_cpa': np.float32,'beta_cpa': np.float32}

df = pd.read_csv('COLREG_classified.csv',  sep=";", decimal=".", dtype=types) 
input(df)



print('Parameter file:\nNumber of situations: ' + str(len(df)))
df = df.drop_duplicates(subset=['own_mmsi', 'obst_mmsi', 'date_cpa'], keep="first")  # Remove duplicates (diff case)
print('Number of situations without duplicates: ' + str(len(df)))
df = df.loc[df['img_class'] == 'True']  # remove situations that mas not been manually approved
print('Number of manually classified situations: ' + str(len(df)))
df = df.loc[(df['r_cpa'] > 200)]  # include only encounters with DCPA < 700 meters
print('Number of situations with DCPA > 700m: ' + str(len(df)))
df = df.loc[~(df['own_length'].isnull())]  # remove nan values
df = df.loc[~(df['obst_length'].isnull())]  # remove nan values
df = df.loc[(df['own_length'] != 0)]  # remove zero values
df = df.loc[(df['obst_length'] != 0)]  # remove zero values
print('Number of situations with ship lengths: ' + str(len(df)))
df = df.loc[~(df['pre_man_t_cpa_own'].isnull())]  # remove nan values
df = df.loc[(df['pre_man_t_cpa_own'] != 0)]  # remove zero values
print('Number of situations with pred TCPA: ' + str(len(df)))

# TODO: Figure out why there are so many port to port passings and port turns
HO_df = df.loc[(df['COLREG'] == HO)]
n_before = len(HO_df)
HO_df = HO_df.loc[(HO_df['alpha_cpa'] > 0)]  # Exclude sb-to-sb passings
HO_df = HO_df.loc[(HO_df['beta_cpa'] < 180)]  # Exclude sb-to-sb passings
HO_df = HO_df.loc[(HO_df['delta_course_own'] < 0)]  # Exclude port maneuvers
print('Number of head-on situations: before filt:' + str(n_before) + ', after filt:' + str(len(HO_df)))
HO_man_obst = HO_df.loc[(HO_df['maneuver_made_obst'] == True)]
print('Number of situations were obst ship makes maneuver: ', str(len(HO_man_obst)))

OTGW_df = df.loc[(df['COLREG'] == OTGW)]
print('Number of otgw situations: ' + str(len(OTGW_df)))
OTGW_man_obst = OTGW_df.loc[(OTGW_df['maneuver_made_obst'] == True)]
print('Number of situations were obst ship makes maneuver: ', str(len(OTGW_man_obst)))

CRGW_df = df.loc[(df['COLREG'] == CRGW)]
n_before = len(CRGW_df)
CRGW_df = CRGW_df.loc[(CRGW_df['alpha_start'] > -10)]  # Exclude port starts
CRGW_df = CRGW_df.loc[(CRGW_df['beta_start'] > 180)]  # Exclude port starts
CRGW_df = CRGW_df.loc[(CRGW_df['delta_course_own'] < 0)]  # Exclude port maneuvers
print('Number of crgw situations: before filt:' + str(n_before) + ', after filt:' + str(len(CRGW_df)))
CRGW_man_obst = CRGW_df.loc[(CRGW_df['maneuver_made_obst'] == True)]
print('Number of situations were obst ship makes maneuver: ', str(len(CRGW_man_obst)))


HO_west = HO_df.loc[HO_df['dataset'] == 'encs_west']
OTGW_west = OTGW_df.loc[OTGW_df['dataset'] == 'encs_west']
CRGW_west = CRGW_df.loc[CRGW_df['dataset'] == 'encs_west']

print('Number HO_west: '+ str(len(HO_west)))
print('Number OTGW_west: '+ str(len(OTGW_west)))
print('Number CRGW_west: '+ str(len(CRGW_west)))


HO_south = HO_df.loc[HO_df['dataset'].str.startswith('encs_south')]
OTGW_south = OTGW_df.loc[OTGW_df['dataset'].str.startswith('encs_south')]
CRGW_south = CRGW_df.loc[CRGW_df['dataset'].str.startswith('encs_south')]

print('Number HO_south: '+ str(len(HO_south)))
print('Number OTGW_south: '+ str(len(OTGW_south)))
print('Number CRGW_south: '+ str(len(CRGW_south)))
