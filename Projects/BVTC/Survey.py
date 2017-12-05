"""
BVTC class to digitize a survey object
"""

from common import Common


class Survey(Common):
    """
    Basic Survey object
    """
    def __init__(self):
        super().__init__()
        self.project = None
        self.survey_doc = None
        self.safety_doc = None
        self.access_doc = None
        self.dates_scheduled = []
        self.dates_tracked = []


def main():
    s = Survey()
    for k, v in s.__dict__.items():
        print(k, v)


if __name__ == "__main__":
    main()
