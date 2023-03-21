import logging
import datetime
from typing import Dict, List, Any, Union
import pandas as pd

def get_datetime_safe(data: Any) -> datetime.datetime:
    if isinstance(data, str):
        return datetime.datetime.strptime(data, "%y-%m-%d")
    elif isinstance(data, datetime.datetime):
        return data
    elif isinstance(data, datetime.date):
        return datetime.datetime(data.year, data.month, data.day)

class IDMapp_Ele(object):
    def __init__(self):
        self.listing_id: str = ""
        self.code: str = ""
        self.start_date: datetime.datetime = None
        self.end_date: datetime.datetime = None

    def __str__(self):
        return f"{self.code},{self.listing_id},{self.start_date},{self.end_date}"

    @staticmethod
    def get_row_key() -> str:
        return "code"

    @staticmethod
    def create_ele(row: Dict):
        ele = IDMapp_Ele()

        ele.code = row["code"]
        ele.listing_id = row["listing_id"]
        ele.start_date = get_datetime_safe(data=row["start_date"])
        ele.end_date = get_datetime_safe(data=row["end_date"])

        return ele

class CompanyMap_Ele(object):
    def __init__(self):
        self.listing_id: str = ""
        self.company_id: str = ""
        self.company_name: str = ""
        self.start_date: datetime.datetime = None
        self.end_date: datetime.datetime = None

    def __str__(self):
        return f"{self.listing_id},{self.company_id},{self.company_name}"

    @staticmethod
    def get_row_key() -> str:
        return "listing_id"

    @staticmethod
    def create_ele(row: Dict):
        ele = CompanyMap_Ele()

        ele.listing_id = row["listing_id"]
        ele.company_id = row["company_id"]
        ele.company_name = row["company_name"]
        ele.start_date = row["start_date"]
        ele.end_date = row["end_date"]

        return ele

class GroupMap_Ele(object):
    def __init__(self):
        self.listing_id: str = ""
        self.ref_industry_code: str = ""
        self.ref_industry_group: str = ""
        self.ref_sector_code: str = ""
        self.start_date: datetime.datetime = None
        self.end_date: datetime.datetime = None

    def __str__(self):
        return f"{self.listing_id},{self.ref_industry_code},{self.ref_industry_group},{self.ref_sector_code},{self.start_date},{self.end_date}"

    @staticmethod
    def get_row_key() -> str:
        return "listing_id"

    @staticmethod
    def create_ele(row: Dict):
        ele = GroupMap_Ele()

        ele.listing_id = row["listing_id"]
        ele.ref_industry_code = row["ref_industry_code"]
        ele.ref_industry_group = row["ref_industry_group"]
        ele.ref_sector_code = row["ref_sector_code"]
        ele.start_date = get_datetime_safe(data=row["start_date"])
        ele.end_date = get_datetime_safe(data=row["end_date"])

        return ele

