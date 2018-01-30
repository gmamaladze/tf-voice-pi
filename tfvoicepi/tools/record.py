import os
import tfvoicepi.voicecmd

isRaspberryPi = (os.uname()[4][:3] == 'arm')
print("Is raspberry pi:", isRaspberryPi)

if isRaspberryPi:
    import mic_pi as mic
else:
    import tfvoicepi.mic

raw_stream = tfvoicepi.voicecmd.get_raw(tfvoicepi.mic.get_mic_data(), 0.00001)

counter = 0
for current in raw_stream:
    if current is None:
        print (".")
    else:
        print ("*")
        f = open(str(counter) + ".raw", 'wb')
        with f:
            buff = memoryview(current).tobytes()
            f.write(buff)
        counter += 1
