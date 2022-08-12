import collections
import sys
import psycopg2
from flask import Flask, request
import json
import phonenumbers
import re

app = Flask(__name__)


def check_email(email):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, email):
        return True
    return False


def check_mobile(mobile):
    my_number = phonenumbers.parse(mobile)
    return phonenumbers.is_possible_number(my_number)


def get_db_connection():
    conn = psycopg2.connect(host='127.0.0.1',
                            database='user_management',
                            user='postgres',
                            password='root')
    return conn


@app.route('/users')
def users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT Users.*,Address.* FROM Users INNER JOIN Address on Users.user_id=Address.u_id")
    users = cur.fetchall()
    objects_list = []
    for row in users:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['name'] = row[1]
        d['email'] = row[2]
        d['password'] = row[3]
        d['pic_url'] = row[4]
        d['mobile'] = row[5]
        d['house_no'] = row[6]
        d['address_line_1'] = row[7]
        d['address_line_2'] = row[8]
        d['city'] = row[9]
        d['stat'] = row[10]
        d['pin_code'] = row[11]
        objects_list.append(d)

    cur.close()
    conn.close()
    res = {"data": objects_list, "result": "success",  "status": 200}
    return json.dumps(res)


@app.route('/users/register', methods=['POST'])
def process_json1():
    data = request.form

    if "name" in data:
        name = data["name"]
    else:
        return {"result": "Name is required", "status": 200}

    if "email" in data:
        email = data["email"]
        if not check_email(email):
            return {"result": "email is not valid", "status": 200}
    else:
        return {"result": "email is required", "status": 200}

    if "password" in data:
        password = data["password"]
    else:
        return {"result": "password is required", "status": 200}

    if "pic_url" in data:
        pic_url = data["pic_url"]
    else:
        return {"result": "pic_url is required", "status": 200}

    if "mobile" in data:
        mobile = data["mobile"]
        if not check_mobile(mobile):
            return {"result": "mobile is not valid", "status": 200}
    else:
        return {"result": "mobile is required", "status": 200}

    # address

    if "house_no" in data:
        house_no = data["house_no"]
    else:
        return {"result": "house_no is required", "status": 200}

    if "address_line1" in data:
        address_line1 = data["address_line1"]
    else:
        address_line1 = "#"

    if "address_line2" in data:
        address_line2 = data["address_line2"]
    else:
        address_line2 = "#"

    if "stat" in data:
        stat = data["stat"]
    else:
        return {"result": "state is required", "status": 200}

    if "city" in data:
        city = data["city"]
    else:
        return {"result": "city is required", "status": 200}

    if "pin_code" in data:
        pin_code = data["pin_code"]
    else:
        return {"result": "pin_code is required", "status": 200}

    try:
        conn = get_db_connection()
        # return 'done'
        cur = conn.cursor()
        q1 = "INSERT INTO users (name, email, password, pic_url, mobile) VALUES " \
             "('" + name + "', '" + email + "', '" + password + "', '" + pic_url + "', '" + mobile + "') RETURNING user_id"

        cur.execute(q1)
        data = cur.fetchone()
        uuid = str(data[0])
        # users = cur.fetchall()

        q2 = "INSERT INTO Address (u_id,house_no, address_line_1, address_line_2, city, stat,pin_code)" \
             "VALUES (" + uuid + ", '" + house_no + "', '" + address_line1 + "', '" + address_line2 + "', '" + city + "','" + stat + "','" + pin_code + "')"

        cur.execute(q2)

        conn.commit()
        cur.close()
        conn.close()
        res = {"id": uuid, "result": "User added successfully", "status": 200}

        return json.dumps(res)
    except Exception as e:
        return {"result": e, "status": 400}


# if __name__ == '__main__':
# app.run(host="localhost", port=8000, debug=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = sys.argv[1]
        app.run(port=port)
