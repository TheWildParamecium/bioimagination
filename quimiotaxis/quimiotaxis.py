#import math
from math import sqrt
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#It calculates the distance between two points in a 2D space
def calculate_distance(point1, point2):
    return sqrt(   (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 )


def follow_bacteria(bacteria, whiteblood):
    whiteblood_updated = whiteblood.copy()
    for cell in whiteblood_updated:

        #These conditions regulate the controlled movement of white cells (if white cells are near of the bacteria)
        if   (bacteria[0] - cell[0]) > 0:
            cell[0] += 10 * (float(1)/ sqrt(calculate_distance(bacteria, cell))) 
        elif (bacteria[0] - cell[0]) < 0:
            cell[0] -= 10 * (float(1)/ sqrt(calculate_distance(bacteria, cell)))
        if   (bacteria[1] - cell[1]) > 0:
            cell[1] += 10 * (float(1)/ sqrt(calculate_distance(bacteria, cell)))
        elif (bacteria[1] - cell[1]) < 0:
            cell[1] -= 10 * (float(1)/ sqrt(calculate_distance(bacteria, cell)))

    
        #These conditions regulate the random movement of white cells (if white cells are far from the bacteria)
        cell[0] += random.randint(-5, 5) * (1 - float(1)/ sqrt(calculate_distance(bacteria, cell)))
        cell[1] += random.randint(-5, 5) * (1 - float(1)/ sqrt(calculate_distance(bacteria, cell)))
    return whiteblood_updated


#It searches the nearest white cell from the bacteria current position
def search_nearest(bacteria, whiteblood):
    nearest_index = 0
    distance = calculate_distance(bacteria, whiteblood[0])
    for i in range(len(whiteblood)):
        new_distance = calculate_distance(bacteria, whiteblood[i])
        
        if new_distance < distance:
            distance = new_distance
            nearest_index = i

    return nearest_index


def scape_of_nearest_cell(bacteria, cell):
    bacteria_updated = bacteria.copy()

    #These conditions regulate the controlled movement of the bacteria (if white cells are near of the bacteria)
    if (bacteria[0] - cell[0]) > 0:
        bacteria_updated[0] += 10 * (float(1)/ sqrt(calculate_distance(bacteria, cell)))
    elif (bacteria[0] - cell[0]) < 0:
        bacteria_updated[0] -= 10 * (float(1)/ sqrt(calculate_distance(bacteria, cell)))
    else:
        bacteria_updated[0] += 10 * (float(1)/ sqrt(calculate_distance(bacteria, cell))) * random.choice([-1,1])

    if (bacteria[1] - cell[1]) > 0:
        bacteria_updated[1] += 10 * (float(1)/ sqrt(calculate_distance(bacteria, cell)))
    elif (bacteria[1] - cell[1]) < 0:
        bacteria_updated[1] -= 10 * (float(1)/ sqrt(calculate_distance(bacteria, cell)))
    else:
        bacteria_updated[0] += 10 * (float(1)/ sqrt(calculate_distance(bacteria, cell))) * random.choice([-1,1])

    #These conditions regulate the random movement of the bacteria (if white cells are far from the bacteria)
    bacteria_updated[0] += random.randint(-5, 5) * (1 - float(1)/ sqrt(calculate_distance(bacteria, cell)))
    bacteria_updated[1] += random.randint(-5, 5) * (1 - float(1)/ sqrt(calculate_distance(bacteria, cell)))

    return bacteria_updated

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(9, 9))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(-1000, 1000) 
ax.set_ylim(-1000, 1000)

# Create white cell points
n_cells = 120
bacteria = [0, 0]
cellsx = [(x*0 + random.randint(-1000, 1000)) for x in range(n_cells)]
cellsy = [(y*0 + random.randint(-1000, 1000)) for y in range(n_cells)]
cells = [list(a) for a in zip(cellsx, cellsy)] #It creates a list of cells positions [[X1,Y1],[X2, Y2],[Xn, Yn]]

# Construct the scatter which we will update during animation
categories = ([0] + [1]*n_cells)
colormap = np.array(['r', 'b'])

scat = ax.scatter(
    [bacteria[0]] + list(map(lambda x: x[0], cells)),
    [bacteria[1]] + list(map(lambda y: y[1], cells)),
    c = colormap[categories],
    alpha = 0.8
    )

def update(frame_number, bacteria, cells):
    # Get an index which we can use to re-spawn the oldest frame
    current_index = frame_number % n_cells

    #Bacteria flees from the nearest white cell
    nearest_index = search_nearest(bacteria, cells)
    new_pos = scape_of_nearest_cell(bacteria, cells[nearest_index])
    bacteria.append(new_pos[0])
    bacteria.append(new_pos[1])
    bacteria.pop(0)
    bacteria.pop(0)
    
    #Then white cells follow bacteria
    cells = follow_bacteria(bacteria, cells)
    
    # Update the scatter collection of point on the screen/image
    scat.set_offsets([bacteria] + cells)
    
# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, fargs=(bacteria, cells), interval=1, frames = 1000, repeat = False)

animation.save('quimiotaxis.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()

