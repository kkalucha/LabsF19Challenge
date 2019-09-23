from flask import Flask, render_template, request
import requests
import collections
import operator
import itertools

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/information/<int:query>')
def show_min(query):
    # data = {'butler': 34, 'lerner': 44, 'low': 12, 'law': 65, 'avery': 4, 'milstein': 0}
    building_nums = [125, 126, 127, 116, 117, 118, 119, 120, 121, 122, 98, 192, 155, 110, 111, 102, 103, 104, 105, 106, 107, 100, 96]
    #building_nums = [125, 126, 127]
    auth = request.args.get('auth', '')
    data = {}
    for nums in building_nums:
        payload = {'auth_token':auth}
        density_request = requests.get('https://density.adicu.com/latest/group/' + str(nums), params = payload).json()
        name = density_request['data'][0]['group_name']
        percent = density_request['data'][0]['percent_full']
        data.update({name:percent})
    sorted_dict = collections.OrderedDict(sorted(data.items(), key=operator.itemgetter(1)))
    truncated = collections.OrderedDict(itertools.islice(sorted_dict.items(), query))
    return render_template('min.html', number = query, buildings = truncated)

@app.route('/information/<string:query>')
def show_building(query):
    building_nums = {'avery':124, 'butler':115, 'east_asian_library':97, 'john_jay':153, 'lehman_library':109, 'lerner':101, 'northwest_corner_building':99, 'uris':2}
    auth = request.args.get('auth', '')
    payload = {'auth_token':auth}
    density_request = requests.get('https://density.adicu.com/latest/building/' + str(building_nums[query.lower()]), params = payload).json()
    building = density_request['data'][0]['building_name']
    data = {}
    for routers in density_request['data']:
        name = routers['group_name']
        percent = routers['percent_full']
        data.update({name:percent})
    sorted_dict = collections.OrderedDict(sorted(data.items(), key=operator.itemgetter(0)))
    return render_template('building.html', building = building, routers = sorted_dict)
    
@app.route('/testing/<string:name>')
def test(name):
    data = ['jane', 'alex', 'joe', 'max']
    return render_template('testing.html', name = name, users = data)

if __name__ == '__main__':
    app.run()
