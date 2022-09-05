import pandas as pd
import matplotlib.pyplot as plt
import random
from itertools import count
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

def animate(i): # Funció que va fent el gràfic cada vegada amb més valors en les llistes dels eixos
    data = pd.read_csv('data_realtime.csv')
    x = data['x_value']
    y1 = data['total_1']
    y2 = data['total_2']

    plt.cla() # Clear axis perquè el gràfic es mantingui amb el mateix color

    plt.plot(x, y1, label='Channel 1')
    plt.plot(x, y2, label='Channel 2')

    plt.legend(loc='upper left')
    plt.tight_layout()


anim = FuncAnimation(plt.gcf(), animate, interval=1000) # interval en milisegons, és a dir, actualitzem cada 1 segon.

plt.tight_layout()
plt.show()