from datetime import time

class FundManager(object):
    def __init__(self):
        self.__total_members: int = 0
        self.__office_size: int = 0

    def tell_total_members(self) -> int:
        return self.__total_members

    def add_member(self, num: int):
        self.__total_members += num

    def clear_member(self):
        self.__total_members = 0

    def set_office_size(self, size: int):
        self.__office_size = size

    def get_office_size(self):
        return self.__office_size

    def clear_office_size(self):
        self.__office_size = 0
