# In case you're using Linux, you can achieve the same using the package wget from terminal
# wget -r --no-parent ftp://ftp.bmf.com.br/MarketData
# After a quick test, you may realize using wget's faster than using this Python script

import ftplib, os, urllib2, shutil, contextlib
import Aux_main
import Tkinter as Tk, datetime as dt, thread

def Stop_Download(thread_id):
    thread.exit(thread_id)

class Update_local_data():
    
    def __init__(self, src, args):
        self.__src = src
        self.__flag = False
        self.__running = False;
        self.__args = args

    def __Print(self, s):
        Aux_main.Print2(self.__src,s)

    def __start(self):

        self.__running = True
        self.__Print("Downloading has been started.")
        
        sv = "ftp.bmf.com.br"
        ftp = ftplib.FTP(sv)
        ftp.login() # start connection
        ftp.cwd("MarketData") # change current directory
        targets = ftp.nlst()[:3] # get list of directories of interest
        self.__Print("List of directories of interest has been adquired.")
        ftp.quit() # end connection

        for targ in targets:
            if not self.__args[targ]:
                continue
            self.__Print("Working on directory of interest: %s" %(targ))
            ftp = ftplib.FTP("ftp.bmf.com.br")
            cc = ftp.login()
            if "Anonymous user logged in" in cc:
                self.__Print("Connection to FTP server has been established.")
            else:
                self.__Print("Connection has just failed.")
                break
            ftp.cwd("%s/%s"%("MarketData",targ))
            l = ftp.nlst() # get list of files in directory of interest
            ftp.quit()

            if not os.path.exists("%s/%s"%("MarketData",targ)):
                os.makedirs("%s/%s"%("MarketData",targ)) # create local folder to download files
                self.__Print("Local folder MarketData/"+targ+" has been created.")
            else:
                self.__Print("Local folder MarketData/"+targ+" has been found.")

            self.__Print("Starting downloading...")
            # in case if the connection breaks suddenly, just restart the script
            # then it'll continue from it'd stopped
            l2 = os.listdir("%s/%s"%("MarketData",targ))
            for f in l:
                if f in l2:
                    continue
                else:
                    if self.__flag:
                        break
                    if (not self.__args["Offer-sell"] and "CPA" in f) or \
                        (not self.__args["NEGs done"] and "NEG" in f) or \
                        (not self.__args["Offer-buy"] and "VDA" in f):
                        continue
                    with contextlib.closing(urllib2.urlopen("ftp://%s/MarketData/%s/%s"%(sv,targ,f))) as rr:
                        with open("MarketData/%s/%s"%(targ,f), 'wb') as fh:
                            shutil.copyfileobj(rr,fh)
                    self.__Print("The download of %s/%s has been completed." %(targ,f))
                    if self.__flag:
                        break
            if self.__flag:
                break
            self.__Print("%s has been completed."%(targ))
        self.__running = False

    def running(self):
        return self.__running

    def start(self):
        thread.start_new_thread(self.__start,())

    def stop(self):
        if self.__running:
            self.__Print("Interrupting download, wait...")
            self.__flag = True

    

