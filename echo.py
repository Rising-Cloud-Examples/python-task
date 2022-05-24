import json
if __name__ == "__main__":
    with open('request.json', 'r') as req_file:
        request = json.load(req_file)
    with open('response.json', 'w+') as res_file:
        response = {}
        response['echo'] = request
        json.dump(response, res_file)
