import requests
import json
import sys

# TODO: retrieve account details such as name of the account_holder as well


class MeroShare:
    def __init__(self, username, password, bank_id):
        self.username = username
        self.password = password
        self.token = self.get_auth_token(bank_id)
        self.toCheck = ['branchName', 'accountNumber', 'bankCode', 'accountType', 'accountBranch', 'customerId',
                        'boid', 'branchCode', 'branchId', 'applyBoid', 'bankId', 'clientCode', 'branchName', 'bankName', 'crnNumber']
        for i in self.toCheck:
            setattr(self, i, None)
        self.check_required()

    @staticmethod
    def get_capital_details():
        response = requests.get(
            'https://webbackend.cdsc.com.np/api/meroShare/capital/')
        return json.loads(response.text)

    def check_required(self):
        for i in self.toCheck:
            if not getattr(self, i):
                try:
                    ownDetail = self.get_own_details()
                    self.boid = ownDetail['demat']
                    self.clientCode = ownDetail['clientCode']
                    self.name = ownDetail['name']
                except KeyError:
                    sys.exit(
                        "Your Demat account has been expired! Renew your Demat account via online payment or visit your DP.")
                break

    def get_my_portfolio(self):
        data = {
            "sortBy": "script",
            "demat": [self.boid],
            "clientCode": self.clientCode,
            "page": 1,
            "size": 200,
            "sortAsc": True
        }

        return self.send_authorized_request("https://webbackend.cdsc.com.np/api/meroShareView/myPortfolio/", "post", data)

    def get_auth_token(self, bank_id):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        }

        payload = {
            'clientId': bank_id,
            'username': self.username,
            'password': self.password,
        }

        response = requests.post(
            'https://webbackend.cdsc.com.np/api/meroShare/auth/', headers=headers, data=json.dumps(payload))

        if not response.status_code == 200:
            print("Invalid Login Credentials!")
            exit(1)

        self.token = response.headers['Authorization']

        return self.token

    def send_authorized_request(self, url, type='get', data=None, parse=True):
        if not self.token:
            print("Please authorized first with getAuthToken method!!")

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'application/json, text/plain, */*',
            'Authorization': self.token,
            'Content-Type': 'application/json',
        }
        if parse:
            data = json.dumps(data)

        if type == 'get':
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, data=data)

        return json.loads(response.text)

    def get_own_details(self):
        return self.send_authorized_request("https://webbackend.cdsc.com.np/api/meroShare/ownDetail/")
