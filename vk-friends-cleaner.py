import json
import urllib


class VKFriendsCleaner:

    USERS_API = 'https://api.vk.com/method/users.get?uids={0}'
    FRIENDS_API = 'https://api.vk.com/method/friends.get?uid={0}&fields=uid,firstname,lastname'

    def __init__(self):
        """
        Read data.
        """
        self.short_name = raw_input('Enter your URL: http://vk.com/')
        self.min_friends = input('Enter min friends of your friends: ')

    def find_friends(self):
        """
        Find friends with a lot of friends.
        """
        result = []

        uid = self.get_uid(self.short_name)
        api = self.FRIENDS_API.format(uid)
        response = urllib.urlopen(api)

        if response.code == 200:
            my_friends_data = json.loads(response.read())
            remaining = len(my_friends_data['response'])

            for my_friend in my_friends_data['response']:
                api = self.FRIENDS_API.format(my_friend['uid'])
                response = urllib.urlopen(api)

                if response.code == 200:
                    friends_data = json.loads(response.read())
                    if 'response' in friends_data:
                        friends_total = len(friends_data['response'])
                    else:
                        friends_total = 0

                    if friends_total >= self.min_friends:
                        my_friend['total'] = friends_total
                        result.append(my_friend)

                remaining -= 1
                print 'Remaining... ', remaining

        self.print_result(result)

    def get_uid(self, short_name):
        """
        Returns UID from a short name.
        """
        api = self.USERS_API.format(short_name)
        response = urllib.urlopen(api)
        if response.code == 200:
            user_data = json.loads(response.read())
            uid = user_data['response'][0]['uid']
            return uid
        return False

    def print_result(self, result):
        """
        Print result in a file.
        """
        f = open('friends.txt', 'w')
        sorted_result = sorted(result, key=lambda k: k['total'], reverse=True)
        for idx, my_friend in enumerate(sorted_result):
            output_template = '{0}. https://vk.com/id{1} {2} {3} ({4})\n'
            output = output_template.format(
                idx + 1,
                my_friend['uid'],
                my_friend['first_name'].encode('utf-8'),
                my_friend['last_name'].encode('utf-8'),
                my_friend['total'],
            )
            f.write(output)

if __name__ == '__main__':
    vk_friends_cleaner = VKFriendsCleaner()
    vk_friends_cleaner.find_friends()
