import os
from config.settings import DATA_DIR
def get_company_dir(company):
    path = f"{DATA_DIR}/{company.lower()}"
    os.makedirs(path, exist_ok=True)
    return path