import urllib2, base64, json
from flask import render_template,Flask,jsonify

app = Flask(__name__)
global op1
op1 = []

def get_ticket():
    global op1
    username = 'karnanikushal@gmail.com'
    password = 'Tcs!2345'
    url = "https://devops-poc.atlassian.net/rest/api/2/search?jql=project='PYT'"
    request = urllib2.Request(url)
    base64string = base64.b64encode('%s:%s' % (username, password))
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib2.urlopen(request)
    res = json.loads(result.read())
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p1n = []
    for i in res['issues']:
        try:
            if i['fields']['priority']['name'] == 'Highest':
                timeleft = i['fields']['customfield_10034']['ongoingCycle']['remainingTime']['friendly']
                if '-' in timeleft:
                    timeleft = "Breached"
                ticket_id = i['key']
                p1n.append(ticket_id)
                try:
                    org = i['fields']['customfield_10002'][0]['name']
                except Exception as e:
                    org = ''
                p1.append({'org': org, 'type': i['fields']['issuetype']['name'],
                           'ticket_id': ticket_id, 'Time Left': timeleft})
            elif i['fields']['priority']['name'] == 'Medium':
                timeleft = i['fields']['customfield_10034']['ongoingCycle']['remainingTime']['friendly']
                if '-' in timeleft:
                    timeleft = "Breached"
                ticket_id = i['key']
                try:
                    org = i['fields']['customfield_10002'][0]['name']
                except Exception as e:
                    org = ''
                p2.append({'org': org, 'type': i['fields']['issuetype']['name'],
                           'ticket_id': ticket_id, 'Time Left': timeleft})
            elif i['fields']['priority']['name'] == 'Low':
                timeleft = i['fields']['customfield_10034']['ongoingCycle']['remainingTime']['friendly']
                if '-' in timeleft:
                    timeleft = "Breached"
                ticket_id = i['key']
                try:
                    org = i['fields']['customfield_10002'][0]['name']
                except Exception as e:
                    org = ''
                p3.append({'org': org, 'type': i['fields']['issuetype']['name'],
                           'ticket_id': ticket_id, 'Time Left': timeleft})
            elif i['fields']['priority']['name'] == 'Lowest':
                timeleft = i['fields']['customfield_10034']['ongoingCycle']['remainingTime']['friendly']
                if '-' in timeleft:
                    timeleft = "Breached"
                ticket_id = i['key']
                try:
                    org = i['fields']['customfield_10002'][0]['name']
                except Exception as e:
                    org = ''
                p4.append({'org': org, 'type': i['fields']['issuetype']['name'],
                           'ticket_id': ticket_id, 'Time Left': timeleft})
        except Exception as e:
            print 'error',e
    new_p1 = list(set(p1n) - set(op1))
    response = {'tickets': [p1,p2,p3,p4],'new_p1': new_p1}
    op1 = p1n[:]
    return response

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/tickets')
def tickets():
    return jsonify(get_ticket())


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)