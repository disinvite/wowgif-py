import math
from subprocess import Popen
from PIL import Image, ImageFont, ImageDraw

def get_stamp(lines):
    font = ImageFont.truetype("impact.ttf", 200)
    
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

def rotated_frame(text,horiz_size,angle,pos_x,pos_y):
    s = get_stamp(text)
    x,y = s.size
    aspect = 1.0*x/y
    
    blank_size = 400 # fixed canvas size
    resize_dim = (horiz_size,int(horiz_size / aspect))
    s = s.resize(resize_dim,Image.BILINEAR)
    s = s.rotate(angle,Image.BILINEAR,1)
    
    image = Image.new('RGB',(blank_size,blank_size))
    
    tx = int(pos_x - (0.5 * s.size[0]))
    ty = int(pos_y - (0.5 * s.size[1]))
    
    image.paste( s, (tx,ty) )
    return image
    
def ffmpeg(frame_prefix,filename):
    x = 'H:/work2/wowgif/test/a/{}%d.png'.format(frame_prefix)
    process = Popen(['D:/bin/ffmpeg-20151126-git-72eaf72-win64-static/bin/ffmpeg.exe',
    '-loglevel','panic',
    '-y','-r','30','-i',x,filename])
    
def create(frames):
    for i, frame in enumerate(frames):
        x = rotated_frame(['UP \'N DOWN'], frame['zoom'], frame['angle'], frame['x'], frame['y'])
        filename = 'test/a/bla{}.png'.format(i)
        x.save(filename, "PNG")
        
    ffmpeg('bla','test.gif')
    
if __name__ == '__main__':
    rotate_pts = [10 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    #zoom_pts   = [int( 300 + (50 * math.sin(i * math.pi / 180.0)) ) for i in range(0,360)]
    zoom_pts = [300 for i in range(360)]
    y_pts = [200 + 30 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    
    frames = [{'zoom': zoom_pts[i], 'angle': rotate_pts[i], 'x':200, 'y': y_pts[i]} for i in range(0,360,10)]
    create(frames)
    ffmpeg('bla','test.gif')
    
