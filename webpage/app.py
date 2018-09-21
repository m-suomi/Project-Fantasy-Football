import os

import pandas as pd
import numpy as np
import json
from scipy import stats
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)



app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../data/fantasy_football_2018.db"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
week1_ppr_projections = Base.classes.week1_ppr_projections
# Samples = Base.classes.table2_name



@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")



# Josh
@app.route("/data")
def data():
    # """Return a table on ufo template"""
    #get week 1 projections
    stmt = """
    SELECT *
    FROM week2_ppr_projections
    """

    # stmt = db.session.query(week1_ppr_projections).statement

    df_week1_ppr_projections = pd.read_sql_query(stmt, db.session.bind)
    print(df_week1_ppr_projections.head())
    return render_template("data.html")




# Connor
@app.route("/tweet")
def tweet():
    # """Return a table on ufo template"""
    #get week 1 projections
    stmt = """
    SELECT *
    FROM week2_ppr_projections
    """

    # stmt = db.session.query(week1_ppr_projections).statement

    df_week1_ppr_projections = pd.read_sql_query(stmt, db.session.bind)
    print(df_week1_ppr_projections.head())
    return render_template("tweet.html")





# Mike
@app.route("/input", methods=['POST', 'GET'])
def input():
    if request.method == "GET":
        # Return an initial blank form before user inputs their custom factors
        return render_template("input.html")
        
    elif request.method == "POST":
        # use the user input to operate on the dataframe and then a list of dictionaries (records) that can be referenced in the html
        
        #return jsonify(request.form)
        scout = request.form.get('')

        #call database test
        stmt = """
            SELECT *
            FROM week3_ppr_projections
            """
        df_proj = pd.read_sql_query(stmt, db.session.bind)

        #send dataframe to records (a list of dictionaries for each row)
        userTableData = df_proj.to_dict('records')
        return render_template("input.html", tableData=userTableData)




# @app.route("/input/test") #?Week=<week>&ESPN=<espn_wt>&CBS=<cbs_wt>&Sharks=<sharks_wt>&Scout=<scout_wt>&Prior=<prior_wt>&Defense=<def_boost>&OverUnder=<overunder_boost>&Twitter=<twitter_boost>&message=<msg_text>")
# def calculate_custom_factors():
#     #get current week projections
#     stmt = """
#     SELECT *
#     FROM week3_ppr_projections
#     """
#     df_proj = pd.read_sql_query(stmt, db.session.bind)


#     #export df as json - orient='records' gives a json string that is a list of dictionaries, 
#     # one dictionary for each row in df with column as keys and row values as values
#     #also need to use python's json.loads function to create it to a real json and not string object
#     json_proj = json.loads(df_proj.to_json(orient='records'))

#     print(json_proj)
#     print(type(json_proj))
#     return render_template("input.html", jsonUser=jsonify(json_proj))



# Zach
@app.route("/compare/<week>", methods=['POST', 'GET'])
def getCharts(week):
    #get week 1 projections & actuals
    stmt = "SELECT * FROM week{}_ppr_projections".format(week)
    df_ppr_projections = pd.read_sql_query(stmt, db.session.bind)

    stmt = "SELECT * FROM week{}_ppr_actuals".format(week)
    df_ppr_actuals = pd.read_sql_query(stmt, db.session.bind)

    #merge starting with the actuals db and merge inner (don't want to evaluate correlations of players not in db)
    df_week1_ppr = pd.merge(df_ppr_actuals, df_ppr_projections[['PLAYER', 'POS',
                                                'FPTS_PPR_ESPN', 'FPTS_PPR_CBS', 'FPTS_PPR_SHARKS',
                                                'FPTS_PPR_SCOUT', 'FPTS_PPR_PRVS_WK_ACTUAL']],
                        how='inner', on=['PLAYER', 'POS'])

    #average all four of our projection sources of ESPN, CBS, Sharks, and Scout
    df_week1_ppr['FPTS_PPR_AVG_PROJ'] = df_week1_ppr[['FPTS_PPR_ESPN','FPTS_PPR_CBS',
                                                  'FPTS_PPR_SHARKS', 'FPTS_PPR_SCOUT']].mean(axis='columns')
    json_ppr_proj = df_week1_ppr.to_dict('records')
    return jsonify(json_ppr_proj)



# @app.route("/compare/<week>", methods=['POST', 'GET'])
# def getCharts(week):
#     #get week 1 projections
#     stmt = "SELECT * FROM week{}_ppr_projections".format(week)

#     df_ppr_projections = pd.read_sql_query(stmt, db.session.bind)
#     json_proj = df_ppr_projections.to_dict('records')
#     return jsonify(json_proj)



@app.route("/compare", methods=['POST', 'GET'])
def compare():
    if request.method == "GET":
        # Return an initial blank form before user inputs their custom factors
        stmt = """
            SELECT *
            FROM week3_ppr_projections
            """
        df_proj = pd.read_sql_query(stmt, db.session.bind)

        #send dataframe to records (a list of dictionaries for each row)
        initialTableData = df_proj.to_dict('records')
        return render_template("compare.html", tableData=initialTableData)
        
    elif request.method == "POST":
        # use the user input to operate on the dataframe and then a list of dictionaries (records) that can be referenced in the html
        
        #return jsonify(request.form)
        scout = request.form.get('')

        #call database test
        stmt = """
            SELECT *
            FROM week3_ppr_projections
            """
        df_proj = pd.read_sql_query(stmt, db.session.bind)

        #send dataframe to records (a list of dictionaries for each row)
        userTableData = df_proj.to_dict('records')
        return render_template("compare.html", tableData=userTableData)



if __name__ == '__main__':
   app.run(debug = True)




# from flask import Flask, render_template, request
# import sqlite3 as sql
# app = Flask(__name__)


# @app.route('/')
# def home():
#    return render_template('home.html')

# @app.route('/list')
# def list():
#    con = sql.connect("my_lite_store.db")
#    con.row_factory = sql.Row
   
#    cur = con.cursor()
#    cur.execute("select * from actual_ppr")
   
#    rows = cur.fetchall()
#    return render_template("list.html",rows = rows)

# if __name__ == '__main__':
#    app.run(debug = True)


