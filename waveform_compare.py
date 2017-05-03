#!/home/samhaug/anaconda2/bin/python

'''
==============================================================================

File Name : waveform_compare.py
Purpose : Compare waveform synth A1,A2 a la Ritsema et al. 2002
Creation Date : 02-05-2017
Last Modified : Tue 02 May 2017 04:21:01 PM EDT
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
from scipy.signal import correlate

def main():
    syn_t = read_synthetic('2006_11_13_T/')
    syn_t = seispy.filter.range_filter(syn_t,(0,72))
    dat_t = read_data('2006-11-13-mw68-santiago-del-estero-prov-arg-5/')
    dat_t = seispy.filter.range_filter(dat_t,(0,72))

    for idx,tr in enumerate(syn_t):
        S_dat, ScS_dat = window_S_ScS(dat_t[idx])
        S_syn, ScS_syn = window_S_ScS(syn_t[idx])
        A1_S,A2_S = correlate_A1_A2(S_dat,S_syn)
        A1_ScS,A2_ScS = correlate_A1_A2(ScS_dat,ScS_syn)
        ratio = ratio_A1_A2(A1_S,A2_S,A1_ScS,A2_ScS)
        print ratio


def read_synthetic(dirname):
    syn_t = obspy.read('/home/samhaug/work1/PcP_ScS_sims/'+dirname+'st_T.pk')
    syn_t.interpolate(40)
    syn_t.integrate()
    syn_t.filter('lowpass',freq=1/8.,zerophase=True)
    for tr in syn_t:
        tr.data *= -1.
    syn_t = seispy.data.normalize_on_phase(syn_t,phase=['S'],window_tuple=(0,40))
    seispy.plot.simple_section(syn_t)
    return syn_t

def read_data(dirname):
    dat_t = obspy.read('/home/samhaug/work1/PcP_ScS_data/'+dirname+'stt.pk')
    dat_t.interpolate(40)
    for tr in dat_t:
        tr.data *= -1.
    dat_t = seispy.data.normalize_on_phase(dat_t,phase=['S'],window_tuple=(0,40))
    seispy.plot.simple_section(dat_t)
    return dat_t

def window_S_ScS(tr):
    S = seispy.data.phase_window(tr,['S'],window=(0,40)).data
    ScS = seispy.data.phase_window(tr,['ScS'],window=(0,40)).data
    return S,ScS

def correlate_A1_A2(data,synth):
    '''A_{1},A_{2} as specified in Ritsema et al. 2002'''
    #plt.plot(data)
    #plt.plot(synth)
    #plt.show()
    ds = correlate(data,synth,mode='same')
    ss = correlate(synth,synth,mode='same')
    dd = correlate(data,data,mode='same')
    sd = correlate(synth,data,mode='same')
    A1 = ds.max()/ss.max()
    A2 = dd.max()/ds.max()
    return A1,A2

def ratio_A1_A2(A1_S,A2_S,A1_ScS,A2_ScS):
    A1_S_ScS = min(A1_S,A2_S)/max(A1_ScS,A2_ScS)
    A2_S_ScS = max(A1_S,A2_S)/min(A1_ScS,A2_ScS)
    return (A1_S_ScS+A2_S_ScS)/2.

main()
