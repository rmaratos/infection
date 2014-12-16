from network import Network, RandomNetwork
import random


class Infection(object):
    """Manages Network and its infection with new versions"""

    def __init__(self, data=None, num_users=None, num_coaches=None,
                 students=(None, None)):
        # Use random network if no data given
        if data:
            self.network = Network(data)
        else:
            self.network = RandomNetwork(num_users, num_coaches, students)

    def total_infection(self, user, version):
        """Infect a user with a version"""
        user.infect_group(version)

    def infect_random_user(self, version):
        """Infect random user with version"""
        user = random.choice(self.network.users)
        print("Infecting:{}".format(user))
        self.total_infection(user, version)

    def limited_infection(self, num_users, version):
        """
        Infect (up to) num_users of users with version

        Prioritizes larger groups and includes as many groups as possible until
        num_users is reached or there are no groups """
        remaining = num_users
        groups = self.network.groups
        sizes = sorted(groups.keys(), reverse=True)
        for size in sizes:
            if size > remaining:
                continue
            # Take random sample to avoid bias towards first groups
            for group in random.sample(groups[size], len(groups[size])):
                if size > remaining:
                    break
                # Ignore any group that already has that version
                if group.version == version:
                    continue
                group.infect(version)
                remaining -= size
        return num_users - remaining

    def __str__(self):
        return str(self.network)
