


class UserData:

    user_id_counter = 0

    def __init__(self, name, password):
        UserData.user_id_counter += 1
        self.user_id = UserData.user_id_counter
        self.user_name = name
        self.password = password
        self.requests = 0
        self.last_access = None

    def set_request(self, count):
        self.requests = count

    def set_last_access(self, time):
        self.last_access = time

    