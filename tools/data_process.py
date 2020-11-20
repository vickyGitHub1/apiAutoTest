#!/usr/bin/env/python3
# -*- coding:utf-8 -*-
"""
@project: apiAutoTest
@author: zy7y
@file: data_process.py
@ide: PyCharm
@time: 2020/11/18
"""
from tools import *


class DataProcess:
    response_dict = {}
    header = {}
    null_header = {}

    @classmethod
    def save_response(cls, key: str, value: object) -> None:
        """
        保存实际响应
        :param key: 保存字典中的key，一般使用用例编号
        :param value: 保存字典中的value，使用json响应
        """
        cls.response_dict[key] = value
        logger.info(f'添加key: {key}, 对应value: {value}')

    @classmethod
    def handle_path(cls, path_str: str) -> str:
        """路径参数处理
        :param path_str: 带提取表达式的字符串 /&$.case_005.data.id&/state/&$.case_005.data.create_time&
        上述内容表示，从响应字典中提取到case_005字典里data字典里id的值，假设是500，后面&$.case_005.data.create_time& 类似，最终提取结果
        return  /511/state/1605711095
        """
        # /&$.case.data.id&/state/&$.case_005.data.create_time&
        return rep_expr(path_str, cls.response_dict)

    @classmethod
    def handle_header(cls, is_token: str, response: dict, reg) -> dict:
        """处理header"""
        if is_token == '写':
            cls.header['Authorization'] = extractor(response, reg)
            return cls.header
        elif is_token == '':
            return cls.null_header
        else:
            return cls.header

    @classmethod
    def handler_files(cls, file_obj: str) -> object:
        """file对象处理方法
        :param file_obj: 上传文件使用，格式：接口中文件参数的名称:"文件路径地址"/["文件地址1", "文件地址2"]
        实例- 单个文件: &file&D:
        """
        # todo 待完成
        if file_obj == '':
            return None
        for k, v in convert_json(file_obj).items():
            # 多文件上传
            if isinstance(v, list):
                files = []
                for path in v:
                    files.append((k, (open(path, 'rb'))))
            else:
                # 单文件上传
                files = {k: open(v, 'rb')}
        return files

    @classmethod
    def handle_data(cls, variable: str) -> dict:
        """请求数据处理
        :param variable: 请求数据，传入的是可转换字典/json的字符串,其中可以包含变量表达式
        return 处理之后的json/dict类型的字典数据
        """
        if variable == '':
            return
        data = rep_expr(variable, cls.response_dict)
        variable = convert_json(data)
        logger.info(f'最终的请求数据如下: {variable}')
        return variable




if __name__ == '__main__':
    print(convert_json("""{"files":["D:\\apiAutoTest\\data\\case_data - 副本.xls", "D:\\apiAutoTest\\data\\case_data.xlsx"]}"""))