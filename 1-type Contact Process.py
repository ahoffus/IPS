import matplotlib.colors as cl
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import numpy as np
import random as rd

run = False
width, height = 100, 100
vacant, occupied = xrange(2)
colorsList = ['white','black']
CustomCmap = cl.ListedColormap(colorsList)
rate, recrate = 0.1, 0.05
n = 1000

fig,ax = plt.subplots(1)
fig.subplots_adjust(bottom=0.2)
ax.set_aspect('equal'); ax.axis([0,width,0,height])
ax.set_xticks(())
ax.set_yticks(())

def init():
    global im, time, config, moves, recovery
    
    time = 0
    
    config = np.zeros([width, height])
    config[height/2, width/2] = occupied #initial configuration

    moves = [[height/2 + 1, width/2],[height/2 - 1, width/2],
                    [height/2, width/2 + 1],[height/2, width/2 - 1]] #initial available moves
                    
    recovery = [[height/2, width/2]] #initial possible recovery states
    
    im = ax.imshow(config,cmap=CustomCmap)
    ax.set_title('t = ' + str(time))
    
def step():
    global im, t, time, config, moves, recovery
    
    tgrow = rd.expovariate(rate*len(moves))
    trec = rd.expovariate(recrate*len(recovery))
    t = min(tgrow,trec)
    time += t
    
    m, mrec = rd.randrange(len(moves)), rd.randrange(len(recovery))
    
    if t == tgrow: #growth
        [m1,m2] = moves[m]
        config[m1,m2] = occupied
        moves[:] = [x for x in moves if x != [m1,m2]]
        recovery.append([m1,m2])
        nextmoves = []
        for dy in xrange(-1, 2,2):
            if config[(m1+dy)%height,(m2)%width] != occupied:
                nextmoves.append([(m1+dy)%height,(m2)%width])
        for dx in xrange(-1, 2,2):        
            if config[(m1)%height,(m2+dx)%width] != occupied:
                nextmoves.append([(m1)%height,(m2+dx)%width])
        moves.extend(nextmoves)
    
    elif t == trec: #recovery
        [m1,m2] = recovery[mrec]
        config[m1,m2] = vacant
        recovery[:] = [x for x in recovery if x != [m1,m2]]
        k = 0
        for dy in xrange(-1, 2,2):
            if config[(m1+dy)%height,(m2)%width] != occupied:
                moves.remove([(m1+dy)%height,(m2)%width])
                k += 1
        for dx in xrange(-1, 2,2):        
            if config[(m1)%height,(m2+dx)%width] != occupied:
                moves.remove([(m1)%height,(m2+dx)%width])
                k += 1 #delete possible moves from recovered site
        for i in xrange(4-k):
            moves.append([m1,m2]) #add no. neighbours of recovered site
            
    im.set_data(config)
    ax.set_title('t = ' + str(time))
    
def skip(n):
    for i in range(n):
        if recovery == []:
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
axrate = plt.axes([0.1,0.05,0.2,0.075])
bnext = Button(axnext, 'Next'); bnext.on_clicked(callback.Next)
breset = Button(axreset, 'Reset'); breset.on_clicked(callback.Reset)
bstart = Button(axstart, 'Start'); bstart.on_clicked(callback.Run)
bpause = Button(axpause, 'Pause'); bpause.on_clicked(callback.Pause)
bskip = Button(axskip, 'Skip'); bskip.on_clicked(callback.Skip)
srate = Slider(axrate, 'Rate', 0.005, 0.5, valinit=rate)

def handle_close(evt):
    global run
    run = False

fig.canvas.mpl_connect('close_event', handle_close)

def update(val):
    global rate
    rate = srate.val
srate.on_changed(update)

fig.show()
init()