class User(object):
    """
    Basic User Class for Infection Simulation
    """
    user_id = 0

    def __init__(self, name=None, version=None):
        self.user_id = User.user_id
        User.user_id += 1
        self.name = name if name else "User{}".format(self.user_id)
        self.version = version
        self.students = []
        self.coaches = []

    def add_student(self, student):
        self.students.append(student)
        student.coaches.append(self)

    def add_students(self, students):
        for student in students:
            if student is not self:
                self.add_student(student)

    def __str__(self):
        return "User: {self.name}(v{self.version}) coaching {self.students}".format(self=self)

    def __repr__(self):
        return self.name

