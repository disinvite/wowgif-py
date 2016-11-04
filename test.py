import math
import wowgif

def dummy_up_one():
    rotate_pts = [10 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    zoom_pts = [300 for i in range(360)]
    y_pts = [200 + 30 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    return [{'text': 'HEY NOW', 'zoom': zoom_pts[i], 'angle': rotate_pts[i], 'x':200, 'y': y_pts[i]} for i in range(0,360,10)]
    
def dummy_up_two():
    x_pts = [260 + 30 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    return [{'text': 'lil guy', 'zoom': 100, 'angle': 0, 'x':x_pts[i], 'y': 350} for i in range(0,360,10)]

if __name__ == '__main__':    
    canvas = {'filename': 'hi', 'x': 400, 'y': 400}
    xx = zip(dummy_up_one(),dummy_up_two())
    frames = [ {'objs': x} for x in xx ]
    wowgif.create(canvas,frames)
