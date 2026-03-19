from user_data import UserData




class AuthenticationData:

    def __init__(self):
        self.data = {}  

    def register_user(self, name, password):
        user = UserData(name, password)
        self.data[name] = user

    def check_login(self, user_name, password):
        user = self.data.get(user_name)

        if user and user.password == password:
            return True
        
        return False
    