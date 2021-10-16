
from flask import Flask, render_template, request
from flask_mysqldb import MySQL


app = Flask (__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'inventory'
app.config['MYSQL_PASSWORD'] = 'Printers!'
app.config['MYSQL_DB'] = 'test2'

mydb = MySQL(app)


@app.route('/')
def index():
    title = "SJUSD Tech Inventory"
    return render_template("index.html", title=title)

@app.route('/search', methods=['POST'])
def search():
    items = ["Cable", "Hardware", "Software", "Networking"]
    return render_template("search.html", items = items)

@app.route('/update', methods=['POST'])
def update():
    return render_template("update.html")


@app.route('/searchbyitemnumber', methods=['POST'])
def searchbyitemnumber():
    return render_template("searchbyitemnumber.html")


@app.route('/searchbydescription', methods=['POST'])
def searchbydescription():
    return render_template("searchbydescription.html")

@app.route('/searchresultitems', methods=['POST'])
def searchresultitems():
    itemid = request.form.get("item_number")
    itemidcheck = 0
    itemidcheck = int(itemid)
    cur = mydb.connection.cursor()

    cur.execute("SELECT ItemNumber, ItemDescription, ItemBoxNumber, ItemCurrentStock  from items WHERE ItemNumber = %s", itemid)

    fetchdata = cur.fetchall()
    cur.close()
    headings = ("ItemID", "Description", "Box#", "CurrentStock")
    return render_template("searchresult.html", itemid=itemid, data=fetchdata, headings=headings)

@app.route('/searchresultdescription', methods=['POST'] )
def searchresultdescription():
    description = request.form.get("item_Description")
    cur = mydb.connection.cursor()

    sql = f"""SELECT ItemNumber, ItemDescription, ItemBoxNumber, ItemCurrentStock  from items WHERE ItemDescription LIKE '%{description}%'"""
    cur.execute(sql)

    fetchdata = cur.fetchall()
    cur.close()
    headings = ("ItemID", "Description", "Box#", "CurrentStock")
    return render_template("searchresult.html",  data=fetchdata, headings=headings)

@app.route('/updatebyitem', methods=['POST'])
def updatebyitem():
    return render_template("updatebyitem.html")


@app.route('/updatebybox', methods=['POST'])
def updatebybox():
    return render_template("updatebybox.html")

@app.route('/updateresultitems', methods=['post'])
def updatebyitems():
    itemid = int(request.form.get("item_number"))
    update = request.form.get("update")

    updatemultiplier = 0
    if update == "increase":
        updatemultiplier = 1
    else:
        updatemultiplier = -1

    quantity = int(request.form.get("quantity"))
    myupdate = quantity*updatemultiplier
    cur = mydb.connection.cursor()

    sql = "UPDATE items SET ItemCurrentStock = ItemCurrentStock + %d WHERE ItemNumber=%d" % (myupdate, itemid)
    cur.execute(sql)
    mydb.connection.commit()
    cur.close()

    return render_template("updateresult.html", identifier=itemid, myupdate=myupdate)

@app.route('/updateresultbybox', methods=['post'])
def updateresultbybox():
    boxid = int(request.form.get("box_number"))
    update = request.form.get("update")

    updatemultiplier = 0
    if update == "increase":
        updatemultiplier = 1
    else:
        updatemultiplier = -1

    quantity = int(request.form.get("quantity"))
    myupdate = quantity*updatemultiplier
    cur = mydb.connection.cursor()

    sql = "UPDATE items SET ItemCurrentStock = ItemCurrentStock + %d WHERE ItemBoxNumber=%d" % (myupdate, boxid)
    cur.execute(sql)
    mydb.connection.commit()
    cur.close()



    return render_template("updateresult.html", identifier=boxid, myupdate=myupdate)



if __name__ == '__main__':
    app.run()