import matplotlib.colors as cl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import numpy as np
import random as rd

run = False
width, height = 100, 100
vacant, typea, typeb = xrange(3)
colorsList = ['white','black','purple']
CustomCmap = cl.ListedColormap(colorsList)
ratea, rateb = 0.1, 0.1
n = 1000

fig,ax = plt.subplots(1)
fig.subplots_adjust(bottom=0.2)
ax.set_aspect('equal'); ax.axis([0,width,0,height])
ax.set_xticks(())
ax.set_yticks(())

def init():
    global im, time, config, movesa, movesb
    
    time = 0
    
    config = np.zeros([width, height])
    config[height/2, width/2] = typea #initial configuration A
    config[height/2 + 1, width/2] = typeb #initial configuration B

    movesa = [[height/2, width/2 + 1],[height/2, width/2 - 1],
                    [height/2 - 1, width/2]] #initial available moves for type A
                    
    movesb = [[height/2 + 1, width/2 + 1],[height/2 + 1, width/2 - 1],
                    [height/2 + 2, width/2]] #initial available moves for type B
                    
    im = ax.imshow(config,cmap=CustomCmap)
    ax.set_title('t = ' + str(time))
    
def step():
    global im, t, time, config, movesa, movesb
    
    if len(movesa) == 0:
        ta = np.inf
        tb = rd.expovariate(rateb*len(movesb))
        mb = rd.randrange(len(movesb))
    elif len(movesb) == 0:
        ta = rd.expovariate(ratea*len(movesa))
        tb = np.inf
        ma = rd.randrange(len(movesa))
    else:
        ta, tb = rd.expovariate(ratea*len(movesa)), rd.expovariate(rateb*len(movesb))
        ma, mb = rd.randrange(len(movesa)), rd.randrange(len(movesb))
    
    t = min(ta,tb) ### or t = rd.expovariate(ratea*len(movesa)+rateb*len(movesb)) & choose move with probability
    time += t
    
    if t == ta:
        [m1,m2] = movesa[ma]
        config[m1,m2] = typea
        movesa[:] = [x for x in movesa if x != [m1, m2]]
        movesb[:] = [x for x in movesb if x != [m1, m2]]
        nextmovesa = []
        for dy in xrange(-1, 2,2):
            if config[(m1+dy)%height,(m2)%width] == vacant:
                nextmovesa.append([(m1+dy)%height,(m2)%width])
        for dx in xrange(-1, 2,2):        
            if config[(m1)%height,(m2+dx)%width] == vacant:
                nextmovesa.append([(m1)%height,(m2+dx)%width])
        movesa.extend(nextmovesa)
        
    elif t == tb:
        [m1,m2] = movesb[mb]
        config[m1,m2] = typeb
        movesa[:] = [x for x in movesa if x != [m1, m2]]
        movesb[:] = [x for x in movesb if x != [m1, m2]]
        nextmovesb = []
        for dy in xrange(-1, 2,2):
            if config[(m1+dy)%height,(m2)%width] == vacant:
                nextmovesb.append([(m1+dy)%height,(m2)%width])
        for dx in xrange(-1, 2,2):        
            if config[(m1)%height,(m2+dx)%width] == vacant:
                nextmovesb.append([(m1)%height,(m2+dx)%width])
        movesb.extend(nextmovesb)
        
    im.set_data(config)
    ax.set_title('t = ' + str(time))

def skip(n):
    for i in range(n):
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