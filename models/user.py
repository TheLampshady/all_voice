from datetime import datetime


class BaseUser(object):

    def log_error(self, user_id, message):
        raise NotImplementedError("Not Implemented.")

    def get_error(self, user_id):
        raise NotImplementedError("Not Implemented.")


class AllVoiceUser(BaseUser):
    _database = {}
    _db_limit = 50

    @classmethod
    def log_error(cls, user_id, message):
        cls._database[user_id] = (message[:64], datetime.now())
        cls.clean()

    @classmethod
    def get_error(cls, user_id):
        entry = cls._database.get(user_id)
        return (entry[0] if entry else "") or ""

    @classmethod
    def clean(cls):
        if len(cls._database) > cls._db_limit:
            sorted_db = sorted(cls._database.items(), key=lambda x: x[1][1])
            for x in range(0, len(cls._database) - cls._db_limit):
                key = sorted_db[x][0]
                cls._database.pop(key)

    @classmethod
    def reset(cls):
        cls._database = {}


