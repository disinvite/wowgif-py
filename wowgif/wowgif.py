import string
import random
from subprocess import Popen
from PIL import Image, ImageFont, ImageDraw

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def color_hex_to_rgba(x):
    if x.startswith('#'):
        x = x[1:]
    def f(y):
        try:
            return int(y,16)
        except ValueError:
            return 0
            
    return ( f(x[0:2]), f(x[2:4]), f(x[4:6]), 255 ) 
    
def convert(frame_prefix,filename):
    im = 'bin/convert.exe'
    x = 'temp/{}*.png'.format(frame_prefix)
    process = Popen([im,'-delay','3','-loop','0',x,filename])
    process.wait()
    
def create(canvas,frames):
    temp_id = id_generator()
    for i, frame in enumerate(frames):
        x = one_frame(canvas,frame)
        filename = 'temp/{0}_{1:04d}.png'.format(temp_id,i)
        x.save(filename, "PNG")
        
    outfile = '{}.gif'.format(canvas['filename'])
    convert(temp_id,outfile)
