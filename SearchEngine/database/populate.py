from qdrant import populate
from SearchEngine.utils.utils import read_config

if __name__ == "__main__":
    config = read_config()
    populate(int(config['database']['num_populate']))
    