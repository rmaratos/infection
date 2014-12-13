from user import User


class Network(object):
    """
    Represent network of coach student relationships

    user_data should map every user to a list of their students
    """
    def __init__(self, user_data):
        self.user_data = user_data
        self.user_dict = {}
        self.load_data()

    def load_data(self):
        # Create all users
        for user in self.user_data:
            self.user_dict[user] = User(user)
        for user_name in self.user_data:
            for student_name in self.user_data[user_name]:
                # print("student_name:{} user_name:{}".format(user_name, student_name))
                coach = self.user_dict[user_name]
                student = self.user_dict[student_name]
                # print("Adding coach {} -> {}".format(coach, student))
                coach.add_student(student)

    def __str__(self):
        return "\n".join([str(user) for user in self.user_dict.values()])

test_data = {"A": ["B"],
             "B": [],
             "C": ["A", "B"]}

print(Network(test_data))

