class User(object):
    """
    Basic User Class for Infection Simulation
    """
    user_id = 0

    def __init__(self, name, version=None):
        self.user_id = User.user_id
        User.user_id += 1
        self.name = name
        self.version = version
        self.students = []
        self.coaches = []

    def add_student(self, student):
        self.students.append(student)
        student.coaches.append(self)

    def __str__(self):
        return "User: {self.name} ({self.user_id})".format(self=self)

    def __repr__(self):
        return str(self)

