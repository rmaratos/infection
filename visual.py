from infection import Infection
from tkinter import Tk, Canvas, CENTER, ALL
import random


def distance(x0, y0, x1, y1):
    return (float(x1-x0)**2 + float(y1-y0)**2)**0.5


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

    def draw_students(self):
        x0, y0 = self.x, self.y
        for student in self.user.students:
            x1, y1 = student.visual.x, student.visual.y
            self.canvas.create_line(x0, y0, x1, y1)

    def draw(self):
        x, y = self.x, self.y
        r = self.r
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="white")
        text = "{user.name}\n{user.version}".format(user=self.user)
        self.canvas.create_text(x, y, text=text, justify=CENTER)

    def update_velocity(self):
        ax = ay = 0
        x0, y0 = self.x, self.y
        for student in self.user.students:
            x1, y1 = student.visual.x, student.visual.y
            print("({:.2f},{:.2f})->({:.2f},{:.2f})".format(x0, y0, x1, y1))
            d = distance(x0, y0, x1, y1)
            print("d:{:.2f}".format(d))
            dx, dy = float(x1-x0), (y1-y0)
            if d > self.r + 5:
                if dx:
                    ax += 0.001*dx
                if dy:
                    ay += 0.001*dy
            else:
                self.vx = 0
                self.vy = 0
            # print("ax,ay", ax, ay)
        self.vx += ax
        self.vy += ay
        self.vx *= 0.9
        self.vy *= 0.9
        if ax or ay:
            print("a:({:.2f},{:.2f})".format(ax, ay))
            print("v:({:.2f},{:.2f})".format(self.vx, self.vy))

    def update_location(self):
        self.update_velocity()
        # print(self.x, self.y)
        self.x += self.vx
        if self.x > self.width - self.r or self.x < self.r:
            self.x -= self.vx
            self.vx = 0
        self.y += self.vy
        if self.y > self.height - self.r or self.y < self.r:
            self.y -= self.vy
            self.vy = 0



class Visual(object):
    def __init__(self, width=800, height=600):
        root = Tk()
        self.width, self.height = width, height
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

    def timer_fired(self):
        self.update_locations()

    def timer(self):
        if not self.paused:
            self.timer_fired()
            self.redraw_all()
        self.canvas.after(self.timer_delay, self.timer)

    def init_animation(self):
        self.users = []
        self.paused = True
        self.timer_delay = 100
        self.infection = Infection(num_users=100, min_students=0, max_students=2)
        self.raw_users = self.infection.network.users
        self.init_users()
        self.timer()

    def mouse_event(self, e):
        print("({e.x},{e.y})".format(e=e))

    def key_event(self, e):
        if e.keysym == 'r':
            self.init_animation()
            self.paused = False
        elif e.keysym == 'p':
            self.paused = not self.paused


Visual()