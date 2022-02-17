from re import L
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys

args=sys.argv[1:]
if len(args)==0:
    print("Provide file name to graph")
    exit()

filename=args[0]
file=open(filename,"r",encoding='ISO-8859–1')
lines=file.readlines()

start_v=float(lines[1].split(": ")[1][:-2])
end_v=float(lines[-1].split(": ")[1][:-2])
internal_resistance=float(lines[2].split(": ")[1][:-6])
battname=lines[0].strip()
datalines=lines[3:-1]

voltlines=list()
amplines=list()
ahlines=list()

voltlines.append(start_v)
amplines.append(0)
ahlines.append(0)

avgcurr=0
totalcapacity=0
totalenergy=0
lastt=float(datalines[0].split(',')[2])
for line in datalines:
    splitline=line.split(',')
    volts=float(splitline[0])
    amps=float(splitline[1])
    ah=float(splitline[3])
    time=float(splitline[2])
    totalenergy=float(splitline[4][:-2])

    tdiff=time-lastt
    lastt=time

    ahlines.append(ah)
    voltlines.append(volts)
    amplines.append(amps)
    avgcurr+=amps
    totalcapacity=ah

voltlines.append(end_v)
amplines.append(0)
ahlines.append(totalcapacity)

avgcurr/=len(datalines)
plt.rcParams["figure.figsize"] = [11,6]
fig, ax = plt.subplots()

ax2 = ax.twinx()
ax2.plot(ahlines, amplines, color='red')
ax.plot(ahlines, voltlines,color='green',)
ax2.set(ylabel='current (A)')
ax.set_zorder(ax2.get_zorder()+1)
ax.patch.set_visible(False)

ax2.set_ylim(0,5)
ax.set_ylim(2.5,4.3)

ax.set(xlabel='capacity (Ah)', ylabel='voltage (V)',
       title=f'{battname} @ {round(avgcurr,2)} A')
ax.grid()

rows=[[internal_resistance,round(start_v,2),round(end_v,2),round(totalcapacity,3),round(totalenergy,3)]]
columns=["Internal resistance (mOhm)","Start voltage (V)","End voltage (V)","Total capacity (Ah)","Total energy (Wh)"]
plt.subplots_adjust(bottom=0.25)
table=plt.table(cellText = rows,colLabels=columns,bbox=[-0.1,-0.35,1.2,0.2])
table.auto_set_font_size(False)
table.set_fontsize(9)
plt.savefig(filename[:-4]+".png", dpi=200)