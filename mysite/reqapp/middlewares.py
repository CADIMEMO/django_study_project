from django.http import HttpRequest
import datetime
import time

def setup_useragent_middleware(get_response):
    print('initial call')
    def middleware(request: HttpRequest):
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        return response
    return middleware


class CountReqMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.response_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requests count:', self.requests_count)
        response = self.get_response(request)
        self.response_count += 1
        print('response count:', self.response_count)
        return response



class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ips = {}

    def __call__(self, request: HttpRequest):

        user_ip = request.META['REMOTE_ADDR']

        if not user_ip in self.ips:
            self.ips[user_ip] = datetime.datetime.now()
        if self.ips[user_ip] + datetime.timedelta(minutes=1) < datetime.datetime.now():
            self.ips[user_ip] = datetime.datetime.now()
            response = self.get_response(request)
            return response
        else:
            print(datetime.datetime.now())
            print('Ошибка. Запросы чаще чем раз в минуту')
            raise Exception('Ошибка. Запросы чаще чем раз в минуту')



