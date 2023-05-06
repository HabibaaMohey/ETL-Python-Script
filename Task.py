import pandas as pd
import json
import argparse
import os
import time



parser = argparse.ArgumentParser()
parser.add_argument("FILEPATH", help = "ENTER YOUR JSON FILE ")
parser.add_argument("-u", action="store_true", dest="unix", default=False, help=" MAINTAIN UNIX FORMAT")

args = parser.parse_args()
path=args.FILEPATH



#============

df1 = pd.read_json(path,lines=True)
df1.columns
df1 = df1.drop(df1.columns[[1,2,4,5,6,7,8,9]], axis=1)
#==========
df1['r'].replace('http://', '', regex=True, inplace=True)
df1['r'].replace("(/).*","", regex=True , inplace=True)  
#=========
df1['u'].replace('^(http|https)://', '', regex=True, inplace=True)
df1['u'].replace("(/).*","", regex=True , inplace=True)
#=====
#df1["a"].unique() #to show data 
df1['a2'] = df1.loc[:, 'a'] #copied coloumn for applying functions
df1['a'].replace("\([^)]*\).*","", regex=True , inplace=True) #browser  
#===========
def o_s(x): #operating system 
    if 'Windows' in x :
        x='Windows'
        return x
    elif 'Macintosh' in x :
        x='Macintosh'
        return x
    else:
        x='Ubuntu'
        return x 
df1['a2']=df1.a2.apply(o_s) 
#======= 
df1['longitude'] = df1['ll'].str.get(0)
df1['latitude'] = df1['ll'].str.get(1)

#=========
df1.fillna('None', inplace=True)
df1 = df1.replace(r'^\s*$', 'None', regex=True)

#==========
df1 = df1[['a', 'a2', 'r', 'u', 'cy','longitude','latitude','tz','t','hc']]
df1.rename(columns ={"a": "web_browser",
"a2": "operating_sys",
"r": "from_url",
"u": "to_url",
"cy":"city",
"tz":"time_zone",
"t":"time_in",
"hc":"time_out"} , inplace = True)
#df1

if not args.unix:
 
 df1['time_in'] = pd.to_datetime(df1['time_in'],unit='s')
 df1['time_out'] = pd.to_datetime(df1['time_out'],unit='ms')
 
#========
 
  
outname = 'name.csv'  
  
outdir = './dir'  
if not os.path.exists(outdir):  
    os.mkdir(outdir)  
  
fullname = os.path.join(outdir, outname)      
df1.to_csv(fullname)  
start_time=time.time()





print("--- %s seconds ---" % (time.time() - start_time))
print("ROWS AFFECTED " + str(len(df1)))
print ("File path " + fullname )

