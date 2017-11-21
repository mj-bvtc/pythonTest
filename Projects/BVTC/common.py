import uuid
import log


class Common:
    def __init__(self):
        self.guid = uuid.uuid4()
        self.user = log.get_user()
        self.machine = log.get_machine()
        self.time_created = log.get_datetime()


def main():
    c = Common()
    print(c.__dict__)


if __name__ == "__main__":
    main()
