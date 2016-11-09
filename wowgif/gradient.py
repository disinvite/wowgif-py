from PIL import Image

def get_delta(c1,c2,height):
    return tuple(1.0 * (c2[i] - c1[i]) / height for i in range(len(c1)))

def step_one(c,d):
    return list(c[i] + d[i] for i in range(len(c)))

def frame(canvas,top_color,bottom_color):
    img = Image.new('RGB',(canvas['x'],canvas['y']))
    pix = img.load()
    delta = get_delta(top_color,bottom_color,canvas['y'])

    row_color = list(top_color)
    for y in range(canvas['y']):
        c = map(int,row_color)
        for x in range(canvas['x']):
            pix[x,y] = tuple(c)

        row_color = step_one(row_color,delta)

    return img
