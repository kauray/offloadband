"""
==============
Eventplot Demo
==============

An eventplot showing sequences of events with various line properties.
The plot is shown in both horizontal and vertical orientations.
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from numpy import genfromtxt

matplotlib.rcParams['font.size'] = 10.0

# Fixing random state for reproducibility
#np.random.seed(19680801)


# create random data
data1= np.loadtxt('/home/kauray/Desktop/data.csv', delimiter=",")
#data1 = genfromtxt('/home/kauray/Desktop/data.csv', delimiter=',')
print(data1)
print(len(data1))

#data1[10] = data1[10]+0.2
#print(data1[10])

# set different colors for each set of positions
colors1 = ['C{}'.format(i) for i in range(11)]
#print(len(colors1))

# set different line properties for each set of positions
# note that some overlap
lineoffsets1 = [1,2,3,4,5,6,7,8,9,10,11,]
linelengths1 = [0.3]*11

fig, axs = plt.subplots()

plt.xlabel('Combination of Applications')
plt.xticks(np.arange(1, 12, 1))
plt.ylabel('Running Times (in seconds)')

# create a horizontal plot
#axs[].eventplot(data1, colors=colors1, lineoffsets=lineoffsets1,
                    #linelengths=linelengths1)

# create a vertical plot
axs.eventplot(data1, colors=colors1, lineoffsets=lineoffsets1,
                    linelengths=linelengths1, orientation='vertical')

'''
# create another set of random data.
# the gamma distribution is only used for aesthetic purposes
data2 = np.random.gamma(4, size=[60, 50])

# use individual values for the parameters this time
# these values will be used for all data sets (except lineoffsets2, which
# sets the increment between each data set in this usage)
colors2 = 'black'
lineoffsets2 = 1
linelengths2 = 1

# create a horizontal plot
axs[0, 1].eventplot(data2, colors=colors2, lineoffsets=lineoffsets2,
                    linelengths=linelengths2)


# create a vertical plot
#axs[1, 1].eventplot(data2, colors=colors2, lineoffsets=lineoffsets2,
                    #linelengths=linelengths2, orientation='vertical')
'''
plt.show()
