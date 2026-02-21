from utils.paths import get_company_dir

class BaseVectorHnadler:
    def __init__(self):
        pass

    def create_index(self):
        raise NotImplementedError("create_index method not implemented")
    
    def write_index(self, path, index):
        raise NotImplementedError("write_index method not implemented")
    
    def load_company_data_and_index(path):
        raise NotImplementedError("write_index method not implemented")