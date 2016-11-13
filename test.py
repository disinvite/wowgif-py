import math
from wowgif import wowgif, wowtext, starfield, gradient

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
    
def sinusoid(max,n_frames,ofs = 0):
    dx = 360 / n_frames
    return [ofs + (max * math.cos(i * math.pi / 180.0)) for i in range(0,360,dx)]
    
def trails(canvas,movement = 'bob'):
    if movement == 'bob':
        angles = sinusoid(2,60,-10)
        sizes = [int(0.88 * canvas['x'])] * 60
        ys = sinusoid(int(0.1 * canvas['y']),30,int(0.45 * canvas['y']))
        ys = ys + ys
        ys = ys[50:60] + ys[0:50] # bump it a little to get that nice oscillation
    elif movement == 'swirl':
        angles = sinusoid(10,60)
        sizes = [350] * 60
        ys = sinusoid(40,60,190)
        ys = ys[50:60] + ys[0:50] # bump it a little to get that nice oscillation
    elif movement == 'twirl':
        s_max = int(0.6 * canvas['x'])
        s_int = int(0.3 * canvas['x'])

        sizes = map(int,sinusoid(s_int,60,s_max))
        ys = [canvas['y'] / 2] * 60
        angles = sinusoid(10,60,-12)
    elif movement == 'zoom':
        s_max = int(0.6 * canvas['x'])
        s_int = int(0.5 * canvas['x'])
        angles = [0] * canvas['frames']
        sizes = map(int,sinusoid(s_int,canvas['frames'],s_max))
        ys = [canvas['y'] / 2] * canvas['frames']
    
    center_x = canvas['x'] / 2

    frames = []
    for i in range(canvas['frames']):
        text = 'this is\nnot going well'
        di = [(i + (canvas['frames'] - j)) % canvas['frames'] for j in range(1,4)]
        
        main   = {'text': text, 'color': '#ffa3ca', 'zoom': sizes[i], 'angle': angles[i], 'x':center_x, 'y': ys[i]}
        shadow1 = {'text': text, 'color': '#ff89b2', 'zoom': sizes[di[0]], 'angle': angles[di[0]], 'x':center_x, 'y': ys[di[0]]}
        shadow2 = {'text': text, 'color': '#ff89b2', 'zoom': sizes[di[1]], 'angle': angles[di[1]], 'x':center_x, 'y': ys[di[1]]}
        shadow3 = {'text': text, 'color': '#ff89b2', 'zoom': sizes[di[2]], 'angle': angles[di[2]], 'x':center_x, 'y': ys[di[2]]}

        # text stroke
        x0 = {'text': text, 'color': '#ff1668', 'zoom': sizes[i], 'angle': angles[i], 'x':center_x-1, 'y': ys[i]}
        x1 = {'text': text, 'color': '#ff1668', 'zoom': sizes[i], 'angle': angles[i], 'x':center_x+1, 'y': ys[i]}
        y0 = {'text': text, 'color': '#ff1668', 'zoom': sizes[i], 'angle': angles[i], 'x':center_x, 'y': ys[i]-1}
        y1 = {'text': text, 'color': '#ff1668', 'zoom': sizes[i], 'angle': angles[i], 'x':center_x, 'y': ys[i]+1}

        #objs = [shadow1, shadow2, main]
        objs = [shadow1, shadow2, shadow3, x0,x1,y0,y1, main]
        frames.append({'objs': objs })
    
    return frames
    
def combined(movement):
    canvas = {'filename': 'xyz', 'x': 300, 'y': 300}
    frames = trails(canvas,movement)
    sg = starfield.stargen(60,canvas)
    starframes = list(sg)
    
    temp_id = wowgif.id_generator()
    for i, frame in enumerate(frames):
        img = starframes[i]
        img = wowtext.one_frame(canvas,frame,img)
        filename = 'temp/{0}_{1:04d}.png'.format(temp_id,i)
        img.save(filename, "PNG")
        
    outfile = '{}.gif'.format(canvas['filename'])
    wowgif.convert(temp_id,outfile)
    
def miami(movement):
    #(170,231,232)
    #(219,169,206)

    canvas = {'filename': 'xyz', 'x': 400, 'y': 400, 'frames': 60}
    frames = trails(canvas,movement)
    frames = frames[32:52] # what if we don't want a loop
    bg = gradient.frame(canvas, (170,231,232), (219,169,206))

    temp_id = wowgif.id_generator()
    for i, frame in enumerate(frames):
        img = bg.copy()
        img = wowtext.one_frame(canvas,frame,img)
        filename = 'temp/{0}_{1:04d}.png'.format(temp_id,i)
        img.save(filename, "PNG")
        
    outfile = '{}.gif'.format(canvas['filename'])
    wowgif.convert(temp_id,outfile)

if __name__ == '__main__':
    miami('zoom')
    #combined('bob')
    #canvas = {'filename': 's', 'x': 400, 'y': 400}
    #xx = zip(dummy_up_one(),dummy_up_two())
    #frames = [ {'objs': x} for x in xx ]
    #frames = trails()
    #wowgif.create(canvas,frames)
