# -*- coding: utf-8 -*-

import os
import os.path
import pickle


class FileManager:
    # pylint: disable=all
    @staticmethod
    def exists(path):
        return os.path.exists(path)

    @staticmethod
    def write(path, data):
        with open(path, "w") as f:  #
            f.write(data)

    @staticmethod
    def append(path, data):
        with open(path, "w+") as f:
            f.write(data)

    @staticmethod
    def check_dir(path):
        if not os.path.isdir(path):
            os.makedirs(path)

    @staticmethod
    def read(path):
        with open(path) as f:
            return f.read()

    @staticmethod
    def remove(path):
        if FileManager.exists(path):
            os.remove(path)

    @staticmethod
    def write_pickle(path, obj: any):
        with open(path, "wb") as fw:
            pickle.dump(obj, fw)

    @staticmethod
    def read_pickle(path):
        with open(path, "rb") as fr:
            return pickle.load(fr)
