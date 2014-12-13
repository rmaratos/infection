from user import User
import random
import copy


class Group(object):
    """Group of connected users"""
    def __init__(self, users=None):
        if users:
            self.users = users
        else:
            self.users = []

    def add_user(self, user):
        """Add new user to group"""
        self.users.append(user)
        user.group = self

    def length(self):
        return len(self.users)

    def infect(self, version):
        """Infect all users within a group with version"""
        for user in self.users:
            user.infect(version)

    def __str__(self):
        return "Group({}):{}".format(self.length(), self.users)

    def __repr__(self):
        return str(self)


class Network(object):
    """
    Represent network of coach student relationships

    If supplied, user_data should map every user to a list of their students
    Otherwise, self.users should be already defined
    """
    def __init__(self, user_data=None):
        if user_data:
            self.users = None
            self.user_data = user_data
            self.load_data()
        self.groups = None
        self.find_groups()

    def load_data(self):
        # Used to temporarily map user names to instances before connections are made
        temp_user_dict = {}

        # Create all users
        for user in self.user_data:
            user_dict[user] = User(user)

        # Create student coach relationships
        for user_name in self.user_data:
            for student_name in self.user_data[user_name]:
                # Get student and coach instances
                coach = temp_user_dict[user_name]
                student = temp_user_dict[student_name]
                coach.add_student(student)

        # Only need user instances from here on out
        self.users = list(temp_user_dict.values())

    def find_group(self, not_grouped):
        """Find new group within not yet grouped users"""
        to_search = set([not_grouped[0]])
        group = Group()
        # Loop until no more connections to add
        while to_search:
            # Get first user and add to group
            new_user = to_search.pop()
            group.add_user(new_user)
            not_grouped.remove(new_user)
            connections = (new_user.students + new_user.coaches)
            for connection in connections:
                if connection not in group.users:
                    to_search.add(connection)
        return group

    def find_groups(self):
        """Partition set of users into connected groups"""
        groups = {}
        not_grouped = copy.copy(self.users)
        # loop until all users have been put into a group
        while not_grouped:
            group = self.find_group(not_grouped)
            size = group.length()
            # Map size of group to list of groups of that size
            if size in groups:
                groups[size].append(group)
            else:
                groups[size] = [group]
        self.groups = groups

    def get_groups(self):
        """ Unions every group into one list """
        groups = []
        for group_size in self.groups.values():
            groups += group_size
        return groups

    def __str__(self):
        return "\n".join([str(user) for user in self.users])


class RandomNetwork(Network):
    """
    Subclass of Network for creating randomly generated networks

    num_users - Total number of users in network
    min_students - Minimum number of students a user can have
    max_students - Maximum number of students a user can have
    """
    def __init__(self, num_users, min_students, max_students):
        # Generate list of users
        self.users = [User() for _ in range(num_users)]
        for user in self.users:
            num_students = random.randint(min_students, max_students)
            # Randomly sample users to add as students for a user
            students = random.sample(self.users, num_students)
            user.add_students(students)
        super(RandomNetwork, self).__init__()


