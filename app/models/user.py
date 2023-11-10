class User:
    def __init__(self, username, email, password, user_id=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'user_id': str(self.user_id),
            'username': self.username,
            'email': self.email,
            'password':self.password
        }