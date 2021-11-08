from flask import Flask
from getData import getImgData

app = Flask(__name__)


@app.route('/')
def default():  # put application's code here
    return 'api running -> /syncreon/bankName'


@app.route('/syncreon/<bank>')
def get_data(bank):
    fields = getImgData.extraction(bank)
    return fields


if __name__ == '__main__':
    app.run(host="0.0.0.0")
