import matplotlib.colors as cl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import numpy as np
import random as rd

run = False
width, height = 100, 100

vacant, typea, typeb = xrange(3)
colorsList = ['white','purple','black']
CustomCmap = cl.ListedColormap(colorsList)
bounds = [-0.5,0.5,1.5,2.5]
norm = cl.BoundaryNorm(bounds,CustomCmap.N)

ratea, rateb, recratea, recrateb = 0.1, 0.1, 0.05, 0.05
n = 1000

fig,ax = plt.subplots(1)
fig.subplots_adjust(bottom=0.2)
ax.set_aspect('equal'); ax.axis([0,width,0,height])
ax.set_xticks(())
ax.set_yticks(())

def init():
    global im, time, config, movesa, movesb, recoverya, recoveryb
    
    time = 0
                  
    config = np.zeros([width, height])
    config[height/2, width/2] = typea #initial configuration A
    config[height/2 + 1, width/2] = typeb #initial configuration B

    movesa = [[height/2, width/2 + 1],[height/2, width/2 - 1],
                    [height/2 - 1, width/2]] #initial available moves for type A
                    
    movesb = [[height/2 + 1, width/2 + 1],[height/2 + 1, width/2 - 1],
                    [height/2 + 2, width/2]] #initial available moves for type B
                    
    recoverya = [[height/2, width/2]] #initial possible recovery states for type A
    recoveryb = [[height/2 + 1, width/2]] #initial possible recovery states for type B

    im = ax.imshow(config,cmap=CustomCmap)
    ax.set_title('t = ' + str(time))
    
def step():
    global im, t, time, config, movesa, movesb, recoverya, recoveryb

    ta, treca = rd.expovariate(ratea*len(movesa)), rd.expovariate(recratea*len(recoverya))
    tb, trecb = rd.expovariate(rateb*len(movesb)), rd.expovariate(recrateb*len(recoveryb))    
    
    if recoverya == [] and recoveryb != []:
        t = min(tb,trecb)
        mb, mrecb = rd.randrange(len(movesb)), rd.randrange(len(recoveryb))
        
        if t == tb: #growth of B
            [m1,m2] = movesb[mb]
            config[m1,m2] = typeb
            movesb[:] = [x for x in movesb if x != [m1, m2]]
            recoveryb.append([m1,m2])
            nextmovesb = []
            for dy in xrange(-1, 2,2):
                if config[(m1+dy)%height,(m2)%width] == vacant:
                    nextmovesb.append([(m1+dy)%height,(m2)%width])
            for dx in xrange(-1, 2,2):        
                if config[(m1)%height,(m2+dx)%width] == vacant:
                    nextmovesb.append([(m1)%height,(m2+dx)%width])
            movesb.extend(nextmovesb)
            
        elif t == trecb: #recovery of B
            [m1,m2] = recoveryb[mrecb]
            config[m1,m2] = vacant
            recoveryb[:] = [x for x in recoveryb if x != [m1,m2]]
            k = 0
            for dy in xrange(-1, 2,2):
                if config[(m1+dy)%height,(m2)%width] == vacant:
                    movesb.remove([(m1+dy)%height,(m2)%width])
                    k += 1
            for dx in xrange(-1, 2,2):        
                if config[(m1)%height,(m2+dx)%width] == vacant:
                    movesb.remove([(m1)%height,(m2+dx)%width])
                    k += 1
            for i in xrange(4-k):
                movesb.append([m1,m2])
        
    elif recoveryb == [] and recoverya != []:
        t = min(ta,treca)
        ma, mreca = rd.randrange(len(movesa)), rd.randrange(len(recoverya))
        
        if t == ta: #growth of A
            [m1,m2] = movesa[ma]
            config[m1,m2] = typea
            movesa[:] = [x for x in movesa if x != [m1, m2]]
            recoverya.append([m1,m2])
            nextmovesa = []
            for dy in xrange(-1, 2,2):
                if config[(m1+dy)%height,(m2)%width] == vacant:
                    nextmovesa.append([(m1+dy)%height,(m2)%width])
            for dx in xrange(-1, 2,2):        
                if config[(m1)%height,(m2+dx)%width] == vacant:
                    nextmovesa.append([(m1)%height,(m2+dx)%width])
            movesa.extend(nextmovesa)
        
        elif t == treca: #recovery of A
            [m1,m2] = recoverya[mreca]
            config[m1,m2] = vacant
            recoverya[:] = [x for x in recoverya if x != [m1,m2]]
            k = 0
            for dy in xrange(-1, 2,2):
                if config[(m1+dy)%height,(m2)%width] == vacant:
                    movesa.remove([(m1+dy)%height,(m2)%width])
                    k += 1
            for dx in xrange(-1, 2,2):        
                if config[(m1)%height,(m2+dx)%width] == vacant:
                    movesa.remove([(m1)%height,(m2+dx)%width])
                    k += 1
            for i in xrange(4-k):
                movesa.append([m1,m2])
                
    else:
        t = min(ta,treca,tb,trecb)
        ma, mreca = rd.randrange(len(movesa)), rd.randrange(len(recoverya))
        mb, mrecb = rd.randrange(len(movesb)), rd.randrange(len(recoveryb))
        
        if t == ta: #growth of A
            [m1,m2] = movesa[ma]
            config[m1,m2] = typea
            movesa[:] = [x for x in movesa if x != [m1, m2]]
            movesb[:] = [x for x in movesb if x != [m1, m2]]
            recoverya.append([m1,m2])
            nextmovesa = []
            for dy in xrange(-1, 2,2):
                if config[(m1+dy)%height,(m2)%width] == vacant:
                    nextmovesa.append([(m1+dy)%height,(m2)%width])
            for dx in xrange(-1, 2,2):        
                if config[(m1)%height,(m2+dx)%width] == vacant:
                    nextmovesa.append([(m1)%height,(m2+dx)%width])
            movesa.extend(nextmovesa)
        
        elif t == treca: #recovery of A
            [m1,m2] = recoverya[mreca]
            config[m1,m2] = vacant
            recoverya[:] = [x for x in recoverya if x != [m1,m2]]
            k, l = 0, 0
            for dy in xrange(-1, 2,2):
                if config[(m1+dy)%height,(m2)%width] == vacant:
                    movesa.remove([(m1+dy)%height,(m2)%width])
                    k += 1
                elif config[(m1+dy)%height,(m2)%width] == typeb:
                    l += 1
            for dx in xrange(-1, 2,2):        
                if config[(m1)%height,(m2+dx)%width] == vacant:
                    movesa.remove([(m1)%height,(m2+dx)%width])
                    k += 1
                elif config[(m1)%height,(m2+dx)%width] == typeb:
                    l += 1
            for i in xrange(4-l-k): # no. A
                movesa.append([m1,m2])
            for j in xrange(l): # no. B
                movesb.append([m1,m2])
            
        elif t == tb: #growth of B
            [m1,m2] = movesb[mb]
            config[m1,m2] = typeb
            movesa[:] = [x for x in movesa if x != [m1, m2]]
            movesb[:] = [x for x in movesb if x != [m1, m2]]
            recoveryb.append([m1,m2])
            nextmovesb = []
            for dy in xrange(-1, 2,2):
                if config[(m1+dy)%height,(m2)%width] == vacant:
                    nextmovesb.append([(m1+dy)%height,(m2)%width])
            for dx in xrange(-1, 2,2):        
                if config[(m1)%height,(m2+dx)%width] == vacant:
                    nextmovesb.append([(m1)%height,(m2+dx)%width])
            movesb.extend(nextmovesb)
            
        elif t == trecb: #recovery of B
            [m1,m2] = recoveryb[mrecb]
            config[m1,m2] = vacant
            recoveryb[:] = [x for x in recoveryb if x != [m1,m2]]
            k, l = 0, 0
            for dy in xrange(-1, 2,2):
                if config[(m1+dy)%height,(m2)%width] == vacant:
                    movesb.remove([(m1+dy)%height,(m2)%width])
                    l += 1
                elif config[(m1+dy)%height,(m2)%width] == typea:
                    k += 1
            for dx in xrange(-1, 2,2):        
                if config[(m1)%height,(m2+dx)%width] == vacant:
                    movesb.remove([(m1)%height,(m2+dx)%width])
                    l += 1
                elif config[(m1)%height,(m2+dx)%width] == typea:
                    k += 1
            for i in xrange(4-l-k):
                movesb.append([m1,m2])
            for j in xrange(k):
                movesa.append([m1,m2])
    time += t
    
    im.set_data(config)
    ax.set_title('t = ' + str(time))

def skip(n):
    global recoverya, recoveryb
    for i in range(n):
        if recoverya == [] and recoveryb == []:
            break
        step()
        
    
class GUI(object):
    
    def Reset(self, event):
        global run
        run = False
        init()
        fig.canvas.draw_idle()
        
    def Next(self, event):
        step()
        fig.canvas.draw_idle()
    
    def Skip(self, event):
        global n
        skip(n)
        
    def Run(self, event):
        global run, t
        if run == False:
            run = True
        while run == True:
            step()
            plt.pause(t)
    
    def Pause(self, event):
        global run
        if run == True:
            run = False
      
callback = GUI()
axreset = plt.axes([0.81, 0.05, 0.1, 0.075])
axskip = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.59, 0.05, 0.1, 0.075])
axstart = plt.axes([0.48, 0.05, 0.1, 0.075])
axpause = plt.axes([0.37, 0.05, 0.1, 0.075])
axratea = plt.axes([0.1,0.087,0.2,0.037])
axrateb = plt.axes([0.1,0.05,0.2,0.037])
bnext = Button(axnext, 'Next'); bnext.on_clicked(callback.Next)
breset = Button(axreset, 'Reset'); breset.on_clicked(callback.Reset)
bstart = Button(axstart, 'Start'); bstart.on_clicked(callback.Run)
bpause = Button(axpause, 'Pause'); bpause.on_clicked(callback.Pause)
bskip = Button(axskip, 'Skip'); bskip.on_clicked(callback.Skip)
sratea = Slider(axratea, 'Rate A', 0.005, 0.5, valinit=ratea)
srateb = Slider(axrateb, 'Rate B', 0.005, 0.5, valinit=rateb)

def handle_close(evt):
    global run
    run = False

fig.canvas.mpl_connect('close_event', handle_close)

def update(val):
    global ratea, rateb
    ratea = sratea.val
    rateb = srateb.val
sratea.on_changed(update)
srateb.on_changed(update)

fig.show()
init()