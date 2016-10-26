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
    
    blank_size = max(horiz_size,horiz_size / aspect)*2
    resize_dim = (horiz_size,int(horiz_size / aspect))
    image = Image.new('RGB',(blank_size,blank_size))
    
    tx = int(0.5 * (blank_size - resize_dim[0]))
    ty = int(0.5 * (blank_size - resize_dim[1]))
    
    image.paste( s.resize(resize_dim,Image.BILINEAR), (tx,ty) )
    image = image.rotate(angle,Image.BILINEAR)
    return image
    #image.save('test/bla.png', "PNG")
    
if __name__ == '__main__':
    ns = range(-45,45,4)
    for i in range(len(ns)):
        x = rotated_frame('WORLD',400, ns[i])
        filename = 'test/a/bla{}.png'.format(i)
        x.save(filename, "PNG")
