import tkinter as tk
from tkinter import font
import math
import random
import time
import colorsys

class CyberpunkNameDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Cyberpunk Name Art")
        self.root.configure(bg='black')
        
        # Set window size and position it center screen
        window_width = 1200
        window_height = 800
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=window_width, height=window_height, 
                              bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        # Create fonts
        self.custom_font = font.Font(family="Courier", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Courier", size=16, weight="bold")  # Smaller font for subtitle
        self.matrix_font = font.Font(family="Arial", size=14)  # Font for Russian characters
        
        # Initialize matrix rain with Russian characters
        self.matrix_chars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        self.drops = []
        for _ in range(70):  # Increased number of matrix columns
            self.drops.append({
                'x': random.randint(0, window_width),
                'y': random.randint(-800, 0),
                'speed': random.uniform(2, 6),
                'length': random.randint(15, 35),
                'chars': [random.choice(self.matrix_chars) for _ in range(20)]
            })
        
        # Name art configuration
        self.name_lines = [
            "  _____           _____  __  __          ",
            " / ____|   /\\    / ____||  ||  |   /\\    ",
            "| (___    /  \\  | (___  | |__| |  /  \\   ",
            " \\___ \\  / /\\ \\ \\___ \\ |  __  | / /\\ \\  ",
            " ____) |/ ____ \\____) || |  | |/ ____ \\ ",
            "|_____/_/    \\_\\_____/ |_|  |_/_/    \\_\\",
            "                                          ",
            " ______   ___    ____  _____  _____  __    _____ _   _ ",
            "|___  /  / _ \\  |  _ \\|  ___||  __ \\| |   |_   _| \\ | |",
            "   / /  | |_| | | |_) | |__  | |  \\/| |     | | |  \\| |",
            "  / /   |  _  | |  _ <|  __| | | __ | |     | | | . ` |",
            " / /___ | | | | | |_) | |___ | |_\\ \\| |____ | |_| |\\  |",
            "/_____/ |_| |_| |____/|_____| \\____/|______|_____|_| \\_|"
        ]
        
        self.time = 0
        self.animate()

    def _draw_name(self):
        """Draw name with white 3D effect and blue text"""
        center_x = self.canvas.winfo_width() / 2
        start_y = self.canvas.winfo_height() / 2 - len(self.name_lines) * 15
        self.time += 0.5

        for i, line in enumerate(self.name_lines):
            y = start_y + i * 30
            
            # 3D Extrusion Effect (white shades)
            for depth in range(10, 0, -1):
                white_intensity = min(255, 40 + (depth * 25))
                color = f'#{white_intensity:02x}{white_intensity:02x}{white_intensity:02x}'
                
                self.canvas.create_text(
                    center_x + depth, 
                    y + depth,
                    text=line,
                    font=self.custom_font,
                    fill=color,
                    anchor='center'
                )

            # Main Text (white with blue glow)
            # Glitch Effect (blue variations)
            blue_variation = random.choice(['#00ffff', '#0066ff', '#0099ff'])
            glitch_offset = (math.sin(self.time*2)*1.5, math.cos(self.time*1.5)*1.5) if random.random() < 0.07 else (0,0)
            
            self.canvas.create_text(
                center_x + glitch_offset[0],
                y + glitch_offset[1],
                text=line,
                font=self.custom_font,
                fill=blue_variation,
                anchor='center'
            )

            # Scanline Effect (cyan)
            if random.random() < 0.2:
                self.canvas.create_line(
                    center_x - 200, y - 15,
                    center_x + 200, y - 15,
                    fill='#00ffff',
                    width=2,
                    stipple='gray50'
                )

    def animate(self):
        """Main animation loop"""
        self.canvas.delete('all')
        
        # Update matrix rain
        self._update_matrix_rain()
        
        # Draw name with effects
        self._draw_name()
        
        # Add hologram effect
        self._draw_hologram_effect()
        
        self.root.after(20, self.animate)

    def _draw_hologram_effect(self):
        """Blue-only hologram effect"""
        for i in range(20):
            self.canvas.create_line(
                i * 60, 0,
                i * 60, self.canvas.winfo_height(),
                fill='#0066ff',
                width=1,
                stipple='gray50'
            )
            self.canvas.create_line(
                0, i * 60,
                self.canvas.winfo_width(), i * 60,
                fill='#0099ff',
                width=1,
                stipple='gray50'
            )

    def _update_matrix_rain(self):
        """Blue matrix rain"""
        for drop in self.drops:
            drop['y'] += drop['speed']
            if drop['y'] > self.canvas.winfo_height():
                drop['y'] = random.randint(-200, -100)
                drop['x'] = random.randint(0, self.canvas.winfo_width())
                drop['chars'] = [random.choice(self.matrix_chars) for _ in range(20)]
            
            for i in range(drop['length']):
                y_pos = drop['y'] - (i * 20)
                if 0 <= y_pos <= self.canvas.winfo_height():
                    opacity = int(255 * (1 - i/drop['length']))
                    blue_value = min(255, opacity + 150)
                    color = f'#0000{blue_value:02x}'
                    self.canvas.create_text(
                        drop['x'], y_pos,
                        text=drop['chars'][i % len(drop['chars'])],
                        font=self.matrix_font,
                        fill=color
                    )

def main():
    root = tk.Tk()
    app = CyberpunkNameDisplay(root)
    root.mainloop()

if __name__ == "__main__":
    main()