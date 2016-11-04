import math
import string
import random
from subprocess import Popen
from PIL import Image

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def convert(frame_prefix,filename):
    im = 'bin/convert.exe'
    x = 'temp/{}*.png'.format(frame_prefix)
    process = Popen([im,'-delay','3','-loop','0',x,filename])
    process.wait()

def get_color(i,n):
    x = (2 * math.pi * i / n)
    return (
        max(0,int( math.cos(x) * 255)),
        max(0,int( math.sin(x) * 255)),
        max(0,int(-math.sin(x) * 255))
    )
    
def create(in_file,out_file):
    temp_id = id_generator()
    x = Image.open(in_file).convert('L')
    
    colors = [get_color(i,36) for i in range(36)]
    for i,c in enumerate(colors):
        print '{} {}'.format(i,c)
    
    x.save(out_file, "PNG")

if __name__ == '__main__':
    create('test/2336_012.jpg','test/hi_man.png')
