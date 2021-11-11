
from flask import Flask, render_template, request
from flask_mysqldb import MySQL


app = Flask (__name__)

app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'bf92da29ab98b1'
app.config['MYSQL_PASSWORD'] = '8da85e36'
app.config['MYSQL_DB'] = 'heroku_147cceb9bbe24e3'

mydb = MySQL(app)


@app.route('/')
def index():
    title = "SJUSD Tech Inventory"
    return render_template("index.html", title=title)

@app.route('/search', methods=['POST', 'GET'])
def search():
    items = ["Cable", "Hardware", "Software", "Networking"]
    return render_template("search.html", items = items)

@app.route('/update', methods=['POST', 'GET'])
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

    cur.execute("SELECT ItemNumber, ItemDescription, ItemBoxNumber, ItemCurrentStock  from items WHERE ItemNumber = %s", ([itemid]))

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



    return render_template("updateresult.html", identifier=boxid)

@app.route('/EditRow',methods=['POST'])
def EditRow():
    itemid = int(request.form.get("item_number"))
    description = (request.form.get("item_description"))
    boxid = int(request.form.get("item_boxnumber"))
    itemStock = int(request.form.get("item_stock"))

    cur = mydb.connection.cursor()
    sql1 = "UPDATE items SET ItemCurrentStock =%d WHERE ItemNumber=%d" % (itemStock, itemid)
    sql2 = "UPDATE items SET ItemDescription = %s WHERE ItemNumber=%s"
    val = (description, itemid)

    cur.execute(sql1)
    cur.execute(sql2, val)

    mydb.connection.commit()
    cur.close()

    return render_template("updateresult.html", identifier=boxid)

@app.route('/viewtable',methods=['POST', 'GET'])
def viewtable():

    cur = mydb.connection.cursor()

    cur.execute('SELECT * FROM items')

    fetchdata = cur.fetchall()
    cur.close()
    headings = ("ItemID", "Description", "CommonName", "Picture", "Type", "Vendor", "ProductNumber", "Box #", "CurrentStock", "Restock Level" ,"Reorder?")
    return render_template("viewtable.html", data=fetchdata, headings=headings)

@app.route('/addRow',methods=['POST', 'GET'])
def addRow():
    description = (request.form.get("item_description2"))
    commonName = (request.form.get("item_commonname2"))
    type = (request.form.get("item_type2"))
    vendor = (request.form.get("item_vendor2"))
    productNumber = (request.form.get("item_productnumber2"))
    boxNumber = (request.form.get("item_boxnumber2"))
    currentStock = (request.form.get("item_stock2"))
    restockLevel =(request.form.get("item_restock2"))
    reorder = (request.form.get("item_reorder2"))




    cur = mydb.connection.cursor()
    sql = """INSERT INTO items(ItemDescription,ItemCommonName,ItemCategory, ItemVendor,ItemVendorID,ItemBoxNumber,ItemCurrentStock,ItemRestockLevel,ItemReorder) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s )"""

    val=[description, commonName, type, vendor, productNumber, boxNumber, currentStock, restockLevel, reorder]

    cur.execute(sql, val)

    mydb.connection.commit()
    cur.close()

    return render_template("updateresult.html", val=val)


@app.route('/EditSqlTable', methods=['POST', 'GET'])
def EditSqlTable():
    itemid = (request.form.get('item_number'))
    description = (request.form.get("item_description"))
    commonName = (request.form.get("item_commonname"))
    type = (request.form.get("item_type"))
    vendor = (request.form.get("item_vendor"))
    productNumber = (request.form.get("item_productnumber"))
    boxNumber = (request.form.get("item_boxnumber"))
    currentStock = (request.form.get("item_stock"))
    restockLevel = (request.form.get("item_restock"))
    reorder = (request.form.get("item_reorder"))

    cur = mydb.connection.cursor()
    sql1 = "UPDATE items SET itemDescription =%s WHERE ItemNumber=%s"
    sql2 ="UPDATE items SET itemcommonName =%s WHERE ItemNumber=%s"
    sql3 = "UPDATE items SET itemCategory =%s WHERE ItemNumber=%s"
    sql4 = "UPDATE items SET itemVendor =%s WHERE ItemNumber=%s"
    sql5 = "UPDATE items SET itemVendorID =%s WHERE ItemNumber=%s"
    sql6 = "UPDATE items SET itemBoxNumber =%s WHERE ItemNumber=%s"
    sql7 = "UPDATE items SET itemCurrentStock =%s WHERE ItemNumber=%s"
    sql8 = "UPDATE items SET itemRestockLevel =%s WHERE ItemNumber=%s"
    sql9 = "UPDATE items SET itemReorder =%s WHERE ItemNumber=%s"

    val1= [description, itemid]
    val2= [commonName, itemid]
    val3 =[type, itemid]
    val4 =[vendor, itemid]
    val5 =[productNumber, itemid]
    val6 =[boxNumber, itemid]
    val7 =[currentStock, itemid]
    val8 =[restockLevel, itemid]
    val9 =[reorder, itemid]

    cur.execute(sql1, val1)
    cur.execute(sql2, val2)
    cur.execute(sql3, val3)
    cur.execute(sql4, val4)
    cur.execute(sql5, val5)
    cur.execute(sql6, val6)
    cur.execute(sql7, val7)
    cur.execute(sql8, val8)
    cur.execute(sql9, val9)

    mydb.connection.commit()
    cur.close()

    return render_template("updateresult.html", identiier=itemid)





if __name__ == '__main__':
    app.run()