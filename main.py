from flask import Flask, jsonify, request
from modules.googleNews import GoogleNews
from modules.googleVideo import GoogleVideo
from modules.googleSearch import GoogleSearch
from modules.knowledge_graph_search import KnowledgeGraphSearch
from modules.google_db import Google_db
from modules.google_contacts import GoogleContacts
from raven.contrib.flask import Sentry

app = Flask(__name__)
sentry = Sentry(app)


# @app.route('/api/v1/search/<string:query>/<int:count>')
@app.route('/api/v1/search')
def google_search():
    query = request.args.get('q')
    limit = request.args.get('limit')
    obj4 = GoogleSearch()
    result = obj4.get(query)
    return jsonify({'data': result})


# @app.route('/api/v1/search/news/<string:query>/<int:count>')
@app.route('/api/v1/search/news')
def google_news():
    query = request.args.get('q')
    limit = request.args.get('limit')
    obj1 = GoogleNews()
    result = obj1.get(query)
    return jsonify({'data': result})


# @app.route('/api/v1/search/video/<string:query>/<int:count>')
@app.route('/api/v1/search/video')
def google_video():
    query = request.args.get('q')
    limit = request.args.get('limit')
    obj2 = GoogleVideo()
    result = obj2.get(query)
    return jsonify({'data': result})


@app.route('/api/v1/search/knowledge-graph')
def google_knowledge_graph():
    obj3 = KnowledgeGraphSearch()
    query = request.args.get('q')
    limit = request.args.get('limit')
    result = obj3.knowledge_search(query, limit)
    return jsonify(result)

# @app.route('/api/v1/search/id')
# def emailChecker():
#     email = request.args.get('q')
#     obj = EmailChecker()
#     data = obj.checker(email)
#     return jsonify({'result': data})


@app.route('/api/v1/search/id')
def email_checker():
    email = request.args.get('q')
    obj2 = Google_db()
    data_db = obj2.db_check(email)
    # print(data_db)
    # obj = EmailChecker()
    # data = obj.checker(email)
    # obj2.data_loader(data)
    try:
        # return jsonify({'result': data_db})
        return jsonify({'data': {"availability": data_db['email']}})

    except TypeError:
        data = dict()
        data['name'] = data_db['name']
        data['email'] = data_db['email']
        data['image'] = data_db['image']
        data['googlePlusId'] = data_db['googlePlusId']
        data['email_id'] = data_db['email_id']
        # return jsonify({'result': data})
        return jsonify({'data': {"availability": data['email']}})


@app.route('/api/v1/google_contacts', methods=['POST', 'GET'])
def google_():
    global request_data
    if request.method == 'POST':
        request_data = request.get_json()
        # numbers = request_data['number_list']

    obj = GoogleContacts()
    res = obj.checker(request_data)
    return jsonify({"data": res})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5018)

