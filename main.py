import datetime
from flask import Flask
from flask import render_template, redirect, make_response, url_for, abort
from flask import request
import db_handler

db_handler.setup()
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/adminlogin", methods=["POST"])
def adminlogin():
    if db_handler.check_admin(request.form["username"], request.form["password"]):
        resp = make_response(redirect("/inventory"))
        resp.set_cookie("username", request.form["username"])
        resp.set_cookie("type", "admin")
        return resp
    else:
        return redirect("/")


@app.route("/driverlogin", methods=["POST"])
def driverlogin():
    if db_handler.check_driver(request.form["username"], request.form["password"]):
        resp = make_response(redirect("/"))
        resp.set_cookie("username", request.form["username"])
        resp.set_cookie("type", "driver")
        return resp
    else:
        return redirect("/")


@app.route("/cylinderhist", methods=["GET"])
def cylinderhist():
    if request.cookies.get("type") != "admin":
        return abort(403)
    if request.args.get("id") == None:
        return abort(403)

    return render_template(
        "cylinderhist.html",
        cylinder_id=request.args.get("id"),
        cylinderhist=db_handler.get_cylinder_hist(int(request.args.get("id"))),
    )


@app.route("/billing")
def billing():
    if request.cookies.get("type") == "admin":
        billing_items = db_handler.get_billing_items()
        return render_template("billing.html", billing_items=billing_items)
    else:
        return abort(403)


@app.route("/inventory")
def inventory():
    if request.cookies.get("type") != "admin":
        return abort(403)

    inventory_items = db_handler.get_inventory_items()
    return render_template("inventory.html", inventory_items=inventory_items)


@app.route("/inventory_edit", methods=["GET", "POST"])
def inventory_edit():
    if request.cookies.get("type") != "admin":
        return abort(403)

    if request.method == "GET":
        if request.args.get("id") == None:
            return abort(403)

        inventory_item = db_handler.get_inventory_item(int(request.args.get("id")))
        return render_template("inventory_edit.html", inventory_item=inventory_item)
    else:
        data = dict(request.form)
        data["capacity"] = int(data["capacity"])
        data["cylinder_id"] = int(data["cylinder_id"])
        db_handler.modify_inventory_item(data)
        return redirect("/inventory")

@app.route("/inventory_new", methods=["GET", "POST"])
def inventory_new():
    if request.cookies.get("type") != "admin":
        return abort(403)

    if request.method == "GET":
        return render_template("inventory_new.html")
    else:
        data = dict(request.form)
        data["capacity"] = int(data["capacity"])
        data["cylinder_id"] = int(data["cylinder_id"])
        db_handler.insert_inventory_item(data)
        return redirect("/inventory")


@app.route("/refilling")
def refilling():
    if request.cookies.get("type") != "admin":
        return abort(403)

    refilling_items = db_handler.get_refilling_items()
    # print(refilling_items)
    return render_template("refilling.html", refilling_items=refilling_items)

@app.route("/refillcomeback", methods=["POST"])
def refillcomeback():
    if request.cookies.get("type") != "admin":
        return abort(403)

    db_handler.refill_come_back(int(request.form['id']))
    return redirect('/refilling')
    

@app.route("/customer")
def customer():
    if request.cookies.get("type") != "admin":
        return abort(403)

    customer_items = db_handler.get_customer_items()
    return render_template("customer.html", customer_items=customer_items)

@app.route("/customercomeback", methods=["POST"])
def customercomeback():
    if request.cookies.get("type") != "admin":
        return abort(403)

    db_handler.customer_come_back(int(request.form['id']))
    return redirect('/customer')

@app.route("/challan")
def challan():
    if request.cookies.get("type") != "admin":
        return abort(403)

    challan_items = db_handler.get_challan_items()
    return render_template("challan.html", challan_items=challan_items)


@app.route("/challan_cylinder")
def challan_cylinder():
    if request.cookies.get("type") != "admin":
        return abort(403)

    if request.args.get("id") == None:
        return abort(403)

    challan_id = int(request.args.get("id"))
    challan_cylinder_items = db_handler.get_challan_cylinder_items(challan_id)
    # print(challan_cylinder_items)
    return render_template(
        "challan_cylinder.html",
        challan_id=challan_id,
        challan_cylinder_items=challan_cylinder_items,
    )


@app.route("/challan_empty", methods=["GET", "POST"])
def challan_empty():
    if request.cookies.get("type") != "admin":
        return abort(403)

    if request.method == "GET":
        cylinder_ids = db_handler.get_empty_cylinder_ids()
        return render_template("challan_empty.html", cylinder_ids=cylinder_ids)
    else:
        data = dict(request.form)
        data["cylinder_id"] = list(map(int, request.form.getlist("cylinder_id")))
        data["challan_id"] = int(data["challan_id"])
        data["challan_date"] = datetime.datetime.now()
        db_handler.new_empty_challan(data)
        return redirect("/challan")


@app.route("/challan_full", methods=["GET", "POST"])
def challan_full():
    if request.cookies.get("type") != "admin":
        return abort(403)

    if request.method == "GET":
        cylinder_ids = db_handler.get_full_cylinder_ids()
        return render_template("challan_full.html", cylinder_ids=cylinder_ids)
    else:
        data = dict(request.form)
        data["cylinder_id"] = list(map(int, request.form.getlist("cylinder_id")))
        data["challan_id"] = int(data["challan_id"])
        data["challan_date"] = datetime.datetime.now()
        data["total_cost"] = int(data["total_cost"])
        data["total_tax"] = int(data["total_tax"])
        db_handler.new_full_challan(data)
        return redirect("/challan")

@app.route("/challan_billing", methods=["GET"])
def challan_billing():
    if request.cookies.get("type") != "admin":
        return abort(403)

    if request.args.get("id") == None:
        return abort(403)

    billing_item = db_handler.get_billing_item(request.args.get("id"))
    print(billing_item)
    return render_template("challan_billing.html", billing_item=billing_item)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
