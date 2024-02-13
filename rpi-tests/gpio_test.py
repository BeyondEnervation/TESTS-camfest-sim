## Welcome 
import pygame
import sys, math, time
import RPi.GPIO as GPIO
print("Hello World")
GPIO.setmode(GPIO.BCM)
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRID_COLOR = (50, 50, 50)
GRID_SPACING = 20

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CDT Sim")

# Constants for the three plotters
PLOTTER_WIDTH = 200
PLOTTER_HEIGHT = 150
PLOTTER_X = WIDTH - PLOTTER_WIDTH - 20  # Align to the right
PLOTTER_Y1 = 50
PLOTTER_Y2 = PLOTTER_Y1 + PLOTTER_HEIGHT + 30
PLOTTER_Y3 = PLOTTER_Y2 + PLOTTER_HEIGHT + 30

# Constants for the expanded graph area
EXPANDED_X = 50
EXPANDED_Y = PLOTTER_Y1
EXPANDED_HEIGHT = PLOTTER_Y3 + PLOTTER_HEIGHT - PLOTTER_Y1
EXPANDED_WIDTH = WIDTH - PLOTTER_WIDTH - 70

# Inital y-scale
y_scale = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
current_y_value = 0
y_dif = 0

# Create a Pygame font for displaying text
font = pygame.font.Font(None, 24)

# Boolean
scroll_mode = False

# Data for the three graphs
max_points = 50

# Data for Graph 1
x_values_1, y_values_1 = [], []

# Data for Graph 2
x_values_2, y_values_2 = [], []

# Data for Graph 3
x_values_3, y_values_3 = [], []

# Data for the expanded graph
x_values_expanded, y_values_expanded = [], []

# Variable to store the program start time
program_start_time = time.time()

# Function to update graph data with sinusoidal pattern
def update_data(x_values, y_values, phase_offset, frequency_multiplier):
    # Add a new data point to the graph
    elapsed_time = time.time() - program_start_time
    x_values.append(elapsed_time)
    y_values.append(5 * math.sin(frequency_multiplier * (elapsed_time + phase_offset)) + 5)

    # Keep the number of data points within the maximum limit
    if len(x_values) > max_points:
        x_values.pop(0)
        y_values.pop(0)

# Main game loop
running = True
clock = pygame.time.Clock()

# Variable to track the selected graph
selected_graph = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within one of the plotters
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if PLOTTER_X <= mouse_x <= PLOTTER_X + PLOTTER_WIDTH:
                if PLOTTER_Y1 <= mouse_y <= PLOTTER_Y1 + PLOTTER_HEIGHT:
                    selected_graph = 1
                elif PLOTTER_Y2 <= mouse_y <= PLOTTER_Y2 + PLOTTER_HEIGHT:
                    selected_graph = 2
                elif PLOTTER_Y3 <= mouse_y <= PLOTTER_Y3 + PLOTTER_HEIGHT:
                    selected_graph = 3

    # Update the data for each graph with higher frequency
    update_data(x_values_1, y_values_1, 0, 2)  # Frequency multiplier of 2
    update_data(x_values_2, y_values_2, math.pi / 2, 3)  # Frequency multiplier of 3
    update_data(x_values_3, y_values_3, math.pi, 4)  # Frequency multiplier of 4

    # Clear the screen
    screen.fill(BLACK)

    # Draw grid on the plotters
    for plotter_y in [PLOTTER_Y1, PLOTTER_Y2, PLOTTER_Y3]:
        for x in range(PLOTTER_X, PLOTTER_X + PLOTTER_WIDTH, GRID_SPACING):
            pygame.draw.line(screen, GRID_COLOR, (x, plotter_y), (x, plotter_y + PLOTTER_HEIGHT), 1)
        for y in range(plotter_y, plotter_y + PLOTTER_HEIGHT, GRID_SPACING):
            pygame.draw.line(screen, GRID_COLOR, (PLOTTER_X, y), (PLOTTER_X + PLOTTER_WIDTH, y), 1)

    # Draw the three plotters with titles
    for i, (plotter_y, x_values, y_values) in enumerate([(PLOTTER_Y1, x_values_1, y_values_1),
                                                         (PLOTTER_Y2, x_values_2, y_values_2),
                                                         (PLOTTER_Y3, x_values_3, y_values_3)], start=1):
        pygame.draw.rect(screen, GREEN, (PLOTTER_X, plotter_y, PLOTTER_WIDTH, PLOTTER_HEIGHT + 2), 2)

        # Draw the graph with scrolling effect
        for j in range(1, len(x_values)):
            x1 = PLOTTER_X + int((x_values[j - 1] - x_values[0]) * PLOTTER_WIDTH / (x_values[-1] - x_values[0]))
            y1 = plotter_y + PLOTTER_HEIGHT - int(y_values[j - 1] * (PLOTTER_HEIGHT / 10))
            x2 = PLOTTER_X + int((x_values[j] - x_values[0]) * PLOTTER_WIDTH / (x_values[-1] - x_values[0]))
            y2 = plotter_y + PLOTTER_HEIGHT - int(y_values[j] * (PLOTTER_HEIGHT / 10))
            pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 2)

        # Display the title
        title_text = font.render(f"Graph {i}", True, GREEN)
        screen.blit(title_text, (PLOTTER_X + 8, plotter_y - 22))

    # Draw the expanded graph area
    pygame.draw.rect(screen, GREEN, (EXPANDED_X, EXPANDED_Y, EXPANDED_WIDTH, EXPANDED_HEIGHT + 2), 2)

    # Attempt to make y axis scroll
    if y_values_expanded:
        current_y_value = y_values_expanded[-1]

        if current_y_value > y_scale[10]:
            y_dif = current_y_value - y_scale[10]
        elif current_y_value < y_scale[0]:
            y_dif = current_y_value - y_scale[0]
        else:
            y_dif = 0

        y_scale_pos_offset = y_dif * (EXPANDED_HEIGHT / 10)

    # Draw the scales on the y-axis along with the grid
    y_scale_pos_offset = 0  # Define it here
    for i in range(11):
        y_scale_pos = EXPANDED_Y + int(i * EXPANDED_HEIGHT / 10) + y_scale_pos_offset

        pygame.draw.line(screen, GREEN, (EXPANDED_X - 5, y_scale_pos),
                         (EXPANDED_X + 5, y_scale_pos), 2)
        scale_text = font.render(str(y_scale[len(y_scale) - 1] - i), True, GREEN)

        # Make the 10 mark fit nicer
        if i == 0:
            screen.blit(scale_text, (EXPANDED_X - 26, y_scale_pos - 10))
        else:
            screen.blit(scale_text, (EXPANDED_X - 20, y_scale_pos - 10))

        # Draw grid on the expanded graph along the y-axis
        pygame.draw.line(screen, GRID_COLOR, (EXPANDED_X + 6, y_scale_pos),
                         (EXPANDED_X + EXPANDED_WIDTH - 3, y_scale_pos), 1)

    print(y_scale_pos)

    # Draw the scales on the x-axis along with the grid
    previous_second = -1
    for x_value in x_values_expanded:
        seconds = int(x_value)
        if seconds != previous_second and seconds % 1 == 0:  # Update every second
            x_scale_pos = EXPANDED_X + int((x_value - x_values_expanded[0]) * EXPANDED_WIDTH / (x_values_expanded[-1] - x_values_expanded[0]))
            pygame.draw.line(screen, GREEN, (x_scale_pos, EXPANDED_Y + EXPANDED_HEIGHT),
                             (x_scale_pos, EXPANDED_Y + EXPANDED_HEIGHT + 5), 2)
            scale_text = font.render(str(seconds), True, GREEN)
            screen.blit(scale_text, (x_scale_pos - 10, EXPANDED_Y + EXPANDED_HEIGHT + 5))
            previous_second = seconds

            # Draw grid on the expanded graph along the x-axis
            pygame.draw.line(screen, GRID_COLOR, (x_scale_pos, EXPANDED_Y),
                             (x_scale_pos, EXPANDED_Y + EXPANDED_HEIGHT), 1)


    # Draw the selected graph in the expanded area with scrolling effect
    if selected_graph is not None:
        if selected_graph == 1:
            x_values_expanded, y_values_expanded = x_values_1.copy(), y_values_1.copy()
        elif selected_graph == 2:
            x_values_expanded, y_values_expanded = x_values_2.copy(), y_values_2.copy()
        elif selected_graph == 3:
            x_values_expanded, y_values_expanded = x_values_3.copy(), y_values_3.copy()

        for j in range(1, len(x_values_expanded)):
            x1 = EXPANDED_X + int((x_values_expanded[j - 1] - x_values_expanded[0]) * EXPANDED_WIDTH /
                                  (x_values_expanded[-1] - x_values_expanded[0]))
            y1 = EXPANDED_Y + EXPANDED_HEIGHT - int((y_values_expanded[j - 1]) * (EXPANDED_HEIGHT / 10))
            x2 = EXPANDED_X + int((x_values_expanded[j] - x_values_expanded[0]) * EXPANDED_WIDTH /
                                  (x_values_expanded[-1] - x_values_expanded[0]))
            y2 = EXPANDED_Y + EXPANDED_HEIGHT - int((y_values_expanded[j]) * (EXPANDED_HEIGHT / 10))

            pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 2)

    # Update the display
    pygame.display.update()

    # Cap the frame rate to 30 FPS (slower speed)
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()


