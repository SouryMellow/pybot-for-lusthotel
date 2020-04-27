class Verified:
    __id = 0
    __user = ""
    __gender = ""
    __country = ""
    verifieds = []

    def __init__(self, id, user, gender, country):
        self.__id = id
        self.__user = user
        self.__gender = gender
        self.__country = country

    def __getId(self):
        return self.__id

    def __getUser(self):
        return self.__user

    def __getGender(self):
        return self.__gender

    def __getCountry(self):
        return self.__country

    id = property(fget=__getId)
    user = property(fget=__getUser)
    gender = property(fget=__getGender)
    country = property(fget=__getCountry)
