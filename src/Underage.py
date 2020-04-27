class Underage:
    __id = 0
    __user = ""
    __evidence = ""
    underages = []

    def __init__(self, id, user, evidence):
        self.__id = id
        self.__user = user
        self.__evidence = evidence

    def __getId(self):
        return self.__id

    def __getUser(self):
        return self.__user

    def __getEvidence(self):
        return self.__evidence

    id = property(fget=__getId)
    user = property(fget=__getUser)
    evidence = property(fget=__getEvidence)
