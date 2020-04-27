class Person:
    __id = 0
    __user = ""
    __message = []
    __messages = 0
    persons = []

    def __init__(self, id, user, message, messages):
        self.__id = id
        self.__user = user
        self.__message = message
        self.__messages = messages

    def __getId(self):
        return self.__id

    def __getUser(self):
        return self.__user

    def __getMessage(self):
        return self.__message

    def __getMessages(self):
        return self.__messages

    def setMessage(self, x):
        self.__message.append(x)

    def setMessages(self, x):
        self.__messages = x

    id = property(fget=__getId)
    user = property(fget=__getUser)
    message = property(fget=__getMessage)
    messages = property(fget=__getMessages)
