import serial
ser = serial.Serial('/dev/ttyUSB1')
initialPosition = [0.0,0.0,0.0]
deg2meters = 110967 # https://msi.nga.mil
while True:
    NMEAline = str(ser.readline())
    if 'GGA' in NMEAline:
        csvlist = NMEAline.split(',')
        lat = float(list(csvlist)[2])
        long = float(list(csvlist)[4])
        elev = float(list(csvlist)[9])
        if initialPosition == [0.0,0.0,0.0]:
            initialPosition = [lat,long,elev]
            print('initialPosition set')
        dLat = round((initialPosition[0]-lat)*deg2meters,5)
        dLong = round((initialPosition[1]-long)*deg2meters,5)
        dElev = round((initialPosition[2]-elev),5)
        # print('Movement = Lat: ' + str(lat) + ' Long: ' + str(long) + ' Elev: ' + str(elev))
        print('Movement = Lat: ' + str(dLat) + ' Long: ' + str(dLong) + ' Elev: ' + str(dElev))
        ser.flush()

