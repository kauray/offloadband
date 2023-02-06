import numpy as np
import os
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import subprocess

def calculateprobability(dataserver, minserver, maxserver):
    #divide into 5 intervals between min and max
    interval = (maxserver - minserver) / 5
    count = [0] * 5

    points = []
    points.append(minserver)
    intervalranges = [minserver + (i * interval) for i in range(0, 5)]
    #print(intervalranges)

    #calculate frequence in each interval
    for i in range(len(dataserver)):
        for j in range(5):
            if j < 4:
                if dataserver[i] >= intervalranges[j] and dataserver[i] < intervalranges[j+1]:
                    count[j] = count[j] + 1
                    break
            else:
                if dataserver[i] >= intervalranges[j]:
                    count[j] = count[j] + 1
                    break

    #print(count)
    #print(sum(count))
    #calculate probabilities
    pr = [0] * 5
    for i in range(5):
        pr[i] = count[i] / sum(count)

    return pr, count
    #input()
    
#setup the device parameter constants

pmax = 5
latencym = 100
tmax = 50
slottime = 20
batteryenergy = 28800

#band calculation
batteryenergyband = 28800

#// constants for p_device
ccf = 0.00642
xcf = 1500
xck = 0.01
xcu = 0.05
p0xcpu = 0.332

pcpu = ccf * xcf * (xck    + xcu) + p0xcpu

e = 2.718281828459045;
ib = pcpu / 0.6;
b21 = -0.043;
b22 = -14.275;
vsoc = 0.96; #// vsoc = cb / cfull * 1 V
b23 = 0.154;
#//const double voc;
kd = 0.019;

b11 = -0.265;
b12 = -61.649;
b13 = -2.039;
b14 = 5.276;
b15 = -4.173;
b16 = 1.654;
b17 = 3.356;

p_device = pcpu

pcpulittle = 1
pcpubig = 5
#pcpuserver = 122;
pcpuserver = 80

#band specific power
pcpuserver4g = 5;
pcpuserver5glow = 40;
pcpuserver5gmmwave = 80;
#band specific power

voc = b11 * pow(e, (b12 * vsoc)) + b13 * pow(vsoc, 4) + b14 * pow(vsoc, 3) + b15 * pow(vsoc, 2) + b16 * vsoc + b17

e_loss = slottime  * (ib * ib * b21* pow(e, ((b22*vsoc) + b23))) + (ib * voc * (pow(ib, kd) - 1))

econsumedlittle = slottime  * pcpulittle * e_loss
econsumedbig = slottime  * pcpubig * e_loss
econsumedserver = slottime  * pcpuserver * e_loss

#band specific power

econsumedserver4g = slottime  * pcpuserver4g * e_loss;
econsumedserver5glow = slottime  * pcpuserver5glow * e_loss;
econsumedserver5gmmwave = slottime  * pcpuserver5gmmwave * e_loss;

#band specific power

#temperature
tenv = 32
rcpuenv = 35.8
rbatenv = 7.58
rcpubat = 78.8
pbatlittle = 6.67
pbatbig = 33.33

tempbatterylittle = tenv + (rcpuenv * rbatenv) / (rbatenv + rcpubat + rcpuenv) * pcpulittle # +  ((rcpuenv * rbatenv) + (rcpubat*rbatenv)) / (rbatenv + rcpubat + rcpuenv) * pbatlittle;

tempbatterybig = tenv + (rcpuenv * rbatenv) / (rbatenv + rcpubat + rcpuenv) * pcpubig # + ((rcpuenv * rbatenv) + (rcpubat*rbatenv)) / (rbatenv + rcpubat + rcpuenv) * pbatbig;

#read data stochastic
dataserver= np.loadtxt('data.csv', delimiter=",")
datalittle= np.loadtxt('data2.csv', delimiter=",")
databig= np.loadtxt('data3.csv', delimiter=",")

print(dataserver)

#randomly pick one time of day
randindex = np.random.randint(0, 11)
dataserver = dataserver[randindex]
datalittle = datalittle[randindex]
databig = databig[randindex]

sorteddataserver = np.sort(dataserver)
sorteddatalittle = np.sort(datalittle)
sorteddatabig = np.sort(databig)

#calucluate probabilities of ranges and pass as parameter
print(min(dataserver), max(dataserver), np.median(dataserver))
minserver = min(dataserver)
maxserver = max(dataserver)

prserver, countserver = calculateprobability(dataserver, minserver, maxserver)

minserver = min(datalittle)
maxserver = max(datalittle)

prlittle, countlittle = calculateprobability(datalittle, minserver, maxserver)

minserver = min(databig)
maxserver = max(databig)

prbig, countbig = calculateprobability(databig, minserver, maxserver)

#concatenate the probabilities as string parameters
pr1 = ','

for i in range(len(prserver)):
    pr1 = pr1 + 'p1' + str(i+1) + '=' + str(prserver[i]) + ','

for i in range(len(prlittle)):
    pr1 = pr1 + 'p2' + str(i+1) + '=' + str(prlittle[i]) + ','

for i in range(len(prserver)):
    pr1 = pr1 + 'p3' + str(i+1) + '=' + str(prbig[i]) + ','

pr1 = pr1[:-1]

#print(pr1)
#input()
##print(prserver)
##print(prlittle)
##print(prbig)
##
##input()

#generate strategy in prism
#os.system('')

output = subprocess.Popen('/home/kauray/Desktop/prism-games-3.0-linux64/bin/prism model.pm props.props -const tenv=32,pbat=7.5' + pr1 + ' -exportstrat rps2_strat3.dot -exportstates model.sta ', shell = True)
output.wait()

output = subprocess.Popen('mv adv.tra advoffload.tra', shell = True)
output.wait()

output = subprocess.Popen('/home/kauray/Desktop/prism-games-3.0-linux64/bin/prism modelband.pm propsband.props -const tenv=32,pbat=7.5' + pr1 + ' -exportstrat rps2_strat3.dot -exportstates modelband.sta ', shell = True)
output.wait()
#print(output)
#input()

#print("Press Any Key To Continue")
#input()

output = subprocess.Popen('mv adv.tra advband.tra', shell = True)
output.wait()

output = subprocess.Popen('mv advoffload.tra adv.tra', shell = True)
output.wait()

#adv.tra strategy for scheduler
#advband.tra band selection strategy

#print(output)
#print("Models Done")

output = subprocess.Popen('cut -f 2 -d : model.sta | sed \'s/.$//; s/^.//\' > output.csv', shell=True)
output.wait()

filestra = open('adv.tra', 'r')

actiondict = {}

for line in filestra:
    #print(line)
    tokens = line.split()
    if len(tokens) == 0:
        break
    #print(tokens)
    actiondict[int(tokens[0])] = tokens[1]
    #print(key, val)

filestra.close()

reader = csv.reader(open('output.csv', 'r'))
states = {}

i = -1
for row in reader:
    if i == -1:
        i = i + 1
        continue
    states[tuple(map(int, row))] = i
    i = i + 1

'''print dictionary    
for key, value in states.items():
    print(key, value)
'''

#process models and adv for band
output = subprocess.Popen('cut -f 2 -d : modelband.sta | sed \'s/.$//; s/^.//\' > outputband.csv', shell=True)
output.wait()

filestra = open('advband.tra', 'r')

actiondictband = {}

for line in filestra:
    #print(line)
    tokens = line.split()
    if len(tokens) == 0:
        break
    #print(tokens)
    actiondictband[int(tokens[0])] = tokens[1]
    #print(key, val)

filestra.close()

reader = csv.reader(open('outputband.csv', 'r'))
statesband = {}

i = -1
for row in reader:
    if i == -1:
        i = i + 1
        continue
    statesband[tuple(map(int, row))] = i
    i = i + 1
#process models and adv for band

#print(output)

#state format
#(turn,execution,tmig,batteryenergy,temp,mig,core,dtime,latency)

turn = 0
execution = -1
tmig = 0
temp1 = tenv
temp2 = tenv
mig = 0
core = 0
latency = 0

latarray = []
temparray = []
temparray2 = []
energyarray = []
mecarray = []

#bandexecution
bandarray = []
bandenergyarray = []
throughputarray = []
bandexecution = 0

#run simulation for iterations tmax
for i in range(tmax):

    #calculate action according to the dictionary
    #for task execution, turn = 0, for core, turn = 2
    #print(states)
    print((turn, execution, tmig, batteryenergy, temp1, temp2, mig, core, i, latency))
    if (turn, execution, tmig, batteryenergy, temp1, temp2, mig, core, i, latency) in states:
        print('Good')
    else:
        print('Nay')
    #input()
    #simulate task offload / ondevice decision

    print(i)
    if turn == 0 :
        #find task execution
        if (turn, execution, tmig, batteryenergy, temp1, temp2, mig, core, i, latency) in states:
            stateid = states[(turn, execution, tmig, batteryenergy, temp1, temp2, mig, core, i, latency)]
            act = actiondict[stateid]
            print(act)
            #print(len(act))
            if act == 'serverex':
                execution = 1
            elif act == 'deviceex':
                #print('inside')
                execution = 0
            elif act == 'retaindevice' or act == 'retainserver':
                tmig = 0
            elif act == 'migtoserver':
                tmig = 1
                execution = 1
            elif act == 'migtodevice':
                tmig = 2
                execution = 0
            #print('Yay')
            #get action from stateid

    #input()
    tmig = 0
    turn = 1
    
    if execution == 0 and turn == 1:
        if (turn, execution, tmig, batteryenergy, temp1, temp2, mig, core, i, latency) in states:
            stateid = states[(turn, execution, tmig, batteryenergy, temp1, temp2, mig, core, i, latency)]
            act = actiondict[stateid]
            print(act)
            if act == 'core1':
                core = 1
            elif act == 'core2':
                core = 2
            elif act == 'retaincore1' or act == 'retaincore2':
                mig = 0
            elif act == 'migonetwo':
                mig = 1
                core = 2
            elif act == 'migtwoone':
                mig = 2
                core = 1

            turn = 2

    if execution == 0 and turn == 2:
        if core == 1:
            latency = np.random.choice(np.arange(0, 5), p=prlittle)

            index1 = 0
            index2 = 0
            
            for j in range(0, 5):
                if latency == j:
                    break
                if latency <= j:
                    index1 = index1 + countlittle[j]

            index2 = index2 + countlittle[j]

            #print(index1, index2)
            #find random latency
            lt = sorteddatalittle[np.random.randint(index1, index2 + 1)]
            
        elif core == 2:
            latency = np.random.choice(np.arange(0, 5), p=prbig)

            index1 = 0
            index2 = 0
            
            for j in range(0, 5):
                if latency == j:
                    break
                if latency <= j:
                    index1 = index1 + countbig[j]

            index2 = index2 + countbig[j]
            print(index1, index2)
            #find random latency
            lt = sorteddatabig[np.random.randint(index1, index2 + 1)]

        if core == 1:
            etdt = batteryenergy - econsumedlittle
            batteryenergy = math.floor(etdt)
            temp1 = math.ceil(tempbatterylittle)
        elif core == 2:
            etdt = batteryenergy - econsumedbig
            batteryenergy = math.floor(etdt)
            temp2 = math.ceil(tempbatterybig)

        mig = 0
        

    if execution == 1 and turn == 1:
        latency = np.random.choice(np.arange(0, 5), p=prserver)

        index1 = 0
        index2 = 0
        
        for j in range(0, 5):
            if latency == j:
                break
            if latency <= j:
                index1 = index1 + countserver[j]

        print(index1, index2)

        index2 = index2 + countserver[j]

        #find random latency
        lt = sorteddataserver[np.random.randint(index1, index2 + 1)]
        thvalue = sorteddataserver[np.random.randint(index1, index2 + 1)]

        #find band from advband.tra
        if (0,bandexecution,32,i,0) not in statesband:
            for key,value in statesband.items():
                print(key, value)
                input()
            print("Error")
            input()
        stateidband = statesband[(0,bandexecution,32,i,0)]
        actband = actiondictband[stateidband]

        if actband == 'band4g':
            bandexecution = 0
        elif actband == 'band5glow':
            bandexecution = 1
        elif actband == 'band5gmmwave':
            bandexecution = 2
        #find band from advband.tra
        etdt = batteryenergy - econsumedserver
        batteryenergy = math.floor(etdt)
        temp1 = math.ceil(tenv)
        temp2 = math.ceil(tenv)

        #find band energy
        etdtband = batteryenergyband - econsumedserver4g
        batteryenergyband = math.floor(etdtband)

        etdtband = batteryenergyband - econsumedserver5glow
        batteryenergyband = math.floor(etdtband)

        etdtband = batteryenergyband - econsumedserver5gmmwave
        batteryenergyband = math.floor(etdtband)

    turn = 0

    '''
    if execution == 1:
        latency = np.random.choice(numpy.arange(0, 5), p=prserver)
    elif execution == 0:
        if core == 1:
            latency = np.random.choice(numpy.arange(0, 5), p=prlittle)
        elif core == 2:
            latency = np.random.choice(numpy.arange(0, 5), p=prbig)

    print(execution)
    print(latency)
    #print(prserver)
    #calculate energy consumed according to iterationss
    etdt = batteryenergy - econsumed
    batteryenergy = math.floor(etdt)

    if execution == 1:
        #execution is server
        #sample execution time from the random choice of data
        maxrange = len(dataserver)
        runtime = dataserver[np.random.randint(0, maxrange)]
        #print(runtime)

    #reset tmig to 0
    '''
    mig = 0
    #tmig = 0
    #print(tempbattery)
    #print(etdt)

    latarray.append(lt)
    temparray.append(temp1)
    temparray2.append(temp2)
    energyarray.append(batteryenergy)
    mecarray.append(execution)
    bandenergyarray.append(batteryenergyband)
    if execution == 1:
        bandarray.append(bandexecution)
        throughputarray.append(thvalue)
    else:
        bandarray.append(-1)
        throughputarray.append(-1)

print(latarray)
print(temparray)
print(temparray2)
print(energyarray)
print(bandenergyarray)
print(bandarray)
print(throughputarray)

timeslot = range(1,51)

energyarray = [e / 10000 for e in energyarray]
bandenergyarray = [e / 10000 for e in bandenergyarray]
#plt.plot(timeslot, latarray, linewidth = 1.0)

#f = plt.figure(figsize=(5.8, 3.2))

plt.xlabel('Time Slot')
plt.ylabel('Temperature in degree C')

plt.plot(timeslot, temparray, 
         color='red',   
         linewidth=1.0,  
         linestyle='-' 
        )
plt.plot(timeslot, temparray2, 
         color='green',   
         linewidth=1.0,  
         linestyle='--' 
        )
plt.legend(["Core1", "Core2"])
'''
plt.plot(timeslot, mecarray, 
         color='blue',   
         linewidth=1.0,  
         linestyle='dotted'
        )
'''
##plt.set_figheight(10)
##plt.set_figwidth(15)
plt.show()
#f.savefig("temperature.pdf")

fig, ax1 = plt.subplots()

#f = plt.figure(figsize=(5.8, 3.2))

ax2 = ax1.twinx()
ax1.plot(timeslot, latarray, 'b-')
ax2.plot(timeslot, mecarray, 'r--')

#plt.xlabel('Time Slot')
#plt.ylabel('Runtime in seconds')

ax1.set_xlabel('Time Slot')
ax1.set_ylabel('Latency', color='b')
ax2.set_ylabel('Execution Location', color='r')

ax1.legend(["Latency", "Location (0 - Device, 1 - Server)"], loc = 'upper left')
ax2.legend(["Location (0 - Device, 1 - Server)"])
##plt.plot(timeslot, latarray, 
##         color='blue',   
##         linewidth=1.0,  
##         linestyle='--' 
##        )
##
##plt.xlabel('x')
##plt.ylabel('y')

##plt.plot(timeslot, mecarray, 
##         color='red',   
##         linewidth=1.0,  
##         linestyle='--' 
##        )

plt.show()

#f.savefig("latency.pdf")

fig, ax1 = plt.subplots()

#f = plt.figure(figsize=(5.8, 3.2))

ax2 = ax1.twinx()
ax1.plot(timeslot, latarray, 'b-')
ax2.plot(timeslot, energyarray, 'r--')

#plt.xlabel('Time Slot')
#plt.ylabel('Runtime in seconds')

ax1.set_xlabel('Time Slot')
ax1.set_ylabel('Latency', color='b')
ax2.set_ylabel('Energy', color='r')

ax1.legend(["Latency", "Location (0 - Device, 1 - Server)"])
ax2.legend(["Energy"], loc = 'upper left')

plt.show()

#f.savefig("latencyenergy.pdf")

'''
energy plots

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.plot(timeslot, energyarray, 'b-')
ax2.plot(timeslot, bandenergyarray, 'r--')

#plt.xlabel('Time Slot')
#plt.ylabel('Runtime in seconds')

ax1.set_xlabel('Time Slot')
ax1.set_ylabel('Energy', color='b')
ax2.set_ylabel('Energy with Band', color='r')

ax1.legend(["Energy"])
ax2.legend(["Energy with Band"], loc = 'upper left')

plt.show()
'''

fig = plt.subplots()

#f = plt.figure(figsize=(5.8, 3.2))

energyarray = energyarray[0::10]
bandenergyarray = bandenergyarray[0::10]

barWidth = 0.25
br1 = np.arange(len(energyarray))
br2 = [x + barWidth for x in br1]

plt.bar(br1,energyarray,label="Energy with Band Selection",color='b',width=barWidth)
plt.bar(br2,bandenergyarray,label="Energy", color='g',width=barWidth)

plt.legend(loc='lower left')
plt.xticks([r + barWidth for r in range(len(energyarray))],
        ['0', '10', '20', '30', '40'])
plt.xlabel('Slot')
plt.ylabel('Energy')

#plt.title('Details')

# Print the chart
plt.show()

#f.savefig("energyband.pdf")


####band plots

fig, ax1 = plt.subplots()

#plt.figure(figsize=(5.8, 3.2))

ax2 = ax1.twinx()
ax1.plot(timeslot, bandarray, 'b-')
ax2.plot(timeslot, throughputarray, 'r--')

#plt.xlabel('Time Slot')
#plt.ylabel('Runtime in seconds')

ax1.set_xlabel('Time Slot')
ax1.set_ylabel('Band Selected', color='b')
ax2.set_ylabel('Throughput', color='r')

ax1.legend(["Band Selected"])
ax2.legend(["Throughput"])

plt.show()
#f.savefig("bandthroughput.pdf")

###band bar plot

fig = plt.subplots()

#f = plt.figure(figsize=(5.8, 3.2))

bandselected = []
bandselected.append(' ')

for i in range(len(bandarray)):
    if bandarray[i] == 0:
        bandselected.append('band4g')
    elif bandarray[i] == 1:
        bandselected.append('band5glow')
    elif bandarray[i] == 2:
        bandselected.append('band5gmmwave')
    elif bandarray[i] == -1:
        bandselected.append('device')

print(bandselected)

barWidth = 0.5
br1 = np.arange(len(bandselected))
br2 = [x + barWidth for x in br1]

plt.bar(br1,bandselected,color='b',width=barWidth)
#plt.bar(br2,throughputarray,label="Energy with Band", color='g',width=barWidth)

plt.legend()
plt.xlabel('Slot')
plt.ylabel('Band Selected')

# Print the chart
plt.show()

#f.savefig("bandselected.pdf")
