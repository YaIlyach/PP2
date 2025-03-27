import pygame
import math
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1800, 1200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Paint")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)

# Default settings
drawing_color = BLACK
bg_color = WHITE
current_tool = "pen"  # Default tool
tool_size = 5
eraser_size = 20

# Variables for shape drawing
start_pos = None
drawing_shape = False
shape_type = "rectangle"  # Default shape

# List to store all drawings for undo functionality
drawings = []

# Font for UI
font = pygame.font.SysFont('Arial', 16)

def draw_toolbar():
    """Draw the toolbar with all available tools and color options"""
    # Toolbar background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 50))
    
    # Draw color selection buttons
    colors = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE]
    for i, color in enumerate(colors):
        pygame.draw.rect(screen, color, (10 + i * 40, 10, 30, 30))
        if color == drawing_color:
            pygame.draw.rect(screen, WHITE, (10 + i * 40, 10, 30, 30), 2)
    
    # Draw tool selection buttons
    tools = ["pen", "rectangle", "circle", "square", "triangle", "rtriangle", "rhombus", "eraser"]
    tool_icons = ["P", "R", "C", "S", "T", "RT", "RH", "E"]
    
    for i, (tool, icon) in enumerate(zip(tools, tool_icons)):
        pos_x = 350 + i * 50
        button_color = WHITE if current_tool != tool else GREEN
        pygame.draw.rect(screen, button_color, (pos_x, 10, 40, 30))
        text = font.render(icon, True, BLACK)
        screen.blit(text, (pos_x + 15, 15))
        
        # Highlight selected tool
        if current_tool == tool:
            pygame.draw.rect(screen, BLACK, (pos_x, 10, 40, 30), 2)

def draw_equilateral_triangle(surface, color, start_pos, end_pos):
    """Draw an equilateral triangle between start and end positions"""
    width = end_pos[0] - start_pos[0]
    height = end_pos[1] - start_pos[1]
    
    # Calculate the three points of the triangle
    top = (start_pos[0] + width // 2, start_pos[1])
    left = (start_pos[0], end_pos[1])
    right = (end_pos[0], end_pos[1])
    
    pygame.draw.polygon(surface, color, [top, left, right])

def draw_right_triangle(surface, color, start_pos, end_pos):
    """Draw a right triangle between start and end positions"""
    points = [
        start_pos,
        (start_pos[0], end_pos[1]),
        end_pos
    ]
    pygame.draw.polygon(surface, color, points)

def draw_rhombus(surface, color, start_pos, end_pos):
    """Draw a rhombus between start and end positions"""
    center_x = (start_pos[0] + end_pos[0]) // 2
    center_y = (start_pos[1] + end_pos[1]) // 2
    
    width = abs(end_pos[0] - start_pos[0])
    height = abs(end_pos[1] - start_pos[1])
    
    points = [
        (center_x, start_pos[1]),  # Top
        (end_pos[0], center_y),    # Right
        (center_x, end_pos[1]),    # Bottom
        (start_pos[0], center_y)   # Left
    ]
    
    pygame.draw.polygon(surface, color, points)

def redraw_screen():
    """Redraw everything on the screen"""
    screen.fill(bg_color)
    
    # Redraw all saved drawings
    for drawing in drawings:
        if drawing["tool"] == "pen":
            pygame.draw.lines(screen, drawing["color"], False, drawing["points"], drawing["size"])
        elif drawing["tool"] == "rectangle":
            pygame.draw.rect(screen, drawing["color"], drawing["rect"], drawing["size"])
        elif drawing["tool"] == "circle":
            pygame.draw.circle(screen, drawing["color"], drawing["center"], drawing["radius"], drawing["size"])
        elif drawing["tool"] == "square":
            rect = drawing["rect"]
            pygame.draw.rect(screen, drawing["color"], rect, drawing["size"])
        elif drawing["tool"] == "triangle":
            draw_equilateral_triangle(screen, drawing["color"], drawing["start"], drawing["end"])
        elif drawing["tool"] == "rtriangle":
            draw_right_triangle(screen, drawing["color"], drawing["start"], drawing["end"])
        elif drawing["tool"] == "rhombus":
            draw_rhombus(screen, drawing["color"], drawing["start"], drawing["end"])
        elif drawing["tool"] == "eraser":
            for point in drawing["points"]:
                pygame.draw.circle(screen, bg_color, point, drawing["size"])
    
    # Draw the current shape being drawn (preview)
    if drawing_shape and start_pos:
        current_pos = pygame.mouse.get_pos()
        if current_tool == "rectangle":
            rect = pygame.Rect(min(start_pos[0], current_pos[0]), min(start_pos[1], current_pos[1]),
                             abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
            pygame.draw.rect(screen, drawing_color, rect, tool_size)
        elif current_tool == "circle":
            radius = int(math.sqrt((current_pos[0] - start_pos[0])**2 + (current_pos[1] - start_pos[1])**2))
            pygame.draw.circle(screen, drawing_color, start_pos, radius, tool_size)
        elif current_tool == "square":
            size = max(abs(current_pos[0] - start_pos[0]), abs(current_pos[1] - start_pos[1]))
            rect = pygame.Rect(min(start_pos[0], current_pos[0]), min(start_pos[1], current_pos[1]), size, size)
            pygame.draw.rect(screen, drawing_color, rect, tool_size)
        elif current_tool == "triangle":
            draw_equilateral_triangle(screen, drawing_color, start_pos, current_pos)
        elif current_tool == "rtriangle":
            draw_right_triangle(screen, drawing_color, start_pos, current_pos)
        elif current_tool == "rhombus":
            draw_rhombus(screen, drawing_color, start_pos, current_pos)
    
    # Draw toolbar and instructions
    draw_toolbar()

# Main game loop
running = True
points = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.pos[1] <= 50:  # Clicked on toolbar
                # Check color selection
                colors = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, WHITE]
                for i, color in enumerate(colors):
                    if 10 + i * 40 <= event.pos[0] <= 40 + i * 40 and 10 <= event.pos[1] <= 40:
                        drawing_color = color
                
                # Check tool selection
                tools = ["pen", "rectangle", "circle", "square", "triangle", "rtriangle", "rhombus", "eraser"]
                for i, tool in enumerate(tools):
                    if 350 + i * 50 <= event.pos[0] <= 390 + i * 50 and 10 <= event.pos[1] <= 40:
                        current_tool = tool
            else:
                if event.button == 1:  # Left click
                    if current_tool == "pen":
                        points = [event.pos]
                    elif current_tool == "eraser":
                        points = [event.pos]
                    else:
                        start_pos = event.pos
                        drawing_shape = True
        
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:  # Left mouse button is pressed
                if current_tool == "pen":
                    points.append(event.pos)
                    drawings.append({"tool": "pen", "color": drawing_color, "points": points.copy(), "size": tool_size})
                elif current_tool == "eraser":
                    points.append(event.pos)
                    drawings.append({"tool": "eraser", "points": [event.pos], "size": eraser_size})
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button released
                if current_tool == "pen":
                    points = []
                elif current_tool == "eraser":
                    points = []
                elif drawing_shape:
                    end_pos = event.pos
                    if current_tool == "rectangle":
                        rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]),
                                         abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                        drawings.append({"tool": "rectangle", "color": drawing_color, "rect": rect, "size": tool_size})
                    elif current_tool == "circle":
                        radius = int(math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2))
                        drawings.append({"tool": "circle", "color": drawing_color, "center": start_pos, "radius": radius, "size": tool_size})
                    elif current_tool == "square":
                        size = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                        rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), size, size)
                        drawings.append({"tool": "square", "color": drawing_color, "rect": rect, "size": tool_size})
                    elif current_tool == "triangle":
                        drawings.append({"tool": "triangle", "color": drawing_color, "start": start_pos, "end": end_pos, "size": tool_size})
                    elif current_tool == "rtriangle":
                        drawings.append({"tool": "rtriangle", "color": drawing_color, "start": start_pos, "end": end_pos, "size": tool_size})
                    elif current_tool == "rhombus":
                        drawings.append({"tool": "rhombus", "color": drawing_color, "start": start_pos, "end": end_pos, "size": tool_size})
                    
                    drawing_shape = False
                    start_pos = None
        
        elif event.type == pygame.MOUSEWHEEL:
            # Change tool size with mouse wheel
            if current_tool == "eraser":
                eraser_size = max(5, min(50, eraser_size + event.y * 5))
            else:
                tool_size = max(1, min(20, tool_size + event.y))
        
        elif event.type == pygame.KEYDOWN:
            # Quick tool selection with number keys
            if event.unicode == '1':
                current_tool = "pen"
            elif event.unicode == '2':
                current_tool = "rectangle"
            elif event.unicode == '3':
                current_tool = "circle"
            elif event.unicode == '4':
                current_tool = "square"
            elif event.unicode == '5':
                current_tool = "triangle"
            elif event.unicode == '6':
                current_tool = "rtriangle"
            elif event.unicode == '7':
                current_tool = "rhombus"
            elif event.unicode == '8':
                current_tool = "eraser"
            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                if drawings:  # Undo last drawing
                    drawings.pop()
    
    redraw_screen()
    pygame.display.flip()

pygame.quit()
sys.exit()