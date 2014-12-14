from infection import Infection
from tkinter import Tk, Canvas, CENTER, ALL
import random


def distance(x0, y0, x1, y1):
    """Distance formula"""
    return ((x1-x0)**2 + (y1-y0)**2)**0.5


class VisualUser(object):
    def __init__(self, user, parent):
        self.width, self.height = parent.width, parent.height
        self.canvas = parent.canvas
        self.user = user
        self.user.visual = self
        self.r = 25
        self.x = random.randint(self.r, self.width - self.r)
        self.y = random.randint(self.r, self.height - self.r)
        self.vx = self.vy = 0
        self.user.group.version = 0

    def draw_students(self):
        x0, y0 = self.x, self.y
        for student in self.user.students:
            x1, y1 = student.visual.x, student.visual.y
            self.canvas.create_line(x0, y0, x1, y1)

    def get_fill(self):
        v = self.user.group.version
        b = 0
        if v < 50:
            r = 255
            g = int(255*min((v/50), 1))
        else:
            r = int(255*max(0, (1-(v-50)/50)))
            g = 255
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def draw(self):
        x, y = self.x, self.y
        r = self.r
        fill = self.get_fill()
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill)
        text = "{user.name}\n{user.version}".format(user=self.user)
        self.canvas.create_text(x, y, text=text, justify=CENTER)

    def update_velocity(self):
        verbose = False
        ax = ay = 0
        x0, y0 = self.x, self.y
        for student in self.user.students:
            x1, y1 = student.visual.x, student.visual.y
            if verbose:
                print("({:.2f},{:.2f})->({:.2f},{:.2f})".format(x0, y0, x1, y1))
            d = distance(x0, y0, x1, y1)
            if verbose:
                print("d:{:.2f}".format(d))
            buffer = 3*self.r
            dx, dy = (x1-x0), (y1-y0)
            k = 0.01
            if d > buffer:
                ax += k*dx
                ay += k*dy
            else:
                self.vx = self.vy = 0
        self.vx += ax
        self.vy += ay
        self.vx *= 0.9
        self.vy *= 0.9
        if (ax or ay) and verbose:
            print("a:({:.2f},{:.2f})".format(ax, ay))
            print("v:({:.2f},{:.2f})".format(self.vx, self.vy))

    def update_location(self):
        self.update_velocity()
        # print(self.x, self.y)
        self.x += self.vx
        if self.x > self.width - self.r or self.x < self.r:
            self.x -= 2*self.vx
            self.vx = 0
        self.y += self.vy
        if self.y > self.height - self.r or self.y < self.r:
            self.y -= 2*self.vy
            self.vy = 0

    def clicked(self, x, y):
        return distance(x, y, self.x, self.y) < self.r

    def infect(self):
        self.user.infect_group(self.user.group.version)
        self.user.group.version += 1


class Visual(object):
    def __init__(self, width=800, height=600, num_users=2):
        root = Tk()
        self.width, self.height = width, height
        self.num_users = num_users
        self.canvas = Canvas(root, width=width, height=height)
        self.canvas.pack()
        self.init_animation()
        root.bind("<Button-1>", lambda e: self.mouse_event(e))
        root.bind("<Key>", lambda e: self.key_event(e))
        root.mainloop()

    def draw_users(self):
        for user in self.users:
            user.draw()

    def draw_connections(self):
        for user in self.users:
            user.draw_students()

    def draw_start_screen(self):
        self.canvas.delete(ALL)
        cx, cy = self.width/2, self.height/2
        font = ("Impact", "128")
        self.canvas.create_text(cx, cy, text="INFECTION", font=font)
        font = ("Impact", 32)
        self.canvas.create_text(cx, 1.5*cy, text="Press s to Begin", font=font)

    def redraw_all(self):
        self.canvas.delete(ALL)
        self.draw_connections()
        self.draw_users()

    def init_users(self):
        for user in self.raw_users:
            self.users.append(VisualUser(user, self))

    def update_locations(self):
        for user in self.users:
            user.update_location()

    def get_fill(self, v):
        b = 0
        if v < 50:
            r = 255
            g = int(255*min((v/50), 1))
        else:
            r = int(255*max(0, (1-(v-50)/50)))
            g = 255
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def draw_random_point(self):
        # print(self.start_counter)
        fill = self.get_fill(self.start_counter % 100)
        self.start_counter += 1
        x = random.randint(0, self.width)
        y = random.randint(0, self.height)
        self.canvas.create_rectangle(x, y, x+2, y+2, width=0, fill=fill)

    def timer_fired(self):
        if self.start_screen:
            for _ in range(10):
                self.draw_random_point()
        if self.started:
            self.update_locations()

    def timer(self):
        self.timer_fired()
        if self.started:
            self.redraw_all()
        self.canvas.after(self.timer_delay, self.timer)

    def init_animation(self):
        self.users = []
        self.timer_delay = 100
        self.start_counter = 0
        self.version = 0
        self.start_screen = True
        self.draw_start_screen()
        self.help_screen = False
        self.started = False
        self.infection = Infection(num_users=self.num_users, min_students=0, max_students=2)
        self.raw_users = self.infection.network.users
        self.init_users()
        self.timer()

    def mouse_event(self, e):
        x, y = e.x, e.y
        # print("({e.x},{e.y})".format(e=e))
        for user in self.users:
            if user.clicked(x, y):
                user.infect()
                break

    def key_event(self, e):
        if e.keysym == 'r':
            self.init_animation()
            self.paused = False
        elif e.keysym == 'p':
            self.paused = not self.paused
        elif e.keysym == 's' and self.start_screen:
            self.start_screen = False
            self.started = True


Visual(num_users=20)