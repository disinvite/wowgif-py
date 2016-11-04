import string
import random
from subprocess import Popen
from PIL import Image, ImageFont, ImageDraw

def id_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_stamp(textin):
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
    
    image = Image.new('RGB',(x,y))
    for i,text in enumerate(lines):
        draw = ImageDraw.Draw(image)
        pos = ( int(0.5 * (x - sizes[i][0])), y_offset[i] )
        draw.text(pos, text, font=font, fill=(244,34,114,0))
    
    return image.crop(image.getbbox())

def render(image,obj):
    s = get_stamp(obj['text'])
    x,y = s.size
    aspect = 1.0*x/y
    
    resize_dim = (obj['zoom'],int(obj['zoom'] / aspect))
    s = s.resize(resize_dim,Image.BILINEAR)
    s = s.rotate(obj['angle'],Image.BILINEAR,1)
    
    tx = int(obj['x'] - (0.5 * s.size[0]))
    ty = int(obj['y'] - (0.5 * s.size[1]))
    
    image.paste( s, (tx,ty) )
    return image

# my own crappy animation pipeline
def one_frame(canvas,frame):
    image = Image.new('RGB',(canvas['x'],canvas['y']))
    for obj in frame['objs']:
        image = render(image,obj)
    return image

def ffmpeg(frame_prefix,filename):
    x = 'H:/work2/wowgif/temp/{}%d.png'.format(frame_prefix)
    process = Popen(['D:/bin/ffmpeg-20151126-git-72eaf72-win64-static/bin/ffmpeg.exe',
    '-loglevel','panic',
    '-y','-r','30','-i',x,filename])
    
def create(canvas,frames):
    temp_id = id_generator()
    for i, frame in enumerate(frames):
        x = one_frame(canvas,frame)
        filename = 'temp/{}{}.png'.format(temp_id,i)
        x.save(filename, "PNG")
        
    outfile = '{}.gif'.format(canvas['filename'])
    ffmpeg(temp_id,outfile)
