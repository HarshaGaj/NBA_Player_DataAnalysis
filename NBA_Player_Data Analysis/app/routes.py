""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/delete/<player_name>/<season_year>", methods=['POST'])
def delete(player_name, season_year):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_task_by_id(player_name, season_year)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<player_name>/<season_year>", methods=['POST'])
def update(player_name, season_year):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        db_helper.update_status_entry(player_name, season_year, data["description"])
        result = {'success': True, 'response': 'Status Updated'}
        # elif "description" in data:
        #     db_helper.update_task_entry(task_id, data["description"])
        #     result = {'success': True, 'response': 'Task Updated'}
        # else:
        #     result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    print(data)
    db_helper.insert_new_task(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/advanced_query_1/", methods=['GET'])
def advanced_query_1():
    items = db_helper.advanced_query_1()
    return render_template("advanced_query_1.html", items = items)

@app.route("/advanced_query_2/", methods=['GET'])
def advanced_query_2():
    items = db_helper.advanced_query_2()
    return render_template("advanced_query_2.html", items = items)

@app.route("/<query>", methods=['GET'])
def search(query):
    print(query)
    items = db_helper.search_season(query)
    return render_template("index.html", items = items)

@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_todo()
    return render_template("index.html", items=items)

