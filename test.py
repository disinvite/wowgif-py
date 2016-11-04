import math
import wowgif

def dummy_up_one():
    rotate_pts = [10 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    zoom_pts = [300 for i in range(360)]
    y_pts = [200 + 30 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    return [{'text': 'HEY NOW', 'color': '#f80000', 'zoom': zoom_pts[i], 'angle': rotate_pts[i], 'x':200, 'y': y_pts[i]} for i in range(0,360,10)]
    
def dummy_up_two():
    x_pts = [260 + 30 * math.cos(i * math.pi / 180.0) for i in range(0,360)]
    return [{'text': 'lil guy', 'color': '#c0c0ff', 'zoom': 100, 'angle': 0, 'x':x_pts[i], 'y': 350} for i in range(0,360,10)]

def swerve():
    objs = [{'text': 'HI THERE', 'color': '#{0:02x}0000'.format(10 + 4*i), 'zoom': 200 + 2*i, 'angle': 0, 'x':200, 'y':250-2*i} for i in range(50)]
    objs[-1]['color'] = '#ffffff'
    
    x_delta = [i + 1 for i in range(-36,36,2)]
    def apply_delta(obj,which,frame):
        x = x_delta[frame] * (which / (1.0 * len(objs)))
        print '{}, {} --> {} / {}'.format(which,frame,x_delta[frame],x)
        obj['x'] += x
        return obj
        
    frames = []
    for frame_no in range(36):
        t_objs = [apply_delta(obj.copy(),i,frame_no) for i,obj in enumerate(objs)]
        frames.append({'objs': t_objs})
        
    return frames
    
if __name__ == '__main__':
    canvas = {'filename': 's', 'x': 400, 'y': 400}
    #xx = zip(dummy_up_one(),dummy_up_two())
    #frames = [ {'objs': x} for x in xx ]
    frames = swerve()
    wowgif.create(canvas,frames)
