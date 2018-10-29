#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : WuJinyu
# @Time    : 2018/10/29 下午2:10
"""{DESC}"""
import json
import os


class Manage():
    content = None
    josn_path = "bnyc.json"
    dir_path = "/Users/jason/Develop/Python/download/data/"

    def __init__(self):
        self.get_file_content()

    def get_file_content(self):
        with open(self.josn_path, 'rb') as f:
            self.content = json.loads(f.read())

    def check_dir_exsts(self, dir):
        path = self.dir_path
        dir_path = path + dir
        if os.path.exists(dir_path):
            print("文件夹[%s]已经存在,跳过..." % dir)
        else:
            os.makedirs(dir_path)
            print("文件夹[%s]新建成功" % dir)

    def check_file_exsts(self, filepath):
        if os.path.exists(filepath):
            print("[%s]已经存在,不需要下载啦" % filepath)
            return True

    def download_file(self, m3u8, filepath):
        path = self.dir_path + filepath
        if self.check_file_exsts(path):
            return None
        shell = "ffmpeg -threads 0 -i \"" + m3u8 + "\" -c copy -y -bsf:a aac_adtstoasc \"" + path + "\""
        res = os.system(shell)
        return res

    def run(self):
        for node in self.content:
            # 创建第一级目录
            self.check_dir_exsts(node['Name'].strip())
            # 创建二级目录
            for chapter in node['Chapter']:
                second_path = node['Name'].strip() + '/' + chapter['Category'].strip()
                self.check_dir_exsts(second_path)
                for lesson in chapter['Lesson']:
                    file_path = second_path + '/' + lesson['Name'].strip() + '.mp4'
                    try:
                        self.download_file(lesson['M3u8'], file_path)
                    except Exception:
                        with open("error.txt", 'a') as f:
                            logs = lesson['Name'] + lesson['M3u8'] + "下载失败\n"
                            f.write(logs)
            break


if __name__ == "__main__":
    manage = Manage()
    manage.run()
