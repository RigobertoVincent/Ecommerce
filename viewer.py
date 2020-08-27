import sys

import psycopg2
from flask import Flask, jsonify, request, abort, json, render_template, url_for, redirect
from config import config
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def home():
    return render_template("login.html")


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/', methods=['POST'])
def users():
    if request.method == 'POST':
        if request.is_json:
            content = request.json
        else:
            content = request.form
            print(content, file=sys.stdout)

        fn = content["FirstName"]
        ln = content["LastName"]
        email = content["Email"]
        ph = content["Password"]  # should be the HASH of content["password"]

        # return "got here "  fn + ln + email + ph

        query = (
                "INSERT INTO public.\"User\" (" + "\"FirstName\"," + "\"LastName\"," + "\"EmailAddress\"," + "\"Password\"" + ") VALUES(%s,%s,%s,%s)"
        )
        to_filter = [fn, ln, email, ph]

        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        # print ('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query, to_filter)
        conn.commit()

        return render_template("cust_merch.html")


@app.route("/cust_merch", methods=['GET'])
def customer():
    return render_template("customer_view.html")


@app.route("/merchant", methods=['GET'])
def merchant():
    return render_template("merchant.html")


# if request.method == 'GET':
#        # read connection parameters
#        params = config()
#
#        # connect to the PostgreSQL server
#        # print ('Connecting to the PostgreSQL database...')
#        conn = psycopg2.connect(**params)
#
#        cur = conn.cursor(cursor_factory=RealDictCursor)
#        cur.execute("SELECT "\"email"\", "\"password"\" FROM "\"User"\" ")
#        # print("The number of regular users: ", cur.rowcount)
#        rows = cur.fetchall()
#        conn.commit()
#
#        if not rows or len(rows) == 0:
#            return not_found()
#
#        return jsonify(rows)



if __name__ == '__main__':
    app.run()
