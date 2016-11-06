import string
import random
from subprocess import Popen
from PIL import Image

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    
def convert(frame_prefix,filename):
    im = 'bin/convert.exe'
    x = 'test/{}_*.png'.format(frame_prefix)
    process = Popen([im,'-delay','3','-loop','0',x,filename])
    process.wait()
    
def get_stars(howmany,x_dim,y_dim):
    return [ [random.randint(0,x_dim - 1), random.randint(0,y_dim - 1)] for _ in range(howmany) ]
    
def frame(farstars,midstars,bigstars,img = None):
    if img is None:
        img = Image.new('RGB',(400,400),(29,29,35))
    pix = img.load()
    
    cube_3 = [(x,y) for x in range(0,3) for y in range(0,3)]
    cube_2 = [(x,y) for x in range(0,2) for y in range(0,2)]

        
    for x,y in farstars:
        x = int(x)
        try:
            pix[x,y] = (57,83,201)
            pix[133+x,y] = (57,83,201)
            pix[267+x,y] = (57,83,201)
        except IndexError:
            continue

    for x,y in midstars:
        x = int(x)
        for dx,dy in cube_2:
            try:
                pix[x+dx,y+dy] = (88,161,241)
                pix[200+x+dx,y+dy] = (88,161,241)
            except IndexError:
                continue
                
    for x,y in bigstars:
        x = int(x)
        for dx,dy in cube_3:
            try:
                pix[x+dx,y+dy] = (192,206,255)
            except IndexError:
                continue
    
    return img
    
def stargen(num_frames):
    farstars = get_stars(30,133,400)
    midstars = get_stars(30,200,400)
    bigstars = get_stars(16,400,400)
    
    for i in range(num_frames):
        img = frame(farstars,midstars,bigstars)
        
        for i,_ in enumerate(farstars):
            farstars[i][0] = (farstars[i][0] + (133.0 / num_frames)) % 133
            
        for i,_ in enumerate(midstars):
            midstars[i][0] = (midstars[i][0] + (200.0 / num_frames)) % 200
            
        for i,_ in enumerate(bigstars):
            bigstars[i][0] = (bigstars[i][0] + (400.0 / num_frames)) % 400

        yield img
    
def create(out_file):
    sg = stargen(60)

    i = 0
    for img in sg:
        img.save('test/zz_{0:04d}.png'.format(i),'PNG')
        i += 1

    convert('zz',out_file)

if __name__ == '__main__':
    random.seed(0)
    create('stars.gif')
