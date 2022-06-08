import os

def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            Hauptmem=int(line.split()[1])/1024
            Freimem=int(line.split()[3])/1024
            return(Hauptmem, Freimem)
            #return(line.split()[1:4])


print("Hauptspeicher ",getRAMinfo()[0],"Freierspeicher ",getRAMinfo()[1])
