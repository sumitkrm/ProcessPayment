from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)


def check_request(request_json):
    if not request_json or not 'CreditCardNumber' in request_json or not 'CardHolder' in request_json or not 'ExpirationDate' in request_json or not 'Amount' in request_json:
        return "Bad Request"
    CreditCardNumber = request_json['CreditCardNumber']
    CardHolder = request_json['CardHolder']
    ExpirationDate = request_json['ExpirationDate']
    SecurityCode = request_json.get('SecurityCode', "")
    Amount = request_json['Amount']

    ExpirationDate_object = datetime.strptime(ExpirationDate, '%d/%m/%y')
    now = datetime.now()

    if (now >= ExpirationDate_object):
        return "Bad Request"
    
    if SecurityCode != "":
        if len(SecurityCode) != 3 or not SecurityCode.isnumeric():
            return "Bad Request"

    if len("".join(CreditCardNumber.split())) != 16 or Amount <= 0:
        return "Bad Request"


class PaymentGateway:
    def __init__(self, request_json):
        self.request_json = request_json
        
    def PremiumPaymentGateway(self):
        pass

    def ExpensivePaymentGateway(self):
        pass

    def CheapPaymentGateway(self):
        pass


@app.route("/", methods=['POST'])
def ProcessPayment():
    if request.method == 'POST':
        
        if check_request(request.json) == "Bad Request":
            return "Bad Request", 400

        Amount = request.json['Amount']

        Gateway = PaymentGateway(request.json)

        if Amount <= 20:
            Gateway.CheapPaymentGateway()

        elif Amount <= 500:
            try:
                Gateway.ExpensivePaymentGateway()
            except:
                Gateway.CheapPaymentGateway()

        else:
            retry = 4
            while retry > 0:
                try:
                    Gateway.PremiumPaymentGateway()
                    break
                except:
                    return "internal server error", 500
                retry += 1
        
        return "OK", 200

    else:
        return "bad request", 400

if __name__ == "__main__":
    app.run(debug=True)

