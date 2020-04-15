class Warn:
    __id = 0
    __user = ""
    __warn = 0
    __message = ""
    peopleWarned = []

    def __init__(self, id, user, warn, message):
        self.__id = id
        self.__user = user
        self.__warn = warn
        self.__message = message

    def __getId(self):
        return self.__id

    def __getUser(self):
        return self.__user

    def setWarn(self, x):
        self.__warn = x

    def __getWarn(self):
        return self.__warn

    def __getMessage(self):
        return self.__message

    id = property(fget=__getId)
    user = property(fget=__getUser)
    warns = property(fget=__getWarn)
    message = property(fget=__getMessage)
