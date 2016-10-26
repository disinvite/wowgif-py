from PIL import Image, ImageFont, ImageDraw

def get_stamp(text):
    font = ImageFont.truetype("times.ttf", 1000)
    x,y = font.getsize(text)
    image = Image.new('RGB',(x,y))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font)
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
    ns = range(-45,45,4)
    for i in range(len(ns)):
        x = rotated_frame('TEST',400 + 20*i, ns[i])
        filename = 'test/a/bla{}.png'.format(i)
        x.save(filename, "PNG")
