from flask import Flask, render_template, request
import requests
import collections
import operator
import itertools

app = Flask(__name__)


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

#returns n least crowded buildings
@app.route('/information/<int:query>')
def show_min(query):
    #all building codes
    building_nums = [125, 126, 127, 116, 117, 118, 119, 120, 121, 122, 98, 192, 155, 110, 111, 102, 103, 104, 105, 106, 107, 100, 96]
    #auth token is received as argument in query URL
    auth = request.args.get('auth', '')
    data = {}
    for nums in building_nums:
        #separate payload to make updates based on changes to density API easier
        payload = {'auth_token':auth}
        #density API response unpacked as json
        density_request = requests.get('https://density.adicu.com/latest/group/' + str(nums), params = payload).json()
        name = density_request['data'][0]['group_name']
        percent = density_request['data'][0]['percent_full']
        #parsed values are stored as key, value pairs in a dictionary
        data.update({name:percent})
    #sort dictionary by percentage full and truncate based on user query
    sorted_dict = collections.OrderedDict(sorted(data.items(), key=operator.itemgetter(1)))
    truncated = collections.OrderedDict(itertools.islice(sorted_dict.items(), query))
    #render html template and display to user
    return render_template('min.html', number = query, buildings = truncated)

#returns how busy given building is    
@app.route('/information/<string:query>')
def show_building(query):
    #this dict maps from building name to building code
    building_nums = {'avery':124, 'butler':115, 'east_asian_library':97, 'john_jay':153, 'lehman_library':109, 'lerner':101, 'northwest_corner_building':99, 'uris':2}
    auth = request.args.get('auth', '')
    payload = {'auth_token':auth}
    #query is lowercase to avoid given malicious test case
    density_request = requests.get('https://density.adicu.com/latest/building/' + str(building_nums[query.lower()]), params = payload).json()
    #well-formatted building name for render is stripped from the first item returned by density API query
    building = density_request['data'][0]['building_name']
    data = {}
    #iterate through all routers in density API response and store in a dictionary
    for routers in density_request['data']:
        name = routers['group_name']
        percent = routers['percent_full']
        data.update({name:percent})
    #sort dictionary alphabetically    
    sorted_dict = collections.OrderedDict(sorted(data.items(), key=operator.itemgetter(0)))
    #render html template and display to user
    return render_template('building.html', building = building, routers = sorted_dict)

if __name__ == '__main__':
    app.run()
