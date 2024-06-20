from qdrant import populate_qdrant
from SearchEngine.utils.utils import read_config

if __name__ == "__main__":
    config = read_config()
    populate_qdrant(int(config['database']['num_populate']))