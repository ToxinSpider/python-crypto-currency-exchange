import json


class KucoinAPIException(Exception):
    def __init__(self, response):
        self.code = ''
        self.message = 'Unknown Error'
        
        try:
            json_res = response.json()
        except ValueError:
            self.message = response.content
        else:
            if 'error' in json_res:
                self.message = json_res['error']
            if 'msg' in json_res:
                self.message = json_res['msg']
            if 'message' in json_res and json_res['message'] != 'No message available':
                self.message += ' - {}'.format(json_res['message'])
            if 'code' in json_res:
                self.code = json_res['code']
            if 'data' in json_res:
                try:
                    self.message += " " + json.dumps(json_res['data'])
                except ValueError:
                    pass

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return 'KucoinAPIException {}: {}'.format(self.code, self.message)


class KucoinRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'KucoinRequestException: {}'.format(self.message)


class OrderException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'OrderException: {}'.format(self.message)


class MarketOrderException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'MarketOrderException: {}'.format(self.message)


class OrderPropertyValidationException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'MarketOrderException: {}'.format(self.message)


class LimitOrderException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'CreateOrderException: {}'.format(self.message)
