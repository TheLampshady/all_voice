from datetime import datetime


class BaseUser(object):
    """
    Base user class for extending. Used by skills for at least logging
        but can be used for more.
    """

    def log_error(self, user_id, message):
        raise NotImplementedError("Not Implemented.")

    def get_error(self, user_id):
        raise NotImplementedError("Not Implemented.")


class AllVoiceUser(BaseUser):
    _database = {}
    _db_limit = 50

    @classmethod
    def log_error(cls, user_id, message):
        """
        Saves error for usage later.
        :param user_id: <str> Unique user ID
        :param message: <str> Message to save
        """
        cls._database[user_id] = (message[:64], datetime.now())
        cls.clean()

    @classmethod
    def get_error(cls, user_id):
        """
        Retrieves error from storage. Returns blank str otherwise
        :param user_id: <str>
        :return: <str>
        """
        entry = cls._database.get(user_id)
        return (entry[0] if entry else "") or ""

    @classmethod
    def clean(cls):
        """Task for clearing old entries"""
        if len(cls._database) > cls._db_limit:
            sorted_db = sorted(cls._database.items(), key=lambda x: x[1][1])
            for x in range(0, len(cls._database) - cls._db_limit):
                key = sorted_db[x][0]
                cls._database.pop(key)

    @classmethod
    def reset(cls):
        """Clears DB"""
        cls._database = {}


