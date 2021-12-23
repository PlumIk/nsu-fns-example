import requests

url = f'http://10.35.7.17:8190/HMC/qr'
payload = {
    'id': 1,
    'qr': "t=20210506T153900&s=263.50&fn=9960440300049147&i=36086&fp=3305237468&n=1"
}
headers = {
    # 'Host': self.HOST,
    # 'Accept': self.ACCEPT,
    # 'Device-OS': self.DEVICE_OS,
    # 'Device-Id': self.DEVICE_ID,
    # 'clientVersion': self.CLIENT_VERSION,
    # 'Accept-Language': self.ACCEPT_LANGUAGE,
    # 'User-Agent': self.USER_AGENT,
}

resp = requests.post(url, json=payload)