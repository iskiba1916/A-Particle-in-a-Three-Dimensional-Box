import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

Lx, Ly, Lz = 1.0, 1.0, 1.0 
V = Lx * Ly * Lz 

def psi(x, y, z, nx, ny, nz):
    normalization = np.sqrt(8 / V)
    return (
        normalization
        * np.sin(nx * np.pi * x / Lx)
        * np.sin(ny * np.pi * y / Ly)
        * np.sin(nz * np.pi * z / Lz)
    )

N = 30
x = np.linspace(0, Lx, N)
y = np.linspace(0, Ly, N)
z = np.linspace(0, Lz, N)
X, Y, Z = np.meshgrid(x, y, z, indexing="ij")

def compute_prob_density(nx, ny, nz):
    prob_density = np.abs(psi(X, Y, Z, nx, ny, nz)) ** 2
    return prob_density / prob_density.max()

nx, ny, nz = 1, 1, 1
prob_density = compute_prob_density(nx, ny, nz)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

threshold = 0.2
high_prob_indices = prob_density > threshold
sc = ax.scatter(X[high_prob_indices], Y[high_prob_indices], Z[high_prob_indices],
                c=prob_density[high_prob_indices], cmap='viridis', s=5)

def plot_box():

    ax.plot([0, Lx, Lx, 0, 0], [0, 0, Ly, Ly, 0], [0, 0, 0, 0, 0], 'k-')

    ax.plot([0, Lx, Lx, 0, 0], [0, 0, Ly, Ly, 0], [Lz, Lz, Lz, Lz, Lz], 'k-')

    ax.plot([0, 0], [0, 0], [0, Lz], 'k-')
    ax.plot([Lx, Lx], [0, 0], [0, Lz], 'k-')
    ax.plot([0, 0], [Ly, Ly], [0, Lz], 'k-')
    ax.plot([Lx, Lx], [Ly, Ly], [0, Lz], 'k-')

plot_box()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title(f'Gęstość prawdopodobieństwa dla n=({nx}, {ny}, {nz})')

axcolor = 'lightgoldenrodyellow'
ax_nx = plt.axes([0.15, 0.01, 0.65, 0.03], facecolor=axcolor)
ax_ny = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_nz = plt.axes([0.15, 0.09, 0.65, 0.03], facecolor=axcolor)

s_nx = Slider(ax_nx, 'n_x', 1, 5, valinit=nx, valstep=1)
s_ny = Slider(ax_ny, 'n_y', 1, 5, valinit=ny, valstep=1)
s_nz = Slider(ax_nz, 'n_z', 1, 5, valinit=nz, valstep=1)

def update(val):
    global sc
    nx = int(s_nx.val)
    ny = int(s_ny.val)
    nz = int(s_nz.val)

    prob_density = compute_prob_density(nx, ny, nz)
    high_prob_indices = prob_density > threshold

    ax.clear()
    sc = ax.scatter(X[high_prob_indices], Y[high_prob_indices], Z[high_prob_indices],
                    c=prob_density[high_prob_indices], cmap='viridis', s=5)
    plot_box()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Gęstość prawdopodobieństwa dla n=({nx}, {ny}, {nz})')
    fig.canvas.draw_idle()

s_nx.on_changed(update)
s_ny.on_changed(update)
s_nz.on_changed(update)

plt.show()
