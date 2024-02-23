import matplotlib.pyplot as plt
import pygame
from pygame.locals import *
import numpy as np
import time
import matplotlib.backends.backend_agg as agg
from matplotlib.gridspec import GridSpec as griddy
import webbrowser
import random


WIDTH, HEIGHT = 800, 600
# Constants for the three plotters
PLOTTER_WIDTH = 200
PLOTTER_HEIGHT = 150
PLOTTER_X = WIDTH - PLOTTER_WIDTH - 20  # Align to the right
PLOTTER_Y1 = 50
PLOTTER_Y2 = PLOTTER_Y1 + PLOTTER_HEIGHT + 30
PLOTTER_Y3 = PLOTTER_Y2 + PLOTTER_HEIGHT + 30

# Number of data points to display on the graph
num_points = 50

# set initial main graph
main = 1

# Initialize empty lists for x and y values
y_mult = 1
y1 = 1
y2 = 0
y3 = 0
y4 = 0
x_values = []
y1_values = []
y2_values = []
y3_values = []
y4_values = []

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CDT Sim")

# Create a figure and axis for the graph
fig = plt.figure(facecolor = 'black',figsize=(WIDTH*0.0103,HEIGHT*0.0103))
gs = griddy(3,4,figure=fig,hspace=0.4,wspace=0.5)

# Make separate axes
ax1 = fig.add_subplot(gs[:,:-1])
ax4 = fig.add_subplot(gs[2,-1])
ax3 = fig.add_subplot(gs[1,-1])
ax2 = fig.add_subplot(gs[0,-1])
ax5 = fig.add_subplot(gs[:,:],visible=False)


# Set the x-axis limits to accommodate the scrolling effect
ax1.set_xlim(0, num_points)
ax2.set_xlim(0, num_points)
ax3.set_xlim(0, num_points)
ax4.set_xlim(0, num_points)

# Set the retro-style colors
ax1.set_facecolor('black')
ax1.tick_params(axis='x', colors='green')
ax1.tick_params(axis='y', colors='green')
ax1.spines['bottom'].set_color('green')
ax1.spines['left'].set_color('green')
ax1.spines['top'].set_visible(True)
ax1.spines['right'].set_visible(True)
ax1.spines['top'].set_color('green')
ax1.spines['right'].set_color('green')

ax2.set_facecolor('black')
ax2.tick_params(axis='x', colors='green')
ax2.tick_params(axis='y', colors='green')
ax2.spines['bottom'].set_color('green')
ax2.spines['left'].set_color('green')
ax2.spines['top'].set_visible(True)
ax2.spines['right'].set_visible(True)
ax2.spines['top'].set_color('green')
ax2.spines['right'].set_color('green')

ax3.set_facecolor('black')
ax3.tick_params(axis='x', colors='green')
ax3.tick_params(axis='y', colors='green')
ax3.spines['bottom'].set_color('green')
ax3.spines['left'].set_color('green')
ax3.spines['top'].set_visible(True)
ax3.spines['right'].set_visible(True)
ax3.spines['top'].set_color('green')
ax3.spines['right'].set_color('green')

ax4.set_facecolor('black')
ax4.tick_params(axis='x', colors='green')
ax4.tick_params(axis='y', colors='green')
ax4.spines['bottom'].set_color('green')
ax4.spines['left'].set_color('green')
ax4.spines['top'].set_visible(True)
ax4.spines['right'].set_visible(True)
ax4.spines['top'].set_color('green')
ax4.spines['right'].set_color('green')

# Start time for elapsed time calculation
start_time = time.time()

# Main loop for updating the graph
running = True
while running:
   # Handle events
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False
       elif event.type == pygame.KEYDOWN:
           if event.key == K_1:
               if main != 1:
                   ax1.set_position(gs[:,:-1].get_position(fig))
                   ax2.set_position(gs[0,-1].get_position(fig))
                   ax3.set_position(gs[1,-1].get_position(fig))
                   ax4.set_position(gs[2,-1].get_position(fig))
                   main = 1
           elif event.key == K_2:
               if main != 2:
                   ax2.set_position(gs[:,:-1].get_position(fig))
                   ax1.set_position(gs[0,-1].get_position(fig))
                   ax3.set_position(gs[1,-1].get_position(fig))
                   ax4.set_position(gs[2,-1].get_position(fig))
                   main = 2
           elif event.key == K_3:
               if main != 3:
                   ax3.set_position(gs[:,:-1].get_position(fig))
                   ax1.set_position(gs[0,-1].get_position(fig))
                   ax2.set_position(gs[1,-1].get_position(fig))
                   ax4.set_position(gs[2,-1].get_position(fig))
                   main = 3
           elif event.key == K_4:
               if main != 4:
                   ax4.set_position(gs[:,:-1].get_position(fig))
                   ax1.set_position(gs[0,-1].get_position(fig))
                   ax2.set_position(gs[1,-1].get_position(fig))
                   ax3.set_position(gs[2,-1].get_position(fig))
                   main = 4
           else:
               pass

   # Get the state of all keyboard keys
   keys = pygame.key.get_pressed()

   # Move the rectangle if the arrow keys are held down
   if keys[pygame.K_UP]:
       y_mult += 0.1
   if keys[pygame.K_DOWN]:
       y_mult -= 0.1

   if y1 <= 0:
       y1 = 0.1
       y_mult = 1
   y1 = y1 * y_mult         
                   
   # Calculate elapsed time
   elapsed_time = time.time() - start_time

   # Calculate y values
   # if main == 1:
       # y1_values = y1_values * 0
       # y2_values = y2_values * 0
       # y3_values = y3_values * 0
       # y4_values = y4_values * 0
   #y1 = elapsed_time**2
   y2 = np.sin(elapsed_time)
   y3 = np.cos(elapsed_time)
   y4 = np.sin(elapsed_time) + np.cos(elapsed_time)
   

   # Append current time and y value to the lists
   x_values.append(elapsed_time)
   y1_values.append(y1)
   y2_values.append(y2)
   y3_values.append(y3)
   y4_values.append(y4)

   # Remove old data points if the number of points exceeds the limit
   if len(x_values) > num_points:
       x_values.pop(0)
       y1_values.pop(0)
       y2_values.pop(0)
       y3_values.pop(0)
       y4_values.pop(0)

   # Clear the axis and plot the updated data
   ax1.clear()
   ax1.plot(x_values, y1_values, color='lime')
   ax2.clear()
   ax2.plot(x_values, y2_values, color='lime')
   ax3.clear()
   ax3.plot(x_values, y3_values, color='lime')
   ax4.clear()
   ax4.plot(x_values, y4_values, color='lime')

   # Set labels and title
   if main == 1:
       ax1.set_xlabel('Elapsed Time', color='green', weight='bold')
       ax1.set_ylabel('Y Value', color='green',weight='bold')
       ax1.set_title('t**2', color='green',weight='bold')
   else:
       ax1.set_xlabel(None)
       ax1.set_ylabel(None)
       ax1.set_title('t**2', color='green')
   if main == 2:
       ax2.set_xlabel('Elapsed Time', color='green', weight='bold')
       ax2.set_ylabel('Y Value', color='green',weight='bold')
       ax2.set_title('sin(t)', color='green',weight='bold')
   else:
       ax2.set_xlabel(None)
       ax2.set_ylabel(None)
       ax2.set_title('sin(t)', color='green')
   if main == 3:
       ax3.set_xlabel('Elapsed Time', color='green', weight='bold')
       ax3.set_ylabel('Y Value', color='green',weight='bold')
       ax3.set_title('cos(t)', color='green',weight='bold')
   else:
       ax3.set_xlabel(None)
       ax3.set_ylabel(None)
       ax3.set_title('cos(t)', color='green')
   if main == 4:
       ax4.set_xlabel('Elapsed Time', color='green', weight='bold')
       ax4.set_ylabel('Y Value', color='green',weight='bold')
       ax4.set_title('sin(t)+cos(t)', color='green',weight='bold')
   else:
       ax4.set_xlabel(None)
       ax4.set_ylabel(None)
       ax4.set_title('sin(t)+cos(t)', color='green')


   ax1.grid(True, color='grey', linewidth=0.3)
   ax2.grid(True, color='grey', linewidth=0.3)
   ax3.grid(True, color='grey', linewidth=0.3)
   ax4.grid(True, color='grey', linewidth=0.3)

   # Draw the plot to a renderer
   canvas = agg.FigureCanvasAgg(fig)
   canvas.draw()

   # Get the renderer buffer as a raw RGBA buffer
   renderer_buffer = canvas.get_renderer().tostring_rgb()

   # Create a Pygame surface from the raw buffer
   graph_surface = pygame.image.fromstring(renderer_buffer, canvas.get_width_height(), "RGB")

   # Blit the graph surface onto the Pygame screen
   screen.blit(graph_surface, (0, 0))

   # Update the display
   pygame.display.flip()

   # Pause for a short interval to control the animation speed
   pygame.time.delay(1)

# Quit pygame
pygame.quit()


