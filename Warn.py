class Warn:
    __id = 0
    __user = ""
    __warns = 0
    __message = ""
    peopleWarned = []

    def __init__(self, id, user, warns, message):
        self.__id = id
        self.__user = user
        self.__warns = warns
        self.__message = message

    def __getId(self):
        return self.__id

    def __getUser(self):
        return self.__user

    def setWarns(self, x):
        self.__warns = x

    def __getWarns(self):
        return self.__warns

    def __getMessage(self):
        return self.__message

    id = property(fget=__getId)
    user = property(fget=__getUser)
    warns = property(fget=__getWarns)
    message = property(fget=__getMessage)
