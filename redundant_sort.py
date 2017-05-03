#!/home/samhaug/anaconda2/bin/python

'''
==============================================================================

File Name : redundant_sort.py
Purpose : save stn and ste traces from the same stations.
Creation Date : 18-04-2017
Last Modified : Tue 18 Apr 2017 11:23:44 AM EDT
Created By : Samuel M. Haugland

==============================================================================
'''

import numpy as np
from matplotlib import pyplot as plt
from subprocess import call
from os import listdir
import h5py
import obspy
import seispy

def main():
    stn = read_stn()
    ste = read_ste()
    c_list = common_list(stn,ste)
    print c_list
    stn,ste = remove_trace(stn,ste,c_list)
    print len(stn),len(ste)

def remove_trace(stn,ste,c_list):
    for tr in stn:
        lat = str(round(tr.stats.sac['stla'],1))
        lon = str(round(tr.stats.sac['stlo'],1))
        if lat+lon in c_list:
            continue
        else:
            stn.remove(tr)
    for tr in ste:
        lat = str(round(tr.stats.sac['stla'],1))
        lon = str(round(tr.stats.sac['stlo'],1))
        if lat+lon in c_list:
            continue
        else:
            ste.remove(tr)
    return stn,ste

def common_list(stn,ste):
    e_list = []
    n_list = []
    for tr in ste:
        lat = str(round(tr.stats.sac['stla'],1))
        lon = str(round(tr.stats.sac['stlo'],1))
        e_list.append(lat+lon)
    for tr in stn:
        lat = str(round(tr.stats.sac['stla'],1))
        lon = str(round(tr.stats.sac['stlo'],1))
        n_list.append(lat+lon)
    print zip(e_list,n_list)
    c_list = list(set(e_list)^set(n_list))

def read_stn():
    stn = obspy.read('*BHN*filtered')
    return stn

def read_ste():
    ste = obspy.read('*BHE*filtered')
    return ste


main()
