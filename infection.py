from network import Network, RandomNetwork
import random


class Infection(object):
    def __init__(self, data=None, num_users=None, min_students=None, max_students=None):
        # Use random network if no data given
        if data:
            self.network = Network(data)
        else:
            self.network = RandomNetwork(num_users, min_students, max_students)

    def total_infection(self, user, version):
        """Infect a user with a version"""
        user.infect_group(version)

    def infect_random_user(self, version):
        # print(type(self.network.users))
        user = random.choice(self.network.users)
        print("Infecting:{}".format(user))
        self.total_infection(user, version)

    def __str__(self):
        return str(self.network)


test_data = {"A": ["B"],
             "B": [],
             "C": [],
             "D": ["C"]}
# i = Infection(test_data)
i = Infection(num_users=10, min_students=0, max_students=2)
print(i.network.get_groups())
# print(i)
i.infect_random_user(1.0)
print(i.network.get_groups())
# print(i)