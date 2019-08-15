
import os

import yaml


# 之前直接拼接的路径，修改了一下，用现在下面这种方法，可以支持linux和windows等不同的平台，
# os.path.split()和os.path.join()，不要直接+'\\xxx\\ss'这样
BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_PATH = os.path.join(BASE_PATH, 'dataconfig')
CONFIG_FILE=os.path.join(CONFIG_PATH,'config.yml')


class YamlReader:
    def __init__(self, yamlf=CONFIG_FILE):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在！')
        self._data = None

    @property
    def data(self):
        # 如果是第一次调用data，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))  # load后是个generator，用list组织成列表
        return self._data[0]

