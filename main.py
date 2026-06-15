"""
File: main.py
----------------
Karel's Homecoming: Pure Tkinter 400x400 Fallback Edition
This standalone version completely bypasses 'graphics.py' or 'stanfordkarel'
dependencies. It uses native Python tkinter to run the hybrid experience
perfectly scaled within a standard 400x400 grid.

Author: [Your Name]
Course: Stanford Code in Place 2026
"""

import tkinter as tk
import time

# --- GLOBAL CONSTANTS ---
# Fixed Code in Place Canvas Bounds
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

# Color Palettes
BACKGROUND_COLOR = "#ECEFF1"     # Sleek light gray sky
KAREL_COLOR = "#00ACC1"          # Classic Karel turquoise/cyan
KAREL_EYE_COLOR = "#FFFFFF"
BEEPER_COLOR = "#FFB300"         # Golden amber beepers

# Animation Settings
DELAY = 0.3                      # Seconds between Karel's steps


# =====================================================================
# PHASE 1: CONSOLE COMPONENT (Data Gathering & Input Validation)
# =====================================================================

def get_user_preferences():
    """
    Displays a text menu to the user in the console, validates choices, 
    and packs everything neatly into a dictionary to hand off to the graphics engine.
    """
    print("=============================================")
    print("      Welcome to Karel's Homecoming!         ")
    print("=============================================\n")
    print("Help Karel find the way home by configuring the world.\n")

    # 1. Choose House Style
    print("--- Step 1: Choose House Architectural Style ---")
    print("1) Cozy Cottage (Traditional design)")
    print("2) Modern Tech Pad (Sleek minimalist design)")
    style_choice = ""
    while style_choice not in ["1", "2"]:
        style_choice = input("Select style (1 or 2): ").strip()
        if style_choice not in ["1", "2"]:
            print("❌ Invalid selection. Please enter 1 or 2.")
    
    house_style = "cozy" if style_choice == "1" else "modern"
    print(f"👍 Style set to: {house_style.upper()}\n")

    # 2. Choose Roof Color
    print("--- Step 2: Choose Roof Color Theme ---")
    print("Options available: red, blue, green")
    valid_colors = ["red", "blue", "green"]
    roof_color = ""
    while roof_color not in valid_colors:
        roof_color = input("Type your preferred color: ").strip().lower()
        if roof_color not in valid_colors:
            print(f"❌ Invalid color. Please choose from {valid_colors}.")
            
    print(f"👍 Roof color set to: {roof_color.upper()}\n")

    # 3. Define the Journey Scale (Number of Beepers to Collect)
    print("--- Step 3: Configure Karel's Task ---")
    print("How many beepers should Karel collect on the journey home? (Pick between 1 and 4)")
    beeper_count = 0
    while beeper_count < 1 or beeper_count > 4:
        user_in = input("Enter number of beepers (1-4): ").strip()
        if user_in.isdigit():
            beeper_count = int(user_in)
            if beeper_count < 1 or beeper_count > 4:
                print("❌ Out of bounds. Please enter a number from 1 to 4.")
        else:
            print("❌ That's not a valid number. Try again.")
            
    print(f"👍 Journey configured! Karel must collect {beeper_count} beepers.")
    print("\n📦 Configuration locked! Launching Graphics Window...")
    print("=============================================\n")

    project_settings = {
        "style": house_style,
        "roof_color": roof_color,
        "beepers": beeper_count
    }
    
    return project_settings


# =====================================================================
# PHASE 2: GRAPHICS COMPONENT (Procedural Scene Drawing)
# =====================================================================

def draw_environment(canvas, settings):
    """
    Decomposes the drawing process to render background canvas elements
    and the completely customized house structured inside 400x400 window limits.
    """
    # Sky
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT - 80, fill=BACKGROUND_COLOR, outline="")
    # Grass lawn road base
    canvas.create_rectangle(0, CANVAS_HEIGHT - 80, CANVAS_WIDTH, CANVAS_HEIGHT, fill="#81C784", outline="")

    # Custom House Frame Placement Constraints scaled for 400x400 viewport
    house_x1 = 280
    house_y1 = 200
    house_x2 = 380
    house_y2 = 320

    color_map = {
        "red": "#E53935",
        "blue": "#1E88E5",
        "green": "#43A047"
    }
    selected_roof_color = color_map[settings["roof_color"]]

    if settings["style"] == "cozy":
        draw_cozy_house(canvas, house_x1, house_y1, house_x2, house_y2, selected_roof_color)
    else:
        draw_modern_house(canvas, house_x1, house_y1, house_x2, house_y2, selected_roof_color)


def draw_cozy_house(canvas, x1, y1, x2, y2, roof_color):
    """Draws a traditional cottage layout inside custom Tkinter parameters."""
    # Main Body
    canvas.create_rectangle(x1, y1, x2, y2, fill="#FFE0B2", outline="#BCAAA4", width=2)
    # Triangular Roof
    mid_x = (x1 + x2) / 2
    roof_y = y1 - 40
    canvas.create_polygon(x1 - 10, y1, mid_x, roof_y, x2 + 10, y1, fill=roof_color, outline="#3E2723", width=2)
    # Cozy Door
    canvas.create_rectangle(x1 + 35, y2 - 55, x1 + 65, y2, fill="#A1887F", outline="#5D4037")
    canvas.create_oval(x1 + 57, y2 - 30, x1 + 62, y2 - 25, fill="#FFD54F")
    # Round Window
    canvas.create_oval(x1 + 10, y1 + 20, x1 + 35, y1 + 45, fill="#E0F7FA", outline="#B2EBF2")


def draw_modern_house(canvas, x1, y1, x2, y2, roof_color):
    """Draws a geometric house layout inside custom Tkinter parameters."""
    # Main Body
    canvas.create_rectangle(x1, y1, x2, y2, fill="#CFD8DC", outline="#78909C", width=2)
    # Flat Roof Overhang
    canvas.create_rectangle(x1 - 5, y1 - 15, x2 + 5, y1, fill=roof_color, outline="#263238")
    # Minimalist Door
    canvas.create_rectangle(x1 + 55, y2 - 65, x1 + 85, y2, fill="#37474F", outline="#212121")
    canvas.create_rectangle(x1 + 59, y2 - 35, x1 + 62, y2 - 20, fill="#B0BEC5")
    # Large Panorama Window
    canvas.create_rectangle(x1 + 10, y1 + 20, x1 + 45, y1 + 55, fill="#80DEEA", outline="#00ACC1")


# =====================================================================
# PHASE 3: KAREL SIMULATION COMPONENT (Animation Logic)
# =====================================================================

def spawn_beepers(canvas, num_beepers):
    """Places objects uniformly tracking real-time layout metrics array."""
    beeper_ids = []
    start_x = 75
    spacing = 45
    y_position = 300
    
    for i in range(num_beepers):
        bx = start_x + (i * spacing)
        beeper = canvas.create_oval(bx, y_position, bx + 12, y_position + 12, fill=BEEPER_COLOR, outline="#FF8F00")
        beeper_ids.append(beeper)
        
    return beeper_ids


def create_karel(canvas, x, y):
    """Constructs complex multi-tiered sprite shapes directly to the canvas context layer."""
    body = canvas.create_rectangle(x, y, x + 24, y + 24, fill=KAREL_COLOR, outline="#006064", width=2)
    eye1 = canvas.create_rectangle(x + 15, y + 4, x + 19, y + 8, fill=KAREL_EYE_COLOR, outline="")
    eye2 = canvas.create_rectangle(x + 15, y + 14, x + 19, y + 18, fill=KAREL_EYE_COLOR, outline="")
    
    return {"body": body, "eye1": eye1, "eye2": eye2}


def move_karel_sprite(canvas, karel, dx, dy):
    """Fires flat structural context alterations down onto item instances."""
    canvas.move(karel["body"], dx, dy)
    canvas.move(karel["eye1"], dx, dy)
    canvas.move(karel["eye2"], dx, dy)


def run_karel_simulation(canvas, root, settings, beeper_ids):
    """Loops and transitions positional items updating the system runtime canvas state."""
    karel_current_x = 15
    karel_y = 290
    karel = create_karel(canvas, karel_current_x, karel_y)
    
    # Boundary tracking coordinate target inside the 400x400 context frame grid
    door_target_x = 315
    beepers_collected = 0
    
    while karel_current_x < door_target_x:
        step_increment = 10
        move_karel_sprite(canvas, karel, step_increment, 0)
        karel_current_x += step_increment
        
        # Test overlapping coordinate indexes directly using Tkinter's native coords function
        for beeper in list(beeper_ids):
            b_coords = canvas.coords(beeper)
            if b_coords: 
                bx1 = b_coords[0]
                if karel_current_x >= bx1 - 8 and karel_current_x <= bx1 + 18:
                    canvas.delete(beeper)
                    beeper_ids.remove(beeper)
                    beepers_collected += 1
                    print(f"🤖 Karel picked up a beeper! ({beepers_collected}/{settings['beepers']})")

        # Command native Tkinter event queue refreshes to capture movement safely
        root.update()
        time.sleep(DELAY)

    # Success Termination Text Output
    canvas.create_text(200, 80, text="Welcome Home, Karel!", font=("Arial", 20, "bold"), fill="#37474F")
    print("\n🎉 SUCCESS! Karel reached home safely and finished all assigned operations!")
    print("=============================================")


# =====================================================================
# MAIN INITIALIZER ENTRY POINT
# =====================================================================

def main():
    # 1. Fire up Interactive Configuration Preferences Processing
    user_settings = get_user_preferences()
    
    # 2. Build explicit native Tkinter window instances
    root = tk.Tk()
    root.title("Karel's Homecoming - Code in Place Capstone")
    root.geometry(f"{CANVAS_WIDTH}x{CANVAS_HEIGHT}")
    root.resizable(False, False)

    # Instantiate drawing space maps directly from native library profiles
    canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#FFFFFF", highlightthickness=0)
    canvas.pack()

    # 3. Graphics Rendering Phase
    draw_environment(canvas, user_settings)
    beeper_handles = spawn_beepers(canvas, user_settings["beepers"])
    
    root.update()
    time.sleep(1.0) 

    # 4. Run the Active Simulation Process Animation Loops
    run_karel_simulation(canvas, root, user_settings, beeper_handles)

    # Retain layout window instances interactively until manually closed
    root.mainloop()


if __name__ == "__main__":
    main()
