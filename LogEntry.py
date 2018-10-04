class LogEntry:
    def __init__(self, asctime, msecs, process, levelname, name, request_ids, user_identitys, instance, message):
        self.asctime = asctime
        self.msecs = msecs
        self.process = process
        self.levelname = levelname
        self.name = name
        self.request_ids = request_ids
        self.user_identitys = user_identitys
        self.instance = instance
        self.message = message
