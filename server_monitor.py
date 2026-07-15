class basic_monitor: #this looks at a time file and sends alarm itf it's been too long without updates
    def __init__(self , repo_name  , filein , backup_interval): #backup_interval is how many seconds without updates is ok
        self.repo_name = repo_name
        if os.path.isdir(repo_name) == False:
            print("cloning the last update repo git archive , it's public ")
            os.system('git clone https://github.com/cjchandler/'+repo_name+'.git')
        else:
            print("pull the latest version")
            os.system("cd "+repo_name+" \n "+repo_name+" \n git reset --hard origin/main")


        self.filename = filein
        self.backup_interval = backup_interval

        self.alarms_active_dict = {}
        self.alarm_last_send_dict= {}
        self.alarm_next_send_dict= {}
        self.alarm_message_dict= {}

        self.alarms_active_dict['git alarm'] = False
        self.alarms_active_dict['file update alarm'] = False
        self.alarm_last_send_dict['file update alarm'] = 0
        self.alarm_next_send_dict['file update alarm'] = 0


        self.last_backup_time = 0


        self.SS = slack_sender()






    def pull_through_git(self ):

        if( True):

            try:
                os.system("cd "+self.repo_name+" \n "+self.repo_name+" \n git reset --hard origin/main")
                self.last_backup_time = time.time()
                self.alarms_active_dict['git alarm'] = False
                print("backup via git is gotten")


            except:
                print("failed to get data updates via git")
                self.alarms_active_dict['git alarm'] = True
                self.alarm_message_dict[  'git alarm'] = self.filename+ "error getting the last update repo from github"

    def file_updated_recently(self):
        f = open("./"+self.repo_name+"/" + self.filename, "r")
        dstring = (f.readline())
        if time.time() > float(dstring) + self.backup_interval:
            return False, float(dstring)
        else :
            return True, float(dstring)

    def look_at_data_update_alarm_states(self):
        recent_file_update_bool, self.last_backup_time  = self.file_updated_recently()


        #reset all alarms to off
        for key in self.alarms_active_dict:
             self.alarms_active_dict[key] = 0

        #now check if any alarms are active from the current data set

        time_since_last_save = time.time() - int(self.last_backup_time )

        if( time_since_last_save >=  self.backup_interval     ):
            self.alarms_active_dict['file update alarm'] = True
            self.alarm_message_dict[  'file update alarm'] = self.filename+ " not logging data in last update repo. secs without data = "+ str(time_since_last_save) +"  Probably malfunctioning seriously "

            print( "no file updates in " , time_since_last_save , "seconds")

    def send_alarms(self):
        #look at all active alarms
        for key in self.alarms_active_dict:
            if self.alarms_active_dict[key] == True:
                #look at the last time we sent an alarm
                last_alarm =  self.alarm_last_send_dict[key]
                #look at the next alarm send time:
                next_alarm = self.alarm_next_send_dict[key]

                #if past next alarm time, send it, update last send
                if time.time() > next_alarm:
                    print("sent and alarm for " , key)
                    self.SS.send_message( "PYTHONANYWHERE SERVER:" + self.filename +" "+ key + " " + self.alarm_message_dict[key] + "  " + time.ctime() + "GMT, this is server alarm" )
                    self.alarm_last_send_dict[key] = time.time()



    def do_all(self):

        self.pull_through_git()
        self.look_at_data_update_alarm_states()
        self.send_alarms()
        
        

		# Get current date and time
		now = datetime.now()

		# Extract integers
		current_hour = now.hour
		current_minute = now.minute

		if current_hour == 13 and current_minute < 3: 
			self.SS.send_message( "PYTHONANYWHERE SERVER:" + self.repo_name +" last update monitor working fine" )

   
        
 
piv1 = basic_monitor("last_update_piv1" , "timestamp.txt" , 60*3)       
while True: 
    piv1.do_all()
    time.sleep(50)
