import targetFinder
import usb
import cubeFinder


camera = usb.USBCamera(0)
cube = cubeFinder.cubeFinder(camera)

while 1:
    cube.find()
