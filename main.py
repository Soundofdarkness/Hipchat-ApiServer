from flask import Flask, request
import requests
import config
import datetime
app = Flask(__name__)

@app.route('/voidtrader', methods=['POST'])
def voidtrader():
    if request.method == 'POST':
        vt_data = requests.get('http://content.warframe.com/dynamic/worldState.php').json()
        state = requests.get('http://content.warframe.com/dynamic/worldState.php').json()
        data = state['VoidTraders'][0]
        node = data['Node']
        act_raw = data['Activation']['sec']
        exp_raw = data['Expiry']['sec']
        act = datetime.datetime.fromtimestamp(act_raw).strftime('%Y-%m-%d %H:%M:%S')
        exp = datetime.datetime.fromtimestamp(exp_raw).strftime('%Y-%m-%d %H:%M:%S')

        if 'Pluto' in node:
            node = 'Orcus Relay'
        elif 'Mercury' in node:
            node = 'Larunda Relay'
        elif 'Saturn' in node:
            node = 'Kronia Relay'

        ex = '{' \
             '"color": "purple",' \
             '"message": "Baro Ki Teer will arrive at' + str(act) + ' until '+ str(exp) + ' on ' + node + '",' \
             '"notify": false,' \
             '"message_format": "text"' \
             '}'
        requests.post(config.warframe_url, data=data)


app.run(host='0.0.0.0', port='8080')