import random
import numpy as np
import matplotlib.pyplot as plt

N = 5  #Размер карты = 2**N + 1     #5  #10
roughness = 2                  #4  #0.1

def diamond_square(N, roughness):
    size = 2 ** N + 1
    height_map = [[0.0 for i in range(size)] for i in range(size)]

    def set_point(x, y, z):
        height_map[x][y] = z

    def get_point(x, y):
        if x < 0 or x >= size or y < 0 or y >= size:
            return -1
        return height_map[x][y]

    def diamond_step(x, y, step):
        average = (
                          get_point(x - step, y - step) +
                          get_point(x + step, y - step) +
                          get_point(x - step, y + step) +
                          get_point(x + step, y + step)
                  ) / 4.0
        set_point(x, y, average + random.uniform(-step * roughness, step * roughness))

    def square_step(x, y, step):
        average = 0.0
        count = 0

        if get_point(x - step, y) != -1:
            average += get_point(x - step, y)
            count += 1
        if get_point(x + step, y) != -1:
            average += get_point(x + step, y)
            count += 1
        if get_point(x, y - step) != -1:
            average += get_point(x, y - step)
            count += 1
        if get_point(x, y + step) != -1:
            average += get_point(x, y + step)
            count += 1

        set_point(x, y, average / count + random.uniform(-step * roughness, step * roughness))

    def diamond_square_recursion(step):
        half = step // 2

        for y in range(half, size, step):
            for x in range(half, size, step):
                diamond_step(x, y, half)

        for y in range(0, size, half):
            for x in range((y + half) % step, size, step):
                square_step(x, y, half)

        if half > 1:
            diamond_square_recursion(half)

    c1 = random.uniform(0, 1)
    c2 = random.uniform(0, 1)
    c3 = random.uniform(0, 1)
    c4 = random.uniform(0, 1)
    set_point(0, 0, c1)
    set_point(0, size - 1, c2)
    set_point(size - 1, 0, c3)
    set_point(size - 1, size - 1, c4)

    diamond_square_recursion(size - 1)

    return height_map


random.seed(6) #2 #4 #6 #8
height_map = diamond_square(N, roughness)

x = np.arange(0, 2**N + 1)
y = np.arange(0, 2**N + 1)
X, Y = np.meshgrid(x, y)
Z = np.array(height_map)



fig = plt.figure(figsize=(16, 9))

plt.imshow(height_map, cmap='terrain') #для 2д
plt.colorbar()

ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, cmap='terrain') #terrain #magma

ax.set_xlim(0, len(height_map) - 1)
ax.set_ylim(0, len(height_map) - 1)
ax.set_zlim(-50,100)

#ax.set_xlabel('X')
#ax.set_ylabel('Y')
#ax.set_zlabel('Z')

#ax.axis('off')
#ax.grid(False)
plt.subplots_adjust(left=0, right=1, top=2, bottom=-1)

plt.show()