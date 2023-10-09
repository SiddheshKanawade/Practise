class LockElementithTask:
    def __init__(self, key, lock_name, nested, wcet):
        self.key = key
        self.type = lock_name
        self.nested = []
        self.wcet = wcet

    