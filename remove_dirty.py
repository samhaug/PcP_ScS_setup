#!/home/samhaug/anaconda2/bin/python

'''
==============================================================================

File Name : remove_dirty.py
Purpose : automate dirty seismogram removal of large stream
Creation Date : 03-05-2017
Last Modified : Wed 03 May 2017 04:29:07 PM EDT
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
import sys

def main():
    st = obspy.read(sys.argv[1])
    st.filter('lowpass',freq=1/5.,zerophase=True)
    st.normalize()
    keep_list = split_stream(st)
    stclean = clean_stream(st,keep_list)
    write_st(stclean)

def split_stream(st):
    keep_list = []
    for ii in range(0,12):
        sparse = st[ii::11].copy()
        seispy.plot.simple_section(sparse,picker=True)
        for tr in sparse:
            keep_list.append(tr.stats.station)
    return keep_list

def clean_stream(st,keep_list):
    for tr in st:
        if tr.stats.station in keep_list:
            continue
        else:
            st.remove(tr)
    return st

def write_st(st):
    st.write('stt_clean.pk',format='PICKLE')


main()
