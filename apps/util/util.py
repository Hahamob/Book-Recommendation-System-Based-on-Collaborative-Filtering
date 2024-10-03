# 工具模块
import os
import random
from rpvputil.util.abstractutil import AbstractUtil


class Util(AbstractUtil):

    # 获取当前时间
    def getCurrentTime(self):
        return super().getCurrentDate().strftime('%Y-%m-%d %H:%M:%S')

    # 获取时间戳+六位随机数，用于上传文件名
    def getCurrentTimeRandom(self):
        strTemp = ""
        for i in range(6):
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            strTemp += ch
        return super().getCurrentDateLong() + "_" + strTemp

    # 定格文件上传格式化路径和文件名方法
    def upload_path_handler(self, instance, filename):
        fileType = os.path.splitext(filename)[1]  # .jpg  获取文件名后缀
        filename = self.getCurrentTimeRandom() + fileType  # 产生一个随机文件名称
        return "{file}".format(file=filename)  # 保存路径和格式
