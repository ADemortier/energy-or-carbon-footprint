#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created sometimes in 2021
@author: faure
'''

import csv
import numpy as np
import pandas as pd
import copy
from datetime import timedelta
import sys
import pickle

#root_path = "/home/faure/EcoStats"
root_path = "./"
#root_path = '/home/cnrm_other/ge/mrmp/demortiera/xpout/GLI2/20210906/'
#zefile = root_path + '/' + '3dvarfr_1day' + '_kwh.txt'
if len(sys.argv) < 2:
    print("File must be specified as argument!")
    quit()
elif len(sys.argv) == 2:
    zefile = sys.argv[1]
else:
    quit("1 argument maximum !")

def hourCPU(time_):
   zetime = copy.deepcopy(time_)
   if "-" in time_:
      zetime1 = zetime.split("-")
      d = zetime1[0]; zetime = zetime1[1] #zetime = ''.join(zetime[1:])
   else :
      d = 0
   zetime2 = zetime.split(":")
   if len(zetime2)<3:
      h = 0; m = zetime2[0]; s = zetime2[1]
   else:
      h = zetime2[0]; m = zetime2[1]; s = zetime2[2]
   if s == '': s = 0
   #print(time_)
   datetime_ = timedelta(days=int(d), hours=int(h), minutes = int(m), seconds = float(s))
   totalhours = datetime_.total_seconds()/3600
   return(totalhours)

if ("kwh" in zefile):

    MyFields = ["file","StepID", "sep", "JobName","State", "Exit", "Start", "End", "Elapsed", "TotalCPU", "CPUTime", "ConsumedEnergy",
        "MaxDiskRead", "MaxDiskWrite", "MaxRSS", "MaxRSSTask", "MaxRSSNode", "NNodes", "NodeList", "Comment"]
    #MyFields = ["1", "2", "3", "dayOrH", "day", "H", 'else']
    zeliste = []
    first=True

    print(root_path+zefile)
    
    dfkw = pd.DataFrame()
    with open( root_path+zefile, "r" ) as theFile:
        reader = csv.DictReader( theFile, fieldnames = MyFields, delimiter=' ',skipinitialspace=True)
        ##print(reader)
        for line in reader:
            list_ = line['file'].split('/')[1:6]
            if len(list_)==4:
                dfkw_ = pd.DataFrame(list_, index = ['date', 'hour', 'kind', 'job']).T
            else :
            	dfkw_ = pd.DataFrame(list_, index = ['date', 'hour', 'kind', 'step', 'job']).T
            if first: #print(line['file'])
                print(line['file'])
                first = False
                pass
            try:
                ##print(line)
                if (line["ConsumedEnergy"] is not None):
                    e = line["ConsumedEnergy"]
                    print(e)
                    if (e[-1] == "M"):
                        val = e[:-1]
                        zeliste.append(float(val)*1000000)
                        dfkw_['kwh'] = float(val)*1000000
                        dfkw_['hCPU'] = hourCPU(line["TotalCPU"])
                        print(dfkw_)
                        dfkw = pd.concat([dfkw, dfkw_])
                    elif (e[-1] == "K"):
                        val = e[:-1]
                        zeliste.append(float(val)*1000)
                        dfkw_['kwh'] = float(val)*1000
                        dfkw_['hCPU'] = hourCPU(line["TotalCPU"])
                        dfkw = pd.concat([dfkw, dfkw_])
                    else:
                        #print('consumed energy', e)
                        dfkw_['kwh'] = 0
                        dfkw_['hCPU'] = hourCPU(line["TotalCPU"])
                        dfkw = pd.concat([dfkw, dfkw_])
                        pass
		
            except:
                pass
    print(dfkw)
    with open("main_kwh_"+zefile[:-4]+".pkl",'wb') as f:
        pickle.dump(dfkw, f) #_superobs       
    totalEnergy = np.array(zeliste)
    #print(totalEnergy)
    print("Total energy in kwh: ", totalEnergy.sum()/3600000.)

elif ("tei" in zefile):

    MyFields = ["1", "2", "3", "dayOrH", "day", "H"]

    zeliste = []
    first=True

    print(root_path+zefile)

    dftei = pd.DataFrame()
    with open( root_path+zefile, "r" ) as theFile:
        reader = csv.DictReader( theFile, fieldnames = MyFields, delimiter=' ',skipinitialspace=True)
        for line in reader:
            list_ = line['1'].split('/')[1:6]
            if len(list_)==4:
                dftei_ = pd.DataFrame(line['1'].split('/')[1:6], index = ['date', 'hour', 'kind', 'job']).T
            else :
                dftei_ = pd.DataFrame(line['1'].split('/')[1:6], index = ['date', 'hour', 'kind', 'step', 'job']).T
            if first:
                print(line['1'])
                first = False
                pass
            #try:
            if (line["H"] is not None):
                zetime = line["H"].split(":")
                #print(zetime[0])
                delta = timedelta(days=int(line["dayOrH"]), hours=int(zetime[0]), minutes = int(zetime[1]))
                zeliste.append(delta)
                dftei_['tei'] = delta
            elif (line["dayOrH"] is not None):
                zetime = line["dayOrH"].split(":")
                #print(zetime[0])
                delta = timedelta(days=0, hours=int(zetime[0]), minutes = int(zetime[1]))
                zeliste.append(delta)
                dftei_['tei'] = delta
            else:
                pass
            dftei = pd.concat([dftei, dftei_])
    print(dftei)
    with open("main_tei_"+zefile[:-4]+".pkl",'wb') as f:
        pickle.dump(dftei, f) #_superobs
    totalEnergy = np.array(zeliste)
    print(totalEnergy)
    print("Total TEI time: ", totalEnergy.sum())

elif ("Elapsedtime" in zefile):

    MyFields = ["1", "2", "3", "4", "dayOrH", "day", "H"]

    zeliste = []
    first=True

    print(root_path+zefile)

    dftei = pd.DataFrame()
    with open( root_path+zefile, "r" ) as theFile:
        reader = csv.DictReader( theFile, fieldnames = MyFields, delimiter=' ',skipinitialspace=True)
        for line in reader:
            #print(line)
            dftei_ = pd.DataFrame(line['1'].split('/')[1:6], index = ['date', 'hour', 'kind', 'step', 'job']).T
            if first:
                print(line['1'])
                first = False
                pass
            #try:
            """
            if (line["H"] is not None) and (line["H"] is not ':'):
                print(line["H"] is not None, line["H"] is not ':')
                zetime = line["H"].split(":")
                #print(zetime[0])
                delta = timedelta(days=int(line["dayOrH"]), hours=int(zetime[0]), minutes = int(zetime[1]))
                zeliste.append(delta)
                dftei_['Elpasedtime'] = delta
            """
            if (line["dayOrH"] is not None):
                zetime = line["dayOrH"].split(":")
                delta = timedelta(days=0, hours=int(zetime[0]), minutes = int(zetime[1]), seconds = int(zetime[2]))
                zeliste.append(delta)
                dftei_['Elapsedtime'] = delta
            else:
                pass
            dftei = pd.concat([dftei, dftei_])
    print(dftei)
    with open("main_Elapsedtime_"+zefile[:-4]+".pkl",'wb') as f:
        pickle.dump(dftei, f) #_superobs
    totalEnergy = np.array(zeliste)
    print(totalEnergy)
    print("Total Elapsedtime time: ", totalEnergy.sum())
else :
    quit('The string "kwh" or "tei" or "Elapsedtime" should appear in the filename.')
