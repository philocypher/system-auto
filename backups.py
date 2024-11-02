#!/usr/bin/env python3
import logging
import platform
from multiprocessing import Pool
import subprocess
import os
import sys

logging.basicConfig(level=logging.INFO,filename='backup-log.log' ,filemode='a')

if len(sys.argv) == 3:
    src = sys.argv[1]
    dest = sys.argv[2]
else:
      print(f"Pass the source and destination to backup your data.\nSyntax: {sys.argv[0]} [source] [destination]")
      sys.exit()
def run(folder):
#       print(folder)
        subprocess.call(["rsync", "-arqh", src + folder, dest])

class App:
    @staticmethod
    def init():
        folders = []
        try:
            for dirpath, dirname, files in os.walk(src):
                    for folder in dirname:
                            folders.append(dirname)
                    break
        except FileNotFoundError as e:
            logging.INFO

        with Pool(len(folders)) as p:
            p.map(run, folders[0])


if __name__ == "__main__":
    App.init()
