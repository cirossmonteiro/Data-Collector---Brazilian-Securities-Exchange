import Tkinter as Tk


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
