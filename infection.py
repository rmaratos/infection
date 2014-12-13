from network import Network, RandomNetwork
import random


class Infection(object):
    def __init__(self, data=None, num_users=None, min_students=None, max_students=None):
        if data:
            self.network = Network(data)
        else:
            self.network = RandomNetwork(num_users, min_students, max_students)

    def infect(self, user, version, seen=set()):
        user.version = version
        # TODO: change from Naive recursive infection
        for person in (user.students + user.coaches):
            if person not in seen:
                seen.add(person)
                self.infect(person, version, seen)

    def infect_random_user(self, version):
        # print(type(self.network.users))
        user = random.choice(self.network.users)
        print("Infecting:{}".format(user))
        self.infect(user, version)

    def __str__(self):
        return str(self.network)


test_data = {"A": ["B"],
             "B": [],
             "C": ["A", "B"]}

i = Infection(num_users=10, min_students=0, max_students=2)
print(i)
i.infect_random_user(1.0)
print(i)