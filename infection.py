from network import Network, RandomNetwork
import random
import copy


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

    def limited_infection(self, num_users, version):
        """Infect num_users of users with version"""
        remaining = num_users
        groups = self.network.groups
        sizes = sorted(groups.keys(), reverse=True)
        for size in sizes:
            if size > remaining:
                continue
            for group in groups[size]:
                if size > remaining:
                    break
                group.infect(version)
                remaining -= size
        return num_users - remaining

    def __str__(self):
        return str(self.network)

#
# test_data = {"A": ["B"],
#              "B": [],
#              "C": [],
#              "D": ["C"]}
# i = Infection(test_data)
i = Infection(num_users=10, min_students=0, max_students=2)
print(i.network.get_groups())
# print(i)
print(i.limited_infection(5, 3))
print(i.network.get_groups())
# print(i)