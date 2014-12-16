class User(object):
    """
    Basic User Class for Infection Simulation

    name and version are both optional and will default to an auto-incrementing
    user_id and None respectively
    """

    # Used to uniquely identify users
    user_id = 0

    def __init__(self, name=None, version=None):
        self.user_id = User.user_id
        User.user_id += 1
        self.name = name if name else "User{}".format(self.user_id)
        self.version = version
        self.students = []
        self.coaches = []
        self.group = None

    def add_student(self, student):
        """Add student to user, and add this user as their coach"""
        # Prevent self referential coaching
        if student is not self:
            self.students.append(student)
            student.coaches.append(self)

    def add_students(self, students):
        """Add list of students to user"""
        for student in students:
                self.add_student(student)

    def infect(self, version):
        """Infect user by changing their version"""
        self.version = version

    def infect_group(self, version):
        self.group.infect(version)

    def __str__(self):
        return "{self.name}({self.version})".format(self=self)

    def __repr__(self):
        return str(self)
