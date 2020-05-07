from flask import Flask, request, jsonify
import json
from flaskext.mysql import MySQL
from flask_cors import CORS, cross_origin
import pymysql
from fuzzywuzzy import process

app = Flask(__name__)

mysql = MySQL(app)
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mysql'
app.config['MYSQL_DATABASE_DB'] = 'quran'
mysql.init_app(app)


@app.route("/hizb/<int:hizb>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def hizb(hizb):
    if ( hizb == 60 ):
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM quran WHERE id >= 5949")
        quarter = cur.fetchall()
        resp = jsonify(quarter)
        return resp
    else :
        conn1 = mysql.connect()
        cur1 = conn1.cursor(pymysql.cursors.DictCursor)
        cur1.execute("SELECT * FROM hizb WHERE id = %s",hizb*4-3)
        hizb1 = cur1.fetchone()
        conn11 = mysql.connect()
        cur11 = conn11.cursor(pymysql.cursors.DictCursor)
        cur11.execute("SELECT * FROM quran WHERE suraId = %s AND ayaId = %s",(hizb1["sura"],hizb1["aya"]))
        hizb11 = cur11.fetchone()
        deb = hizb11["id"]
        conn2 = mysql.connect()
        cur2 = conn1.cursor(pymysql.cursors.DictCursor)
        cur2.execute("SELECT * FROM hizb WHERE id = %s",hizb*4+1)
        hizb2 = cur2.fetchone()
        conn22 = mysql.connect()
        cur22 = conn11.cursor(pymysql.cursors.DictCursor)
        cur22.execute("SELECT * FROM quran WHERE suraId = %s AND ayaId = %s",(hizb2["sura"],hizb2["aya"]))
        hizb22 = cur22.fetchone()
        fin =hizb22["id"]-1
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM quran WHERE id >= %s AND id <= %s",(deb,fin))
        hizb = cur.fetchall()
        resp = jsonify(hizb)
        return resp

@app.route("/juz/<int:juzId>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def juz(juzId):
    conn0 = mysql.connect()
    cur0 = conn0.cursor(pymysql.cursors.DictCursor)
    cur0.execute("SELECT * FROM juz WHERE id = %s",juzId)
    juz = cur0.fetchone()
    deb = juz["deb"]
    fin = juz["fin"]
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM quran WHERE id >= %s AND id <= %s",(deb,fin))
    juzs = cur.fetchall()
    resp = jsonify(juzs)
    return resp

@app.route("/page/<int:page>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def page(page):
    if ( page == 604 ):
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM quran WHERE id >= 6222")
        pag = cur.fetchall()
        resp = jsonify(pag)
        return resp
    else :
        conn1 = mysql.connect()
        cur1 = conn1.cursor(pymysql.cursors.DictCursor)
        cur1.execute("SELECT * FROM page WHERE id = %s",page)
        page1 = cur1.fetchone()
        conn11 = mysql.connect()
        cur11 = conn11.cursor(pymysql.cursors.DictCursor)
        cur11.execute("SELECT * FROM quran WHERE suraId = %s AND ayaId = %s",(page1["sura"],page1["aya"]))
        page11 = cur11.fetchone()
        deb = page11["id"]
        conn2 = mysql.connect()
        cur2 = conn1.cursor(pymysql.cursors.DictCursor)
        cur2.execute("SELECT * FROM page WHERE id = %s",page+1)
        page2 = cur2.fetchone()
        conn22 = mysql.connect()
        cur22 = conn11.cursor(pymysql.cursors.DictCursor)
        cur22.execute("SELECT * FROM quran WHERE suraId = %s AND ayaId = %s",(page2["sura"],page2["aya"]))
        page22 = cur22.fetchone()
        fin = page22["id"]-1
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("SELECT * FROM quran WHERE id >= %s AND id <= %s",(deb,fin))
        pag = cur.fetchall()
        resp = jsonify(pag)
        return resp

@app.route("/sura/<int:suraId>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def sura(suraId):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM quran WHERE suraId = %s",suraId)
    quran = cur.fetchall()
    resp = jsonify(quran)
    return resp

@app.route("/aya/<int:suraId>/<int:ayaId>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def aya(suraId,ayaId):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM quran WHERE suraId = %s AND ayaId = %s",(suraId,ayaId))
    aya = cur.fetchone()
    resp = jsonify(aya)
    return resp

@app.route("/sura", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
#@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def suras():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM sura")
    sura = cur.fetchall()
    resp = jsonify(sura)
    return resp

@app.route("/1", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def search1():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM quran")
    quran = cur.fetchall()
    str = "ٱلرَّحْمَٰنِ"
    result = process.extract(str,quran,limit=7000)
    #resp = jsonify(result)
    return json.dumps(result, ensure_ascii=False)


@app.route("/2", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def search2():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM quran WHERE suraId = 1")
    quran = cur.fetchall()
    str = "ٱلرَّحْمَٰنِ"
    result = process.extract(str,quran,limit=7000)
    #resp = jsonify(result)
    return json.dumps(result, ensure_ascii=False)

@app.route("/<int:aya>", methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def index(aya):
    ss = '%' + aya + '%'
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM quran WHERE aya LIKE %s", ss)
    sura = cur.fetchall()
    #resp = jsonify(sura)
    #return resp
    return json.dumps(sura, ensure_ascii=False)

if __name__ == "__main__":
    app.run()
