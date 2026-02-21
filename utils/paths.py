import os
from config.settings import DATA_DIR
def get_company_dir(company):
    path = f"{DATA_DIR}/{company.lower()}"
    os.makedirs(path, exist_ok=True)
    return path

def get_domain_dir(company, domain):
    company_dir = get_company_dir(company)
    domain_dir = f"{company_dir}/{domain.lower()}"
    os.makedirs(domain_dir, exist_ok=True)
    return domain_dir