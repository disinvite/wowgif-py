import string
import random
from subprocess import Popen
from PIL import Image, ImageFont, ImageDraw

stamp_memo = {}

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
    
def get_stamp(textin,color):
    key = (textin + color).upper()
    if key in stamp_memo:
        return stamp_memo[key]

    font = ImageFont.truetype("impact.ttf", 200)
    
    lines = textin.split('\n')
    
    sizes = [font.getsize(text) for text in lines]
    x = max(t[0] for t in sizes)
    y = sum(t[1] for t in sizes)
    
    ty = 0
    y_offset = []
    for t in sizes[::-1]:
        y_offset += [ty]
        ty += t[1]
    
    image = Image.new('RGBA',(x,y), (0,0,0,0))
    for i,text in enumerate(lines):
        draw = ImageDraw.Draw(image)
        pos = ( int(0.5 * (x - sizes[i][0])), y_offset[i] )
        draw.text(pos, text, font=font, fill=color_hex_to_rgba(color))
    
    output = image.crop(image.getbbox())
    stamp_memo[key] = output
    return output

def render(image,obj):
    s = get_stamp(obj['text'],obj['color'])
    x,y = s.size
    aspect = 1.0*x/y
    
    resize_dim = (obj['zoom'],int(obj['zoom'] / aspect))
    s = s.resize(resize_dim,Image.BILINEAR)
    s = s.rotate(obj['angle'],Image.BILINEAR,1)
    
    tx = int(obj['x'] - (0.5 * s.size[0]))
    ty = int(obj['y'] - (0.5 * s.size[1]))
    
    r, g, b, a = s.split()
    pp1 = Image.merge("RGB", (r, g, b))
    mask = Image.merge("L", (a,))
    
    image.paste(pp1, (tx,ty), mask )
    return image

# my own crappy animation pipeline
def one_frame(canvas,frame,image=None):
    if image is None:
        image = Image.new('RGB',(canvas['x'],canvas['y']))
        
    for obj in frame['objs']:
        image = render(image,obj)
    return image
    
def convert(frame_prefix,filename):
    im = '/opt/local/bin/convert'
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
