import configparser

def detect_language(text):
    def is_english(text):
        return all(ord(char) < 128 for char in text)
    
    def is_persian(text):
        return any('\u0600' <= char <= '\u06FF' or
                '\uFB50' <= char <= '\uFDFF' or
                '\uFE70' <= char <= '\uFEFF' for char in text)
    
    if is_english(text):
        return "English"
    elif is_persian(text):
        return "Persian"
    else:
        return "Unknown"

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config