from donkeycar.parts.keras import KerasLinear
from PIL import Image
import numpy as np


input_shape = (120, 160, 3)
roi_crop = (0, 0)

kl = KerasLinear(input_shape=input_shape, roi_crop=roi_crop)
#kl.load('/home/pi/mycar/models/mypilot20.h5')
img = Image.open('./528.jpg')
img = np.array(img)
#print(img.shape)
out = kl.run(img)
print(out)