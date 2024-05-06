class Person:
    def __init__(self, name, username, profile_picture_url, bio):
        self.name = name
        self.username = username
        self.profile_picture_url = profile_picture_url
        self.bio = bio
        self.followers = []
        self.following = []

    def __str__(self):
        return f"Name: {self.name}, Username: {self.username}, Profile Picture URL: {self.profile_picture_url}, Bio: {self.bio}"

    def add_follower(self, follower):
        self.followers.append(follower)

    def add_following(self, following):
        self.following.append(following)
