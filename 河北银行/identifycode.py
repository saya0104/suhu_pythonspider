from __future__ import print_function
import os, sys
from PIL import Image

im=Image.open(r"C:\Users\suhu\Desktop\code\python_spider\河北银行\img\origna_img5.png")
region=im.crop((470,250,540,282))
region=region.convert('L')


region.show()

