import Tkinter as Tk, datetime as dt


def nospace(s):
    s2 = ""
    for c in s:
        if c != ' ':
            s2 += c
    return s2

def Print2(src, s):
    t = ""
    for i in xrange(len(s)):
        t += s[i]
        if i%189 == 188:
            src.insert(Tk.END, t)
            src.see(Tk.END)
            t = ""
    if len(t):
        src.insert(Tk.END, t)
        src.see(Tk.END)
    fh = open("log.txt",'a')
    fh.write("%s >>> %s\n"%(str(dt.datetime.now()),s))
    fh.close()
