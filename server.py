import json
from flask import Flask, render_template, abort, request
from flask_cors import CORS
from pymongo import cursor
from mock_data import mock_data
from config import db, parse_json


app = Flask(__name__)
CORS(app)

me = {
    "name": "Yadiel",
    "last": "Diaz-Reyes",
    "email": "test@mail.com",
    "age": 27,
    "hobbies": [],
    "address": {
        "street": "main",
        "number": "42"
    }
}

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

# @app.route("/about")
# def about():
#     return f"{me['name']} {me['last']}"

@app.route("/about/email")
def get_email():
    return me["email"]

# @app.route("/about/address")
# def get_address():
#     addresss = me["address"]
#     return f"{addresss['number']} {addresss['street']}"

# API Methods
@app.route("/api/catalog", methods=["GET"])
def get_catalog():
    # read products from database and return it
    cursor = db.products.find({})#get all record/documents
    catalog = []
    for prod in cursor:
        catalog.append(prod)

    return parse_json(catalog)

@app.route("/api/catalog", methods=["POST"])
def save_product():
    product = request.get_json()
    if not "price" in product or product["price"] <= 0:
        abort(400,"Price is required and should be greater that zero")

    if not "title" in product or len(product["title"]) < 5:
        abort(400, "Title is required and should be at least 5 chars long")

    # save product into the DB
    # MongoDB add a _id with a uniqe value
    db.products.insert_one(product)
    return parse_json(product)

@app.route("/api/categories")
def get_categories():
    # return a list with the uniqe categories [string, string]

    cursor = db.products.find({})
    categories = []
    for cat in cursor:
        if cat['category'] not in categories:
            categories.append(cat['category'])
    return parse_json(categories)

@app.route("/api/product/<id>")
def get_by_id(id):
    # find the product with such id
    # return the product as json string

    product = db.products.find_one({"_id": id})

    if not product:
        abort(404)

    return parse_json(product)

@app.route("/api/catalog/<cat>")
def get_by_category(cat):
    # pymongo find case insensitive
    cursor = db.products.find({"category": cat.lower()})
    prods = []
    for prod in cursor:
        prods.append(prod)
    return parse_json(prods)

@app.route("/api/cheapest")
def get_cheapest():
    cursor = db.products.find({})
    cheapest = cursor[0]
    for prod in cursor:
        if prod["price"] < cheapest["price"]:
            cheapest = prod

    return parse_json(cheapest)


@app.route("/api/test/loadData")
def load_data():

    return "Data Already Loaded"
    #load every product in mock_data into the database
    for prod in mock_data:
        db.products.insert_one(prod)

    return "Data Loaded"



# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)

#         return json.JSONEncoder.default(self, o)


# def parse_json(data):
#     return JSONEncoder().encode(data)

@app.route("/api/couponCode", methods=["POST"])
def save_coupon():
    coupon = request.get_json()
    if not "code" in coupon:
        abort(400, "Title is required")

    if not "discount" in coupon or coupon["discount"] <= 0:
        abort(400, "Discount is required and must be more than 0")
    
    db.couponCodes.insert_one(coupon)
    return parse_json(coupon)


@app.route("/api/couponCode")
def get_coupon():
    cursor = db.couponCodes.find({})
    codes = []
    for code in cursor:
        codes.append(code)
    return parse_json(codes)














app.run(debug=True)