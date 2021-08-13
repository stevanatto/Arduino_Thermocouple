#!/usr/bin/env python
# Author: stevanatto@yahoo.com
# Date: 25/11/2019

import glob
import serial
import matplotlib.pyplot as plt
from matplotlib import animation
from time import time
from time import sleep

# Parameters
tmax = 15
ymin = 10
ymax = 240
maxLen = 700 # in samples
sampleRate = 10 # seconds
baudRate = 38400
offset = -1.75

# Global variables
serialConnection = None
lineLabel = None
numPlots = None
start_time = None
t = None
y = None
ax = None
lines = None
anim = None

# Note: look at the Main program!


# Setup Serial Port
def connectme():
    global serialConnection
    serialConnection = None
    try:
        ports = glob.glob('/dev/ttyUSB*')
        for port in ports:
            #print('Trying to connect to: ' + str(port) + ' at ' + str(baudRate) + ' BAUD.')
            serialConnection = serial.Serial(port, baudRate, timeout=sampleRate*(1/4))
            serialConnection.flushInput() # flush any junk left in the serial buffer
            #serialConnection.reset_input_buffer() # for pyserial 3.0+
            print('Connected to ' + str(port) + ' at ' + str(baudRate) + ' BAUD.')
            return True
        print("No port connected!")
        return False
    except:
        print("Error stablishing connection!")
        return False


# Read data 
def read_data():
    global y, numPlots, start_time
    current_time = (time()-start_time)/60 # time [minutes]
    try:
        lineBuffer = serialConnection.readline().decode()
        #print(lineBuffer)
        serialConnection.flushInput() # flush any junk left in the serial buffer
        #serialConnection.reset_input_buffer() # for pyserial 3.0+
        print(str(round(current_time,2)) +':\t' + lineBuffer) # print time and values on shell
        if lineBuffer[0].isnumeric() == False :
                values = [float('NaN')]*numPlots
                lineBuffer = '\t '.join(map(str,values))
    except: # (OSError, serial.SerialException):
        print("Cant't read_data()")
        if connectme():
            lineBuffer = serialConnection.readline().decode() # read Titles
            #print(str(round(current_time,2)) +':\t' + lineBuffer) # print Titles
        values = [float('NaN')]*numPlots
        #values = [ y[n][0] for n in range(numPlots) ]
        #print(values)
        lineBuffer = '\t '.join(map(str,values))
    values = [float(val)+offset for val in lineBuffer.split()]
    return values


# Setup Data & Plot
def setupPlot():
    global lineLabel, numPlots, start_time, t, y, ymin, ymax, ax, lines, anim
    # Get labels of the captures
    sleep(1)
    lineBuffer = serialConnection.readline().decode()
    print('\t' + lineBuffer)
    lineLabel = lineBuffer.split()
    #print('\t' + lineLabel)
    lineLabel = ['T1','T2','T3','T4','T5','T6','T7','T8','T9','T0','Ta','Tb']
    numPlots = len(lineLabel) # number of lines to plot

    # First set up #Setup Data
    start_time = time()
    t = [0*n*sampleRate/60 for n in range(maxLen)]
    y = [[float('NaN')]*maxLen for n in range(numPlots)]
    offsets = [offset for n in range(numPlots)]

    # First set up the figure, the axis, and the plot element we want to animate
    fig = plt.figure()
    ax = plt.axes(xlim=(0, 1), ylim=(ymin,ymax))            
    ax.set_title('Arduino DataLog Read')
    ax.set_xlabel("Time [minutes]")
    ax.set_ylabel("Temperature [Celsius]")
    lines = [ax.plot([], [], lw=2, label=lineLabel[n])[0] for n in range(numPlots)]

    # Setup Animation in the plot
    plotInterval = sampleRate*1000    # Period at which the plot animation updates [ms]
    anim = animation.FuncAnimation(fig,
                                animatePlot,
                                interval=plotInterval,
                                blit=False)#True) 


# animation function.  This is called sequentially
def animatePlot(frame):
    global serialConnection, lineLabel, lines, ax
    values = read_data()  # serialConnection.readline().decode()
    current_time = (time()-start_time)/60 # time [minutes]
    #print(str(round(current_time,2)) +':\t' + '\t '.join(map(str,values))) # print time and values on shell
    t.insert(0,current_time)
    while len(t) > maxLen:
        t.pop(-1)
    try:
        for n in range(numPlots):
            y[n].insert(0,values[n])
            while len(y[n]) > maxLen:
                y[n].pop(-1)
            ax.set_xlim(t[-1], t[0])
            ax.relim()
            ax.grid(True)
            lines[n].set_label(lineLabel[n] +': ' +  str(values[n]))
            ax.legend(loc="upper left")
            lines[n].set_data(t, y[n]) # Refresh Plot
    except:
            print("Error with read values!")
    return lines



# ### Start main program ###

# Setup Serial Port
while connectme() == False :
    sleep(3)

# Setup Data & Plot
sleep(1)
setupPlot()

# Freeze here until close the figure
plt.legend(loc="upper left")
plt.show()
# Call animatePlot() in sampleRate seconds periodicaly.

# Finishing
# TODO: Save the figure. But it is closed here. Maybe at every animatePlot() call.
serialConnection.flushInput() # flush any junk left in the serial buffer
#serialConnection.reset_input_buffer() # for pyserial 3.0+
serialConnection.close()
print("That's all folks!")
