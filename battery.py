import serial
import time
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.5)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.2)
    data = arduino.readline()
    return data.decode("utf-8")

def readvoltamps():
    ret=write_read("r")
    splittext=ret.split(",")
    volts=float(splittext[0])
    amps=float(splittext[1])
    return (volts,amps)

def readvolts():
    ret=write_read("r")
    splittext=ret.split(",")
    volts=float(splittext[0])
    amps=float(splittext[1])
    return volts

def getintres():
    write_read("d")
    time.sleep(2)
    start=readvoltamps()
    time.sleep(1)
    write_read("e")
    time.sleep(2)
    end=readvoltamps()
    write_read("d")
    start_v,start_a=start
    end_v,end_a=end
    voltdiff=start_v-end_v
    print(start)
    print(end)
    return int(voltdiff/end_a*1000)

file=open(f"battery_{int(time.time())}.txt","w")
time.sleep(2)
vres=f"starting voltage: {readvolts()} V"
res=f"internal resistance: {getintres()} mOhm"
print(vres)
print(res)
file.write("Battery name\n")
file.write(vres+"\n")
file.write(res+"\n")

write_read("e")
ah=0
wh=0
lasttime=time.time()
starttime=lasttime
while True:
    time.sleep(5)
    readraw=write_read("r")

    splittext=readraw.split(",")
    volts=float(splittext[0])
    amps=float(splittext[1])

    diff=time.time()-lasttime
    lasttime=time.time()
    ah+=amps*diff/60/60
    wh+=amps*volts*diff/60/60
    read=f"{readraw.strip()},{time.time()-starttime},{ah},{wh};"

    if volts<2.8:
        print(f"Ending measurement, voltage too low: {volts}")
        write_read("d")
        time.sleep(5)
        volts=readvolts()
        file.write(f"ending voltage: {volts} V")
        break

    print(read)
    file.write(read+"\n")

file.close()