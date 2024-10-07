import time
import matplotlib.pyplot as plt
import numpy as np
import vpython as vp
import params
import graphics
from classes.vector import vector
from classes import Optimizer
from classes import Surface


vp.scene.caption = f'''
    Press the Play button to start the optimization process.
    Right click/ctrl+click to rotate the camera
    shift+left click to drag
    scroll to zoom
    '''

is_paused = True
def toggle_pause():
    """Toggles the pause state."""
    global is_paused
    if is_paused:
        is_paused = False
        pause_button.text = "Pause"
    else:
        is_paused = True
        pause_button.text = "Play"



if __name__ == '__main__':
    vp.canvas(background=vp.vector(0.9, 0.9, 0.9), width=800, height=800)


    global pause_button
    pause_button = vp.button(text="Play", bind=lambda: toggle_pause())
    

    surface = Surface.Surface(params.CHOSEN_FUNCTION, params.X_MIN, params.X_MAX, params.Y_MIN, params.Y_MAX)
    rendering = graphics.Graphics(surface)
    rendering.plot_surface()
    
    start_x = -11
    start_y = -13
    
    graddesc = Optimizer.GradientDescent(start_x, start_y, surface=surface, lr=params.LEARNING_RATE, color=vp.color.red)
    momentum = Optimizer.Momentum(start_x, start_y, surface=surface, lr=params.LEARNING_RATE, color=vp.color.blue, gamma=0.95)
    nesterov = Optimizer.Nesterov(start_x, start_y, surface=surface, lr=params.LEARNING_RATE, color=vp.color.orange, gamma=0.95)
    adagrad = Optimizer.AdaGrad(start_x, start_y, surface=surface, lr=params.ADAGRAD_LEARNING_RATE, color=vp.color.green)
    rmsprop = Optimizer.RMSProp(start_x, start_y, surface=surface, lr=params.RMSPROP_LEARNING_RATE, color=vp.color.yellow, gamma=0.9)
    adam = Optimizer.Adam(start_x, start_y, surface=surface, lr=params.ADAM_LEARNING_RATE, color=vp.color.purple, beta_1=0.7, beta_2=0.999)
    
    rendering.add_optimizer(graddesc)
    rendering.add_optimizer(nesterov)
    rendering.add_optimizer(momentum)
    rendering.add_optimizer(adagrad)
    rendering.add_optimizer(rmsprop)
    rendering.add_optimizer(adam)

    rendering.labeling()
    
    t = 0
    while True:
        vp.rate(20)
        while is_paused:
            vp.rate(20)

        del_v = []
        t += params.dt
        
        for optim in rendering.optimizers:
            del_v.append(optim.step())


        rendering.render_optimizers()

        if any([v < 1e-4 for v in del_v]):
            # write something on the canvas
            idx = np.argmin(del_v)
            optim = rendering.optimizers[idx]
            p = optim.position
            vp.text(text=f'Local minimum reached by {optim}!', pos=vp.vector(p.x, p.y, p.z + 20), height=0.5, color=vp.color.black)
            time.sleep(20)
            break
        
        if t > params.T:
            break