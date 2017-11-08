# coding=utf-8
# @author hejiyan <ustchjy@gmail.com>

from flask import Response
from werkzeug.datastructures import Headers

class CrossDomainResponse(Response):
    """
    自定义 Flask 的响应包，使得任何一个路由的 OPTIONS 方法都允许跨域
    @see https://blog.miguelgrinberg.com/post/customizing-the-flask-response-class
    """

    def __init__(self, response=None, **kwargs):
        kwargs['headers'] = ''
        headers = kwargs.get('headers')

        allow_origin  = ('Access-Control-Allow-Origin', '*')
        allow_methods = ('Access-Control-Allow-Methods', 'HEAD, OPTIONS, GET, POST, DELETE, PUT')
        allow_headers = ('Access-Control-Allow-Headers',
                         'X-PINGOTHER, Referer, Accept, Origin, Content-Type, User-Agent, Contestid, Userid, Time, Sign')
        if headers:
            headers.add(*allow_origin)
            headers.add(*allow_methods)
            headers.add(*allow_headers)
        else:
            headers = Headers([allow_origin, allow_methods, allow_headers])

        kwargs['headers'] = headers
        return super(CrossDomainResponse, self).__init__(response, **kwargs)