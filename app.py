import sqlite3
from flask import Flask, url_for, jsonify, render_template, request
app = Flask(__name__, static_folder='dist',
            static_url_path='', template_folder='dist')

DATABASE = './app_info'


@app.route('/')
def index():
    # url_for('static')
    return render_template('index.html')


@app.route('/get_rank', methods=['POST'])
def get_rank():
    # 接收使用的时间
    time_use = request.form['time']
    # 获取远方IP
    ip = request.remote_addr

    try:
        # 初始化sqlite
        sqliteDB = sqlite3.connect(DATABASE)
        # 构造SQL语句
        sql = 'select MAX(range) from flag'
        cur = sqliteDB.execute(sql)
        max_num = cur.fetchall()[0][0]

        sql = "insert into flag (ip,time,range) VALUES ('{0}','{1}','{2}')".format(
            ip, time_use, max_num+1)
        run_sql(sql)

        return jsonify({
            'status': 1,
            'range': max_num+1,
            'time': time_use
        })
    except Exception as e:
        return jsonify({
            'status': 0,
            'msg': e
        })


@app.route('/position', methods=['POST'])
def position():
    addr = request.form['addr']
    if addr == "":
        return jsonify({
            'status': 0,
            'msg': 'addr is empty'
        })
    ip = request.remote_addr

    import cpca
    df = cpca.transform([addr])
    province = ''
    try:
        province = df['省'][0]
    except Exception as e:
        return jsonify({
            'status': 0,
            'msg': e
        })

    try:
        # 初始化sqlite
        sqliteDB = sqlite3.connect(DATABASE)
        # 构造SQL语句
        sql = "INSERT INTO address (province,ip) VALUES ('{0}','{1}') ".format(
            province, ip)
        run_sql(sql)

        sql = "SELECT COUNT(*) from address where province = '{0}'".format(
            province)
        cur = sqliteDB.execute(sql)
        nums = cur.fetchall()[0][0]

        sql = "SELECT COUNT(*) from address"
        cur = sqliteDB.execute(sql)
        total = cur.fetchall()[0][0]

        return jsonify({
            'status': 1,
            'rank': nums,
            'province': province,
            'total': total
        })
    except Exception as e:
        return jsonify({
            'status': 0,
            'msg': e
        })


@app.route('/distribution', methods=['GET'])
def distribution():
    sql = "select distinct(province) from address"
    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.execute(sql)
    province = cur.fetchall()
    data = []
    for i in province:
        data.append({'province': i[0], 'num': get_num(i[0])[0][0]})
    return jsonify({'status': 1, 'data': data})


def get_num(province):
    sql = "select COUNT(*) from address where province = '{0}'".format(
        province)
    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.execute(sql)
    num = cur.fetchall()
    return num


def run_sql(sql):
    sqliteDB = sqlite3.connect(DATABASE)
    cur = sqliteDB.execute(sql)
    sqliteDB.commit()
    sqliteDB.close()
    return cur


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
