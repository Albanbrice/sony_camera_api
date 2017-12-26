import pysony
import six
import time
import argparse

parser = argparse.ArgumentParser(prog="bulb_test")

parser.add_argument("time", help="Open shutter for 'x' seconds")
parser.add_argument("-i", "--iso", type=int, dest="iso", help="set iso to 'x'")

options = parser.parse_args()

search = pysony.ControlPoint()
cameras =  search.discover(5)

print("Available cameras: %s" % cameras)
print("")

for x in cameras:
    print("Connecting Camera: %s" % x)
    camera = pysony.SonyAPI(QX_ADDR=x, debug = True)

    mode = camera.getAvailableApiList()

    # For those cameras which need it
    if 'startRecMode' in (mode['result'])[0]:
        camera.startRecMode()
        time.sleep(5)
        mode = camera.getAvailableApiList()

    speed = camera.getAvailableShutterSpeed()
    if 'BULB' in (speed['result'])[1]:
        res = camera.setShutterSpeed('BULB')
        print(res)

        # Note: need to set an ISO in order for 'BULB' to function
        if options.iso:
            res = camera.setIsoSpeedRate(options.iso)
        else:
            res = camera.setIsoSpeedRate('100')

        print("Opening Shutter")
        res = camera.startBulbShooting()

	time.sleep(float(options.time))

        print("Closing Shutter")
        res = camera.stopBulbShooting()
    else:
        print("BULB is not available")

