class Log(object):
    def log(self, message):
        print(str(message))

    def exception(self, message):
        print(str(message))


logging = Log()
