class Person:
    def __init__(self, name, username, profile_picture_url, bio, followers_count, following_count):
        self.name = name
        self.username = username
        self.profile_picture_url = profile_picture_url
        self.bio = bio
        self.followers = []
        self.following = []
        self.followers_count = followers_count
        self.following_count = following_count

    def __str__(self):
        return f"Name: {self.name}\n Username: {self.username}\n Profile Picture URL: {self.profile_picture_url}\n Bio: {self.bio}"

    def add_follower(self, follower):
        self.followers.append(follower)

    def add_followers_list(self, followers_list):
        self.followers = followers_list + self.followers

    def add_following_list(self, following_list):
        self.following = following_list + self.following

    def add_following(self, following):
        self.following.append(following)
