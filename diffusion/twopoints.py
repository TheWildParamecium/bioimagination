import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(-300, 300) 
ax.set_ylim(-300, 300)

# Create particle point's positions in the graph, splitted in two clusters
n_points = 200
particles = np.zeros((n_points), dtype=[('x', int, 1),
                                        ('y', int, 1),
                                        ('x2', int, 1),
                                        ('y2', int, 1)
                                      ])

particles['x2'] = particles['x2'] + 50 
particles['y2'] = particles['y2'] + 50

# Construct the scatter which we will update during animation
categories = ([0]*n_points + [1]*n_points )
colormap = np.array(['r', 'b'])

scat = ax.scatter(np.concatenate((particles['x'], particles['x2']), axis=0),
                  np.concatenate((particles['y'], particles['y2']), axis=0),
                  c = colormap[categories],
                  alpha = 0.5
                  )

def update(frame_number):
    # Get an index which we can use to re-spawn the older points
    current_index = frame_number % n_points

    # Pick new position for older points, by random numbers
    particles['x'] = particles['x'] + np.random.randint(-4, 5, size = n_points)
    particles['y'] = particles['y'] + np.random.randint(-4, 5, size = n_points)
    particles['x2'] = particles['x2'] + np.random.randint(-4, 5, size = n_points)
    particles['y2'] = particles['y2'] + np.random.randint(-4, 5, size = n_points)
    
    # Update the scatter collection
    scat.set_offsets(np.c_[
        np.concatenate((particles['x'], particles['x2']), axis=0),
        np.concatenate((particles['y'], particles['y2']), axis=0)
    ])

    #---------------------------------------------------------------
    #Just for developing and testing purposes
    #print(np.c_[
    #    np.concatenate((particles['x'], particles['x2']), axis=0),
    #    np.concatenate((particles['y'], particles['y2']), axis=0)
    #    ])
    #print("**************")
    #----------------------------------------------------------------


# Construct the animation, using the update function as the animation director, and 
# then saving to a mp4 file
animation = FuncAnimation(fig, update, interval=65, frames = 800, repeat = False)
#animation.save('twopoints_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()