import os
import pickle

# config = {'name': 'pyprobar', 'version': 107}
# save("pyprobar/version_config.pkl", config)

def version_config(update=False):
    filename = os.path.join(os.path.dirname(__file__), 'version_config.yaml')
    config = yaml_load(filename)
    # config = load(filename)
    if update:
        config["version"] += 1
        yaml_dump(filename, config)
        # save(filename, config)
    __version__ = '0.' + '.'.join(list(str(config["version"])))
    __name__ = config["name"]
    return __version__, __name__

def save(filename, file):
    with open(filename, 'wb') as fw:
        pickle.dump(file, fw)

def load(filename):
    with open(filename, 'rb') as fi:
        file = pickle.load(fi)
    return file

def yaml_dump(filepath, data):
    from yaml import dump
    try:
        from yaml import CDumper as Dumper
    except ImportError:
        from yaml import Dumper
    with open(filepath, "w", encoding='utf-8') as fw:
        fw.write(dump(data, Dumper=Dumper))
        
def yaml_load(filepath):
    from yaml import load
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
    with open(filepath, 'r', encoding="utf-8") as stream:
    #     stream = stream.read()
        content = load(stream, Loader=Loader)
    return content

# Enables the dictionary to be dot operated
class _Dict_enhance(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

def dict_dotable(dic):
    '''
    : input: a dictionary
    : output: an enhanced dictionary
    Example:
        enhance_dic = dict_dotable(dic)
    then, you can operate an enhanced dictionary like this:
        enhance_dic.key1.key2. ...
    '''
    dic = _Dict_enhance(dic)
    for i in dic:
        if type(dic[i]) == dict:
            dic[i] = dict_dotable(dic[i])
    return dic



