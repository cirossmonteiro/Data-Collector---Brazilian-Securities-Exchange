import Tkinter as Tk, Aux_Download as ad
import threading as Th, Aux_main as am, thread, os, zipfile
import cPickle as pk

class WAbout_us(Tk.Frame):

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def doit(self):
        self.parent.quit()
        self.parent.destroy()

    def initUI(self):
        self.parent.title("About us")
        self.parent.geometry('{}x{}'.format(250, 100))
        
        Tk.Label(self.parent, text = "Data Collector non-commercial version").pack()
        Tk.Label(self.parent, text = "Developed by Ciro SS Monteiro.").pack()
        Tk.Label(self.parent, text = "Version January/2017").pack()
        Tk.Button(self.parent, text = "OK", command = self.doit).pack()
        
    

class WUpdate(Tk.Frame):

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def doit(self):
        l = [q.get() for q in self.vchecks]
        if 1 in l[:2] and 1 in l[3:]:
            self.asked = {}
            for i in xrange(len(self.tchecks)):
                self.asked[self.tchecks[i]] = l[i]
            self.parent.quit()
            self.parent.destroy()


    def initUI(self):
        self.parent.title("Update local data")
        self.parent.geometry('{}x{}'.format(500,80))

        self.tchecks = ["BMF","Bovespa-Opcoes","Bovespa-Vista","NEGs done", "Offer-buy", "Offer-sell"]
        self.vchecks = [None]*len(self.tchecks)
        self.bchecks = [None]*len(self.tchecks)

        self.l1 = Tk.Label(self.parent, text = "Select at least one source: ")
        self.l2 = Tk.Label(self.parent, text = "Select at least one type: ")
        self.l1.grid(row = 0, column = 0)
        self.l2.grid(row = 1, column = 0)

        
        for i in xrange(len(self.tchecks)):
            self.vchecks[i] = Tk.IntVar(self.parent)
            self.bchecks[i] = Tk.Checkbutton(self.parent, text = self.tchecks[i], variable = self.vchecks[i])
            self.bchecks[i].grid(row = i/3, column = i%3+1)
        
        self.botao = Tk.Button(self.parent, text = "Update", command = self.doit)
        self.botao.grid(row = 2, column = 0)


    
class Main(Tk.Frame):

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.__list_sec = []
        self.__rootdir = "MarketData"
        self.__direc = ["BMF","Bovespa-Opcoes","Bovespa-Vista"]
        self.__upload_local_data = None
        self.parent.title("Data Collector - BR Securities Exchange")
        self.parent.geometry('{}x{}'.format(800,600))


        self.LOutput = Tk.Label(self.parent, text="Output")
        self.LOutput.pack()
        self.Scrollbar = Tk.Scrollbar(self.parent)
        self.Scrollbar.pack(side = Tk.RIGHT, fill = Tk.Y)
        self.Output = Tk.Listbox(self.parent, yscrollcommand = self.Scrollbar.set, width = 100)
        self.Output.pack(side = Tk.LEFT, fill = Tk.BOTH)
        self.Scrollbar.config(command = self.Output.yview)

        self.Menubar = Tk.Menu(self.parent, tearoff = 0)
        self.parent.config(menu = self.Menubar)

        self.FileMenu = Tk.Menu(self.Menubar, tearoff = 0)
        def tempf1():
            self.popup = Tk.Tk()
            self.wpopup = WUpdate(self.popup)
            self.popup.mainloop()
            self.FileMenu.entryconfig("Update local data", state = "disabled")
            self.FileMenu.entryconfig("Stop updating local data", state = "normal")
            self.__update_local_data = ad.Update_local_data(self.Output, self.wpopup.asked)
            self.__update_local_data.start()
        def tempf2():
            self.__update_local_data.stop()
            def tempf21():
                while self.__update_local_data.running():
                    pass
                am.Print2(self.Output, "Downloading has been stopped.")
                del self.__upload_local_data
                self.FileMenu.entryconfig("Update local data", state = "normal")
                self.FileMenu.entryconfig("Stop updating local data", state = "disabled")
                self.__upload_local_data = None
            thread.start_new_thread(tempf21,())
        self.FileMenu.add_command(label = "Update local data", command = tempf1)
        self.FileMenu.add_command(label = "Stop updating local data", command = tempf2)
        self.FileMenu.add_command(label = "Exit", command = self.parent.destroy)
        self.Menubar.add_cascade(label = "File", menu = self.FileMenu)
        self.FileMenu.entryconfig("Stop updating local data", state = "disabled")

        
        self.SecuritiesMenu = Tk.Menu(self.Menubar, tearoff = 0)
        self.SecuritiesMenu.add_command(label = "Reload list", command = self.Reload_list)
        self.SecuritiesMenu.add_command(label = "List all", command = self.List_all)
        self.Menubar.add_cascade(label = "Securities", menu = self.SecuritiesMenu)
        if os.path.exists("securities.bin"):
            fh = open("securities.bin",'rb')
            self.__list_sec = pk.load(fh)
            fh.close()
            fh = None
        else:
            self.SecuritiesMenu.entryconfig("List all", state = "disabled")


        self.LogMenu = Tk.Menu(self.Menubar, tearoff = 0)
        self.LogMenu.add_command(label = "Clear log", command = self.__Clear_log)
        self.Menubar.add_cascade(label = "Log", menu = self.LogMenu)
        if not os.path.exists("log.txt"):
            self.LogMenu.entryconfig("Clear log", state = "disabled")


        self.AboutMenu = Tk.Menu(self.Menubar, tearoff = 0)
        self.AboutMenu.add_command(label = "About us", command = self.__About_us)
        self.Menubar.add_cascade(label = "About", menu = self.AboutMenu)
        

        am.Print2(self.Output, "Data Collector - BR Securities Exchange has just started.")

    def __About_us(self):
        self.about = Tk.Tk()
        self.wabout = WAbout_us(self.about)
        self.about.mainloop()

    def __Clear_log(self):
        os.remove("log.txt")
        self.LogMenu.entryconfig("Clear log", state = "disabled")
        am.Print2(self.Output, "Log file has been cleared.")
        

    def Reload_list(self):
        thread.start_new_thread(self.__Reload_list, ())

    def __Reload_list(self):
        self.__list_sec = set()
        stemp = ""
        for target in self.__direc:
            ldir = os.listdir("%s/%s"%(self.__rootdir, target))
            for ffile in ldir:
                if 'NEG' in ffile:
                    with zipfile.ZipFile("%s/%s/%s"%(self.__rootdir, target, ffile),'r') as zip_ref:
                    #zip_ref.extractall("%s/%s"%(dir1,d))
                    # two possible cases of naming files
                        try:
                            fn = "apphmb/intraday/%s.TXT"%(ffile[:-4])
                            fh = zip_ref.open(fn,'r')
                        except:
                            fn = "%s.TXT"%(ffile[:-4])
                            fh = zip_ref.open(fn,'r')
                        dailydata = fh.read().split('\n')
                        for q in dailydata:
                            qq = q.split(';')
                            if len(qq) > 5: # indeed, it's a quote
                                qn = am.nospace(qq[1])
                                self.__list_sec.add(qn)                                
                        fh.close()
                        zip_ref.close()
                    am.Print2(self.Output, ffile)
        fh = open("securities.bin", 'wb')
        pk.dump(self.__list_sec, fh)
        fh.close()
        self.SecuritiesMenu.entryconfig("List all", state = "normal")
        

    def List_all(self):
        thread.start_new_thread(self.__List_all, ())

    def __List_all(self):
        ss = ""
        for sec in self.__list_sec:
            if len(ss+' '+sec) > 189:
                am.Print2(self.Output, ss)
                ss = ""+sec
            else:
                ss += ' '+sec
        am.Print2(self.Output, ss)

        
if __name__ == '__main__':
    root = Tk.Tk()
    app = Main(root)
    root.mainloop()
