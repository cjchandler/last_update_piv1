#!/home/carl/Git_Projects/incubator/incubator/pi_incubator/envH/bin/python


#ntfy messaging thing
import requests
import time
import pandas as pd
import os
from datetime import datetime
import subprocess


def push_latest_timestamp( tval ): 
    tnow = time.time() 
    
    #update the project file with current time
    f = open( "/home/carl/Git_Projects/last_update_piv1/timestamp.txt", "w")
    f.write(str(tval))
    f.close()
    
    #push that to git

# Run a command inside a specific folder
    subprocess.run(["git",  "pull" ,  "origin" ,  "main" , "--no-edit" , "--allow-unrelated-histories"], cwd="/home/carl/Git_Projects/last_update_piv1")
    subprocess.run(["git", "add", "."], cwd="/home/carl/Git_Projects/last_update_piv1")
    subprocess.run(["git", "commit", "-a", "-m", 'data_automatic' ], cwd="/home/carl/Git_Projects/last_update_piv1")
    subprocess.run(["git", "push" , "origin" , "main"], cwd="/home/carl/Git_Projects/last_update_piv1")
    
    print("backup via git is done")

   
#send a message saysing all's well, I'm alive, here's the latest timestamp

try: 
    #look up the file:
    filepath = "/home/carl/Git_Projects/incubator/incubator/pi_incubator/datalog/today_data_piV1.csv"
    #look at the pandas thing for last timestamp
    df = pd.read_csv(filepath)
    print(df.tail(20))
    tsaved = df[df.columns[2]].iloc[-1] #2 is the last time saved column
    
    now = datetime.now()
    # Extract integers
    current_hour = now.hour
    current_minute = now.minute
    print( current_hour , current_minute)
    if current_hour == 12 and current_minute < 10:
        pass
    else:
        push_latest_timestamp( tsaved  )

except Exception as e:
    print(e)
    
    
