"""Defines all the functions related to the database"""
from app import db


def fetch_todo() -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from Seasons").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "season": result[0],
            "player_name": result[1],
            "games_played": result[2],
            "age": result[3]

        }
        todo_list.append(item)

    return todo_list


def update_task_entry(task_id: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update tasks set task = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


def update_status_entry(player_name: str, season_year: str, query_add: str) -> None:
    """Updates task status based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update Seasons set {} where player_name="{}" and season="{}";'.format(
        query_add, player_name, season_year)
    conn.execute(query)
    conn.close()


def search_season(query_add: str) -> None:
    """Updates task status based on given task_id

    Args:
        task_id (int): Targeted task_id
        text (str): Updated status

    Returns:
        None
    """

    "SELECT fileid"

    
    sql_query = """SELECT * FROM Seasons
    WHERE player_name LIKE %s"""
    search_val = f'%{query_add}%'
    conn = db.connect()
    # query_results = conn.execute("Select * from Seasons WHERE player_name LIKE %%'{}'%%".format(query_add)).fetchall()
    query_results = conn.execute(sql_query, (search_val))
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "season": result[0],
            "player_name": result[1],
            "games_played": result[2],
            "age":result[3]

        }
        todo_list.append(item)
    return todo_list


def insert_new_task(text: str) -> int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """
    conn = db.connect()
    query = 'Insert Into Seasons (season, player_name, gp, age) VALUES ({});'.format(
        text)
    conn.execute(query)
    query_results = conn.execute("Select LAST_INSERT_ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_task_by_id(player_name: str, season_year: str) -> None:
    print(season_year, season_year)
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From Seasons where player_name="{}" AND season="{}";'.format(
        player_name, season_year)
    conn.execute(query)
    conn.close()


def advanced_query_1() -> dict:
    conn = db.connect()
    query = """SELECT ss.player_name as player_name, Round(SUM(ss.pts*s.gp),0) as total_pts, Round(SUM(ss.reb*s.gp),0) as total_reb,Round(SUM(ss.ast*s.gp),0) as total_ast 
            FROM Season_Statistics as ss JOIN Seasons as s ON (ss.season LIKE s.season and ss.player_name LIKE s.player_name) 
            GROUP BY ss.player_name
            ORDER BY ss.player_name;"""
    query_results = conn.execute(query).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "season": result[0],
            "player_name": result[1],
            "games_played": result[2],
            "age": result[3]

        }
        todo_list.append(item)
    print(todo_list)
    return todo_list


def advanced_query_2() -> dict:
    conn = db.connect()
    query = """SELECT sub_query.player_name
    FROM (SELECT ss.player_name as player_name, Round(SUM(ss.pts*s.gp),0) as total_pts, Round(SUM(ss.reb*s.gp),0) as total_reb,Round(SUM(ss.ast*s.gp),0) as total_ast
    FROM Season_Statistics as ss JOIN Seasons as s ON (ss.season LIKE s.season and ss.player_name LIKE s.player_name)
    GROUP BY ss.player_name) sub_query
    WHERE (sub_query.total_pts > 18000 AND sub_query.total_reb > 4000 AND sub_query.total_ast > 4000) OR (sub_query.total_ast > 10000) OR (sub_query.total_reb > 10000)

    UNION 

    SELECT sub_query.player_name
    FROM (SELECT ss.player_name as player_name, Round(AVG(ss.pts),0) as avg_pts, Round(AVG(ss.reb),0) as avg_rebs ,Round(AVG(ss.ast),0) as avg_ast
    FROM Season_Statistics as ss JOIN Seasons as s ON (ss.season LIKE s.season and ss.player_name LIKE s.player_name)
    GROUP BY ss.player_name) sub_query
    WHERE (sub_query.avg_pts > 25 AND sub_query.avg_rebs > 4 AND sub_query.avg_ast > 4) OR (sub_query.avg_rebs > 12) OR (sub_query.avg_pts > 24.5) OR (sub_query.avg_ast > 10)
    ORDER BY player_name"""
    query_results = conn.execute(query).fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        item = {
            "player_name": result[0],
        }
        todo_list.append(item)
    print(todo_list)
    return todo_list
