# Desktop Pet

import tkinter as tk
import random
import math
import time

class CutePet:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cute Pet")
        self.window.attributes('-topmost', True)
        self.window.overrideredirect(True)
        
        # Make window transparent
        self.window.attributes('-transparentcolor', 'black')
        
        # Pet settings
        self.size = 120
        self.x = 600
        self.y = 400
        self.vx = 0
        self.vy = 0
        self.state = "idle"
        self.facing = "right"
        self.animation_frame = 0
        self.bounce_offset = 0
        
        # Set window size
        self.window.geometry(f'{self.size}x{self.size}+{self.x}+{self.y}')
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.window,
            width=self.size,
            height=self.size,
            bg='black',
            highlightthickness=0
        )
        self.canvas.pack()
        
        # Mouse tracking for dragging
        self.dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # Bind events
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        self.canvas.bind("<Button-3>", self.right_click_menu)
        
        # Create control panel
        self.create_control_panel()
        
        # Start pet behaviors
        self.draw_pet()
        self.move_pet()
        self.animate_pet()
        self.random_behavior()
        
    def create_control_panel(self):
        """Create a stylish control panel"""
        self.panel = tk.Toplevel(self.window)
        self.panel.title("Pet Controller")
        self.panel.geometry("300x250+300+300")
        self.panel.configure(bg='#2C3E50')
        self.panel.attributes('-topmost', True)
        
        # Title with style
        title_frame = tk.Frame(self.panel, bg='#34495E', height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title = tk.Label(
            title_frame,
            text="✨ Cute Desktop Pet ✨",
            font=("Comic Sans MS", 16, "bold"),
            fg='white',
            bg='#34495E'
        )
        title.pack(expand=True)
        
        # Pet stats frame
        stats_frame = tk.Frame(self.panel, bg='#2C3E50')
        stats_frame.pack(pady=15)
        
        # Mood indicator
        self.mood_label = tk.Label(
            stats_frame,
            text="Mood: 😊 Happy",
            font=("Arial", 12),
            fg='#2ECC71',
            bg='#2C3E50'
        )
        self.mood_label.pack(pady=5)
        
        # Activity indicator
        self.activity_label = tk.Label(
            stats_frame,
            text=f"Activity: {self.state}",
            font=("Arial", 11),
            fg='#3498DB',
            bg='#2C3E50'
        )
        self.activity_label.pack(pady=5)
        
        # Control buttons
        button_frame = tk.Frame(self.panel, bg='#2C3E50')
        button_frame.pack(pady=10)
        
        # Action buttons with colors
        actions = [
            ("🎮 Play", self.play_with_pet, '#E74C3C'),
            ("🍖 Feed", self.feed_pet, '#F39C12'),
            ("😴 Sleep", self.sleep_pet, '#9B59B6'),
            ("🏃 Run", self.make_run, '#3498DB')
        ]
        
        for text, command, color in actions:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=("Arial", 10, "bold"),
                width=8,
                cursor="hand2"
            )
            btn.pack(side=tk.LEFT, padx=5)
        
        # Instructions
        info_label = tk.Label(
            self.panel,
            text="Drag pet with left mouse button\nRight click for quick actions",
            font=("Arial", 9),
            fg='#ECF0F1',
            bg='#2C3E50'
        )
        info_label.pack(pady=10)
        
        # Close button
        close_btn = tk.Button(
            self.panel,
            text="Close Pet",
            command=self.close_app,
            bg='#C0392B',
            fg='white',
            font=("Arial", 10, "bold")
        )
        close_btn.pack(pady=5)
    
    def draw_pet(self):
        """Draw an attractive animated pet"""
        self.canvas.delete("all")
        
        # Calculate bounce for animation
        bounce = abs(math.sin(self.animation_frame * 0.1)) * 5
        
        # Base position
        cx = self.size // 2
        cy = self.size // 2 - bounce
        
        # Draw shadow
        shadow_size = 30 + bounce
        self.canvas.create_oval(
            cx - shadow_size//2, self.size - 15,
            cx + shadow_size//2, self.size - 10,
            fill='#333333', outline=''
        )
        
        # Draw body (fluffy circle)
        body_size = 50
        # Outer fluffy layer
        for i in range(8):
            angle = i * 45
            x_offset = math.cos(math.radians(angle)) * 5
            y_offset = math.sin(math.radians(angle)) * 5
            self.canvas.create_oval(
                cx - body_size//2 + x_offset, cy - body_size//2 + y_offset,
                cx + body_size//2 + x_offset, cy + body_size//2 + y_offset,
                fill='#FFE4E1', outline='#FFB6C1', width=1
            )
        
        # Main body
        self.canvas.create_oval(
            cx - body_size//2, cy - body_size//2,
            cx + body_size//2, cy + body_size//2,
            fill='#FFB6C1', outline='#FF69B4', width=2
        )
        
        # Draw ears (triangles)
        ear_size = 15
        # Left ear
        self.canvas.create_polygon(
            cx - 20, cy - body_size//2,
            cx - 25, cy - body_size//2 - ear_size,
            cx - 10, cy - body_size//2 - 5,
            fill='#FFB6C1', outline='#FF69B4', width=2
        )
        # Right ear
        self.canvas.create_polygon(
            cx + 20, cy - body_size//2,
            cx + 25, cy - body_size//2 - ear_size,
            cx + 10, cy - body_size//2 - 5,
            fill='#FFB6C1', outline='#FF69B4', width=2
        )
        
        # Draw face
        # Eyes (animated blink)
        eye_height = 8 if random.random() > 0.95 else 2  # Occasional blink
        
        if self.facing == "right":
            # Looking right
            self.canvas.create_oval(
                cx - 10, cy - 10,
                cx - 2, cy - 10 + eye_height,
                fill='black'
            )
            self.canvas.create_oval(
                cx + 5, cy - 10,
                cx + 13, cy - 10 + eye_height,
                fill='black'
            )
        else:
            # Looking left
            self.canvas.create_oval(
                cx - 13, cy - 10,
                cx - 5, cy - 10 + eye_height,
                fill='black'
            )
            self.canvas.create_oval(
                cx + 2, cy - 10,
                cx + 10, cy - 10 + eye_height,
                fill='black'
            )
        
        # Nose
        self.canvas.create_oval(
            cx - 3, cy,
            cx + 3, cy + 4,
            fill='#FF1493', outline=''
        )
        
        # Mouth (changes with state)
        if self.state == "happy" or self.state == "play":
            # Smile
            self.canvas.create_arc(
                cx - 10, cy,
                cx + 10, cy + 10,
                start=0, end=-180,
                style=tk.ARC, width=2, outline='#FF1493'
            )
        elif self.state == "sleep":
            # Sleeping (Z's)
            self.canvas.create_text(
                cx + 30, cy - 30,
                text="Z", font=("Arial", 14, "bold"),
                fill='#4169E1'
            )
            self.canvas.create_text(
                cx + 35, cy - 40,
                text="z", font=("Arial", 10),
                fill='#4169E1'
            )
        else:
            # Normal mouth
            self.canvas.create_line(
                cx - 5, cy + 5,
                cx + 5, cy + 5,
                width=2, fill='#FF1493'
            )
        
        # Draw paws (little circles)
        paw_y = cy + body_size//2 - 10
        # Left paw
        self.canvas.create_oval(
            cx - 15, paw_y,
            cx - 5, paw_y + 10,
            fill='#FFB6C1', outline='#FF69B4'
        )
        # Right paw
        self.canvas.create_oval(
            cx + 5, paw_y,
            cx + 15, paw_y + 10,
            fill='#FFB6C1', outline='#FF69B4'
        )
        
        # Add sparkles when happy
        if self.state == "happy" or self.state == "play":
            for i in range(3):
                spark_x = cx + random.randint(-30, 30)
                spark_y = cy + random.randint(-30, 30)
                self.canvas.create_text(
                    spark_x, spark_y,
                    text="✨", font=("Arial", 8)
                )
    
    def start_drag(self, event):
        """Start dragging the pet"""
        self.dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.state = "dragged"
    
    def drag(self, event):
        """Drag the pet around"""
        if self.dragging:
            x = self.window.winfo_pointerx() - self.drag_start_x
            y = self.window.winfo_pointery() - self.drag_start_y
            self.window.geometry(f'+{x}+{y}')
            self.x = x
            self.y = y
    
    def stop_drag(self, event):
        """Stop dragging"""
        self.dragging = False
        self.state = "idle"
    
    def move_pet(self):
        """Move the pet autonomously"""
        if not self.dragging and self.state in ["walk", "run"]:
            # Update position
            self.x += self.vx
            self.y += self.vy
            
            # Bounce off screen edges
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            
            if self.x <= 0 or self.x >= screen_width - self.size:
                self.vx = -self.vx
                self.facing = "right" if self.vx > 0 else "left"
            
            if self.y <= 0 or self.y >= screen_height - self.size - 50:
                self.vy = -self.vy
            
            # Update window position
            self.window.geometry(f'+{int(self.x)}+{int(self.y)}')
        
        # Continue moving
        self.window.after(50, self.move_pet)
    
    def animate_pet(self):
        """Animate the pet"""
        self.animation_frame += 1
        self.draw_pet()
        
        # Update activity label
        self.activity_label.config(text=f"Activity: {self.state}")
        
        # Continue animation
        self.window.after(100, self.animate_pet)
    
    def random_behavior(self):
        """Change pet behavior randomly"""
        if not self.dragging:
            behaviors = ["idle", "walk", "happy", "sleep"]
            self.state = random.choice(behaviors)
            
            if self.state == "walk":
                self.vx = random.choice([-2, -1, 1, 2])
                self.vy = random.choice([-2, -1, 0, 1, 2])
                self.facing = "right" if self.vx > 0 else "left"
            else:
                self.vx = 0
                self.vy = 0
            
            # Update mood label
            moods = {
                "idle": "😊 Happy",
                "walk": "🚶 Walking",
                "happy": "🥰 Very Happy",
                "sleep": "😴 Sleeping",
                "run": "🏃 Running",
                "play": "🎮 Playing"
            }
            self.mood_label.config(text=f"Mood: {moods.get(self.state, '😊 Happy')}")
        
        # Schedule next behavior change
        self.window.after(random.randint(3000, 8000), self.random_behavior)
    
    def play_with_pet(self):
        """Play with the pet"""
        self.state = "play"
        self.vx = random.choice([-3, 3])
        self.vy = random.choice([-3, 3])
        self.window.after(3000, lambda: setattr(self, 'state', 'happy'))
    
    def feed_pet(self):
        """Feed the pet"""
        self.state = "happy"
        # Show food emoji
        food = self.canvas.create_text(
            self.size//2, 20,
            text="🍖", font=("Arial", 24)
        )
        self.window.after(2000, lambda: self.canvas.delete(food))
    
    def sleep_pet(self):
        """Make pet sleep"""
        self.state = "sleep"
        self.vx = 0
        self.vy = 0
    
    def make_run(self):
        """Make pet run fast"""
        self.state = "run"
        self.vx = random.choice([-5, 5])
        self.vy = random.choice([-5, 5])
        self.facing = "right" if self.vx > 0 else "left"
    
    def right_click_menu(self, event):
        """Show right-click menu"""
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="Play", command=self.play_with_pet)
        menu.add_command(label="Feed", command=self.feed_pet)
        menu.add_command(label="Sleep", command=self.sleep_pet)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.close_app)
        menu.post(event.x_root, event.y_root)
    
    def close_app(self):
        """Close the application"""
        self.window.destroy()
        self.panel.destroy()
    
    def run(self):
        """Start the pet"""
        print("✨ Cute Pet is running!")
        print("Look for a pink fluffy pet on your screen!")
        print("You can drag it around and interact with it!")
        self.window.mainloop()

if __name__ == "__main__":
    pet = CutePet()
    pet.run()