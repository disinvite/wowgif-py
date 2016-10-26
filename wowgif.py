import math
from PIL import Image, ImageFont, ImageDraw

def get_stamp(lines):
    font = ImageFont.truetype("times.ttf", 1000)
    
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

def rotated_frame(text,horiz_size,angle):
    s = get_stamp(text)
    x,y = s.size
    aspect = 1.0*x/y
    
    blank_size = 800 # fixed canvas size
    resize_dim = (horiz_size,int(horiz_size / aspect))
    s = s.resize(resize_dim,Image.BILINEAR)
    s = s.rotate(angle,Image.BILINEAR,1)
    
    image = Image.new('RGB',(blank_size,blank_size))
    
    tx = int(0.5 * (blank_size - s.size[0]))
    ty = int(0.5 * (blank_size - s.size[1]))
    
    image.paste( s, (tx,ty) )
    return image
    
if __name__ == '__main__':
    rotate_pts = [10 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    zoom_pts   = [100 * math.sin(i * math.pi / 180.0) for i in range(0,360)]
    ns = range(0,360,10)
    
    for i, v in enumerate(ns):
        x = rotated_frame(['hi','there'],500 + int(zoom_pts[v]), rotate_pts[v])
        filename = 'test/a/bla{}.png'.format(i)
        x.save(filename, "PNG")
