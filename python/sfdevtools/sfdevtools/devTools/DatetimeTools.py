from datetime import datetime
from nanoid import generate # poetry add nanoid

def get_current_date() -> str:
    return datetime.utcnow().strftime("%Y%m%d")

def get_current_datetime() -> str:
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")

def get_random_file_name(file_name: str) -> str:
    rid = generate(size=10)
    return f'{get_current_datetime()}_{rid}_{file_name}'
