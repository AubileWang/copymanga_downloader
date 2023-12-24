import os
import vthread
from rich import print
from spider_toolbox import requests_tools, file_tools


# @vthread.pool(20)
def download(url, workdir, name):
    resp = requests_tools.byte_downloader(url,
                                          workdir=workdir,
                                          file_name=name,
                                          file_type='jpg',
                                          timeout=3,
                                          retry_num=20,
                                          retry_sleep=1)
    workdir = os.path.join(workdir, name) + '.jpg'
    if resp:
        print(f'[white]{workdir}下载完成[/]\n', end='')
    else:
        print(f'[red]{workdir} 下载出错[/]')
