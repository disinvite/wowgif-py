import math
from subprocess import Popen
from PIL import Image, ImageFont, ImageDraw

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
    x = 'H:/work2/wowgif/test/a/{}%d.png'.format(frame_prefix)
    process = Popen(['D:/bin/ffmpeg-20151126-git-72eaf72-win64-static/bin/ffmpeg.exe',
    '-loglevel','panic',
    '-y','-r','30','-i',x,filename])
    
def create(canvas,frames):
    for i, frame in enumerate(frames):
        x = one_frame(canvas,frame)
        filename = 'test/a/bla{}.png'.format(i)
        x.save(filename, "PNG")
        
    ffmpeg('bla','test.gif')
    
def dummy_up_one():
    rotate_pts = [10 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    zoom_pts = [300 for i in range(360)]
    y_pts = [200 + 30 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    return [{'text': 'HEY NOW', 'zoom': zoom_pts[i], 'angle': rotate_pts[i], 'x':200, 'y': y_pts[i]} for i in range(0,360,10)]
    
def dummy_up_two():
    x_pts = [260 + 30 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    return [{'text': 'lil guy', 'zoom': 100, 'angle': 0, 'x':x_pts[i], 'y': 350} for i in range(0,360,10)]
    
if __name__ == '__main__':
    canvas = {'x': 400, 'y': 400}
    xx = zip(dummy_up_one(),dummy_up_two())
    frames = [ {'objs': x} for x in xx ]
    create(canvas,frames)
    ffmpeg('bla','test.gif')
    
