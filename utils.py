# coding=utf8
from flask import jsonify, make_response
from functools import wraps
import datetime

def json_format(func):

    # 将返回值 jsonify 的装饰器
    # :param func: 欲格式化的函数
    # :return: jsonify 的返回值

    @wraps(func)
    def wrapper(*args, **kwargs):
        res = make_response(jsonify(func(*args, **kwargs)))
        res.headers['Content-Type'] = 'application/json; charset=utf-8'
        return res

    return wrapper


def success(data = None):
    # 成功的返回格式
    # :param data: 对象数据
    # :return:
    if data:
        return {
            'data': data,
            'status': {
                'code': 0,
                'message': 'success'
            }
        }
    else:
        return {
            'status': {
                'code': 0,
                'message': 'success'
            }
        }

def gen_service(id, description, time = None):
    if (not time):
        time = datetime.datetime.now().isoformat() + "+0800"

    data = {
        "id": id,
        "description": description,
        "time": time
    }

    return data
