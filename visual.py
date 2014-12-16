from infection import Infection
from tkinter import Tk, Canvas, CENTER, ALL, Entry
import random
from enum import Enum


def distance(x0, y0, x1, y1):
    """Distance formula"""
    return ((x1-x0)**2 + (y1-y0)**2)**0.5


class VisualUser(object):
    """
    User as represented visually on screen, a circle containing its name and version

    The VisualUser object contains a reference to an instance of the User class as well as its parent.
    """
    def __init__(self, user, parent):
        self.width, self.height = parent.width, parent.height
        self.parent = parent
        self.canvas = parent.canvas
        self.user = user
        # Give user class reference to visual class, useful when looping over students and coaches
        self.user.visual = self
        self.r = 25
        self.top = parent.margin + self.r
        # Randomly place user on screen
        self.x = random.randint(self.top, self.width - self.r)
        self.y = random.randint(self.top, self.height - self.r)
        # Initially still
        self.vx = self.vy = 0

    def draw_students(self):
        x0, y0 = self.x, self.y
        for student in self.user.students:
            x1, y1 = student.visual.x, student.visual.y
            self.canvas.create_line(x0, y0, x1, y1)

    def draw(self):
        x, y = self.x, self.y
        r = self.r
        # Parent defines how version correlates to fill color
        fill = self.parent.get_fill(self.user.version)
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill)
        text = "{user.name}\n{user.version}".format(user=self.user)
        nudge = 1  # Looks a little off center without
        self.canvas.create_text(x, y+nudge, text=text, justify=CENTER)

    def update_velocity(self):
        """
        Updates user's velocity on the screen

        Users are attracted to the users they either teach or coach.
        They are also repelled by any user if they get within buffer of each other.
        This heuristic helps convince the linked users to form a shape in which every
        group can be identified and not overlap
        """
        # Acceleration is memoryless and recalculated every frame
        ax = ay = 0
        x0, y0 = self.x, self.y
        # Minimum distance centers of users should come near each other
        buffer = 2.5*self.r
        # Calculate acceleration based on location of student and coaches
        connections = (self.user.students + self.user.coaches)
        for student in connections:
            x1, y1 = student.visual.x, student.visual.y
            d = distance(x0, y0, x1, y1)
            dx, dy = (x1-x0), (y1-y0)
            # Hooke's spring law
            k = 0.01
            if d > buffer:
                ax += k*dx
                ay += k*dy
            else:  # Stop users from colliding from attractions
                self.vx = self.vy = 0
        # User is repulsed by all other users
        for user in self.parent.users:
            x1, y1 = user.x, user.y
            d = distance(x0, y0, x1, y1)
            dx, dy = (x1-x0), (y1-y0)
            if d < buffer:
                repulsion = 0.1
                ax -= repulsion*dx
                ay -= repulsion*dy
        self.vx += ax
        self.vy += ay
        # Dissipation of energy
        dissipation = 0.8
        self.vx *= dissipation
        self.vy *= dissipation

    def update_location(self):
        """Update location of user by getting new velocity and moving"""
        self.update_velocity()
        self.x += self.vx
        self.y += self.vy
        # Prevent from going off screen
        if self.x > self.width - self.r or self.x < self.r:
            self.x -= 2*self.vx
            self.vx = 0
        if self.y > self.height - self.r or self.y < self.top:
            self.y -= 2*self.vy
            self.vy = 0

    def clicked(self, x, y):
        """Click on circular user"""
        return distance(x, y, self.x, self.y) < self.r

    def infect(self):
        """Infect user's group with parent's version"""
        self.user.infect_group(self.parent.version)


class Mode(Enum):
    """Animation Modes"""
    START = 0
    SETUP = 1
    MAIN = 2


class Button(object):
    """Basic Button Class for Animations"""
    def __init__(self, cx, cy, width, height, text):
        self.cx, self.cy = cx, cy
        self.x0 = cx - width/2
        self.x1 = cx + width/2
        self.y0 = cy - height/2
        self.y1 = cy + height/2
        self.text = text

    def clicked(self, x, y):
        """Click on rectangular region of button"""
        return (self.x0 <= x <= self.x1) and (self.y0 <= y <= self.y1)

    def draw(self, canvas):
        """Draw button rectangle and text"""
        cx, cy = self.cx, self.cy
        canvas.create_text(cx, cy, text=self.text, font=("Impact", 32))
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1)


class Visual(object):
    def __init__(self, width=800, height=600):
        root = Tk()
        self.root = root
        self.margin = 0.12*height
        self.width, self.height = width, height - self.margin
        self.cx, self.cy = width/2, (height - self.margin)/2
        self.toolbar_canvas = Canvas(self.root, width=self.width, height=self.margin)
        self.toolbar_canvas.pack()
        self.canvas = Canvas(root, width=width, height=height - self.margin)
        self.canvas.pack()
        self.init_animation()
        root.bind("<Button-1>", lambda e: self.mouse_event(e))
        root.bind("<Key>", lambda e: self.key_event(e))
        root.mainloop()

    def draw_users(self):
        """Draw all users"""
        for user in self.users:
            user.draw()

    def draw_connections(self):
        """Draw all of user's connections"""
        for user in self.users:
            user.draw_students()

    def draw_start_screen(self):
        """Start screen text"""
        self.canvas.delete(ALL)
        cx, cy = self.width/2, self.height/2
        font = ("Impact", "128")
        self.canvas.create_text(cx, 0.8*cy, text="INFECTION", font=font)
        font = ("Impact", 32)
        self.canvas.create_text(cx, 1.5*cy, text="Press s to Begin", font=font)

    def draw_setup_screen(self):
        """User setup screen"""
        self.canvas.delete(ALL)
        cx, cy = self.width/2, self.height/2
        self.num_users_entry = Entry(self.canvas, justify=CENTER)
        self.canvas.create_window(cx, 0.5*cy, window=self.num_users_entry)
        self.num_users_entry.insert(0, str(self.default_users))
        self.canvas.create_text(cx, 0.4*cy, text="Number of Users (1-100)", font=("Impact", 24))
        self.button = Button(cx, 1.5*cy, 0.3*cx, 0.2*cy, "Begin")
        self.button.draw(self.canvas)

    def draw_toolbar(self):
        """Toolbar for main animation"""
        self.toolbar_canvas.create_text(self.cx, 0.1*self.cy, text="INFECTION", font=("Impact", 32))
        font = ("Impact", 20)
        text = "Total Infection: Click User"
        self.toolbar_canvas.create_text(self.cx*0.05, 0.1*self.cy, text=text, font=font, anchor="w")
        self.toolbar_canvas.create_text(self.cx*1.8, 0.1*self.cy, text="Limited Infection", font=font, anchor="e")
        self.limited_entry = Entry(self.toolbar_canvas, justify=CENTER, width=3)
        self.toolbar_canvas.create_window(self.cx*1.85, 0.1*self.cy, window=self.limited_entry)
        self.limited_entry.insert(0, str(self.default_users//2))
        cx, cy = self.cx*1.95, self.margin*0.35
        r = self.margin/5
        self.limited_button = (cx, cy, r)
        self.toolbar_canvas.create_oval((cx-r, cy-r, cx+r, cy+r), width=2, fill="RED")
        self.toolbar_canvas.create_text(cx, cy, text="X", font=("Courier Bold", 30))
        side = self.width/self.versions
        self.side = side
        y = 50
        self.gradient = (y, y+side)
        for col in range(int(self.versions)):
            fill = self.get_fill(col)
            width = 2 if col == self.version else 0
            self.toolbar_canvas.create_rectangle(col*side, y, (col+1)*side, y+side, fill=fill, width=width)
            #self.toolbar_canvas.create_text(col*side + side/2, y+side/2, text=str(col), font="Arial 10")
        self.select_version()

    def redraw_all(self):
        """Refresh frame for infection animation"""
        self.canvas.delete(ALL)
        # Draw connections first so circles get drawn on top of lines
        self.draw_connections()
        self.draw_users()

    def init_users(self):
        """Initializes list of VisualUser objects from users"""
        for user in self.raw_users:
            self.users.append(VisualUser(user, self))

    def update_locations(self):
        """Update locations of all users"""
        for user in self.users:
            user.update_location()

    def get_fill(self, v):
        """
        Convert version number into RGB hex value

        Creates gradient covering range of colors
        """
        if v is None:
            return "white"
        b = 0
        quarter = self.versions/4
        if v < quarter:
            r = 255
            g = int(255*min((v/quarter), 1))
        elif quarter <= v < 2*quarter:
            r = int(255*max(0, (1-(v-quarter)/quarter)))
            g = 255
        elif 2*quarter <= v < 3*quarter:
            r = 0
            g = int(255*max(0, (1-(v-2*quarter)/quarter)))
            b = int(255*min(((v-2*quarter)/quarter), 1))
        else:
            g = 0
            r = int(255*min(((v-3*quarter)/quarter), 1))
            b = 255
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def draw_random_point(self):
        """Draw randomly colored point on screen"""
        fill = self.get_fill(self.start_counter % 100)
        self.start_counter += 1
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        self.canvas.create_rectangle(x, y, x+2, y+2, width=1, fill=fill)

    def timer_fired(self):
        """Called every frame refresh"""
        if self.mode == Mode.START:
            for _ in range(10):
                self.draw_random_point()
        if self.mode == Mode.MAIN:
            self.update_locations()

    def timer(self):
        """Setup timer loop"""
        if self.mode == Mode.MAIN and not self.paused:
            self.timer_fired()
            self.redraw_all()
        self.canvas.after(self.timer_delay, self.timer)

    def init_animation(self):
        """Initialize or reset animation"""
        self.users = []
        self.timer_delay = 100
        self.start_counter = 0
        self.versions = 40
        self.default_users = 20
        self.version = None
        self.paused = False
        self.mode = Mode.START
        self.draw_start_screen()
        self.error_text = None
        self.error_font_size = 20
        self.version_select = None
        self.timer()

    def start_infection(self):
        """Initialize users and start infections"""
        num_users_text = self.num_users_entry.get()
        try:
            num_users = int(num_users_text)
            if not (1 <= num_users <= 100):
                raise ValueError
        except ValueError:
            text = "Please enter a number between 1-100"
            font = ("Impact", self.error_font_size)
            if self.error_text:
                self.canvas.delete(self.error_text)
            self.error_text = self.canvas.create_text(self.cx, 0.6*self.cy, text=text, font=font)
            self.error_font_size += 2
            return
        self.infection = Infection(num_users=num_users, min_students=0, max_students=2)
        self.num_users = num_users
        self.raw_users = self.infection.network.users
        self.init_users()
        self.draw_toolbar()
        self.mode = Mode.MAIN

    def limited_infection(self):
        size_text = self.limited_entry.get()
        try:
            size = int(size_text)
            if not (1 <= size <= self.num_users):
                raise ValueError
        except ValueError:
            print("Bad input")
            return
        self.infection.limited_infection(size, self.version)
        print("Limited infection of size", size, self.num_users)

    def select_version(self):
        print("version_select", self.version_select)
        if self.version_select:
            self.toolbar_canvas.delete(self.version_select)
            print("deleted")
        if self.version is None:
            return
        y0, y1 = self.gradient
        x0, x1 = self.version*self.side, (self.version + 1)*self.side
        self.version_select = self.toolbar_canvas.create_rectangle(x0, y0, x1, y1, width="2")

    def mouse_event(self, e):
        """Process click event"""
        x, y = e.x, e.y
        if self.mode == Mode.SETUP:
            if self.button.clicked(x, y):
                self.start_infection()
        if self.mode == Mode.MAIN:
            cx, cy, r = self.limited_button
            if distance(cx, cy, x, y) < r:
                self.limited_infection()
            elif self.gradient[0] <= y <= self.gradient[1]:
                print("gradient bar", x)
                self.version = int(x / self.side)
                print(self.versions, self.version)
                self.select_version()
            else:
                for user in self.users:
                    if user.clicked(x, y):
                        print("user clicked", user)
                        user.infect()
                        break

    def key_event(self, e):
        """Process keyboard event"""
        if e.keysym == 'r':
            self.init_animation()
            self.paused = False
        elif e.keysym == 'p':
            self.paused = not self.paused
        elif e.keysym == 's' and self.mode == Mode.START:
            self.mode = Mode.SETUP
            self.draw_setup_screen()
        elif e.keysym == 'b' and self.mode == Mode.SETUP:
            self.start_infection()
        elif e.keysym == 'q':
            self.root.destroy()

Visual()