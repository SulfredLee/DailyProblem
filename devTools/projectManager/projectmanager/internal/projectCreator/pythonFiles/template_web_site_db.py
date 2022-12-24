content_st = """
from pymongo import MongoClient
from typing import List, Dict, Tuple
import datetime

users = {}

class MicroBlog_DC(object): # MicroBlog Data Control
    def __init__(self
                 , user_name: str = "bootcamp_admin"
                 , password: str = "bootcamp_admin1234abcd"
                 , db_server: str = "cluster0.bv9jgop.mongodb.net"
                 , db_name: str = "microblog"):
        # self.__db_client = MongoClient("mongodb+srv://bootcamp_admin:bootcamp_admin1234abcd@cluster0.bv9jgop.mongodb.net/microblog")
        self.__db_client = MongoClient(f"mongodb+srv://{user_name}:{password}@{db_server}/{db_name}")
        self.__db = self.__db_client[db_name]

    def get_all_blog_post(self) -> List:
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in self.__db.entries.find({})
        ]
        return entries_with_date

    def save_a_blog_post(self, blog_post: Dict):
        self.__db.entries.insert_one(blog_post)
"""
