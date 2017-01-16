import Tkinter as Tk

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

    def select_all(self):
        if self.vall.get():
            for b in self.bchecks:
                b.select()
                b.config(state = "disabled")
        else:
            for b in self.bchecks:
                b.deselect()
                b.config(state = "normal")


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

        self.vall = Tk.IntVar(self.parent)
        self.all = Tk.Checkbutton(self.parent, text = "ALL", variable = self.vall, command = self.select_all)
        self.all.grid(row = 2, column = 0)
        self.botao = Tk.Button(self.parent, text = "Update", command = self.doit)
        self.botao.grid(row = 2, column = 1)
