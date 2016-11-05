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

def color_map():    
    r = ([255] * 255) + range(255,0,-1) + ([0] * 510) + range(0,255) + ([255] * 255)
    g = range(0,255) + ([255] * 510) + range(255,0,-1) + ([0] * 510)
    b = ([0] * 510) + range(0,255) + ([255] * 510) + range(255,0,-1)
    return zip(r,g,b)
    
def get_color(c):
    where = int(1530.0 * c / 255)
    cm = color_map()
    return cm[where]
    
def create(in_file,out_file):
    temp_id = id_generator()
    grayscale = Image.open(in_file).convert('L')
    luminance = grayscale.load()
    
    x,y = grayscale.size
    output = Image.new('RGB', grayscale.size)
    pixels = output.load()

    for row in range(0,x):
        for col in range(0,y):
            pixels[row,col] = get_color(luminance[row,col])
    
    output.save(out_file, "PNG")

if __name__ == '__main__':
    create('test/2336_012.jpg','test/hi_man.png')
