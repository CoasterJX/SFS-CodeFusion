from .PathManager import PM

class InternalUser:

    def __init__(self, name) -> None:
        self.name = name
        user_info = PM.get_user(self.name)
        self.groups = user_info["groups"]
        

