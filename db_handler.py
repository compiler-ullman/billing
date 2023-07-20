import sqlite3
import datetime


def connect_db():
    con = sqlite3.connect(
        "database.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    cur = con.cursor()

    return (con, cur)


def setup():
    con, cur = connect_db()

    cur.execute("DROP TABLE IF EXISTS admins")
    cur.execute("DROP TABLE IF EXISTS cylinder_info")
    cur.execute("DROP TABLE IF EXISTS cylinder_hist")
    cur.execute("DROP TABLE IF EXISTS billing")
    cur.execute("DROP TABLE IF EXISTS inventory")
    cur.execute("DROP TABLE IF EXISTS challan")
    cur.execute("DROP TABLE IF EXISTS challan_cylinder")

    cur.execute(
        "CREATE TABLE admins ( \
            username VARCHAR(255) PRIMARY KEY, \
            password VARCHAR(255))"
    )

    cur.execute(
        "CREATE TABLE cylinder_info ( \
            cylinder_id INT PRIMARY KEY, \
            cylinder_type VARCHAR(255), \
            capacity INT, \
            manufacturer VARCHAR(255), \
            current_condition VARCHAR(255))"
    )

    cylinder_info_data = [
        (1, "Type A", 10, "Manufacturer X", "Empty"),
        (2, "Type B", 15, "Manufacturer Y", "Empty"),
        (3, "Type C", 20, "Manufacturer Z", "Full"),
        (4, "Type A", 12, "Manufacturer X", "Full"),
        (5, "Type B", 18, "Manufacturer Y", "Full"),
        (6, "Type C", 22, "Manufacturer Z", "Full"),
        (7, "Type A", 14, "Manufacturer X", "Full"),
        (8, "Type B", 20, "Manufacturer Y", "Full"),
        (9, "Type C", 25, "Manufacturer Z", "Full"),
    ]

    cur.executemany(
        "INSERT INTO cylinder_info VALUES(?, ?, ?, ?, ?)",
        cylinder_info_data,
    )

    # place 0 = with us
    #       1 = refilling
    #       2 = customer
    cur.execute(
        "CREATE TABLE cylinder_hist ( \
            cylinder_id INT, \
            place INT, \
            refilling VARCHAR(255), \
            customer VARCHAR(255), \
            hist_datetime TIMESTAMP, \
            FOREIGN KEY (cylinder_id) REFERENCES cylinder_info(cylinder_id))"
    )

    cylinder_hist_data = [
        (1, 0, None, None, datetime.datetime(2011, 11, 4, 12, 12, 13)),
        (1, 1, "Refilling Station 1", None, datetime.datetime(2011, 11, 5, 12, 12, 13)),
        (1, 0, None, None, datetime.datetime(2011, 11, 6, 12, 12, 13)),
        (1, 2, None, "Customer 1", datetime.datetime(2011, 11, 7, 12, 12, 13)),
        (1, 0, None, None, datetime.datetime(2011, 11, 8, 12, 12, 13)),
        (2, 0, None, None, datetime.datetime(2011, 11, 4, 12, 12, 13)),
        (2, 1, "Refilling Station 1", None, datetime.datetime(2011, 11, 5, 12, 12, 13)),
        (2, 0, None, None, datetime.datetime(2011, 11, 6, 12, 12, 13)),
        (2, 2, None, "Customer 1", datetime.datetime(2011, 11, 7, 12, 12, 13)),
        (2, 0, None, None, datetime.datetime(2011, 11, 8, 12, 12, 13)),
        (3, 0, None, None, datetime.datetime(2011, 11, 4, 12, 12, 13)),
        (3, 1, "Refilling Station 1", None, datetime.datetime(2011, 11, 5, 12, 12, 13)),
        (4, 0, None, None, datetime.datetime(2011, 11, 4, 12, 12, 13)),
        (4, 1, "Refilling Station 1", None, datetime.datetime(2011, 11, 5, 12, 12, 13)),
        (5, 0, None, None, datetime.datetime(2011, 11, 4, 12, 12, 13)),
        (5, 2, None, "Customer 1", datetime.datetime(2011, 11, 5, 12, 12, 13)),
        (6, 0, None, None, datetime.datetime(2011, 11, 4, 12, 12, 13)),
        (6, 2, None, "Customer 1", datetime.datetime(2011, 11, 5, 12, 12, 13)),
        (7, 0, None, None, datetime.datetime(2011, 11, 4, 12, 12, 13)),
        (8, 0, None, None, datetime.datetime(2011, 11, 4, 12, 12, 13)),
        (9, 0, None, None, datetime.datetime(2011, 11, 4, 12, 12, 13)),
    ]

    cur.executemany(
        "INSERT INTO cylinder_hist VALUES(?, ?, ?, ?, ?)",
        cylinder_hist_data,
    )

    # challan_type = 0 empty (to refilling)
    #              = 1 full (to customer)
    cur.execute(
        "CREATE TABLE challan ( \
        challan_id INTEGER PRIMARY KEY, \
        challan_date TIMESTAMP, \
        challan_type INTEGER, \
        challan_where VARCHAR(255), \
        vehicle VARCHAR(255) \
    )"
    )

    challan_data = [
        (
            1,
            datetime.datetime(2011, 11, 5, 12, 12, 13),
            0,
            "Refilling Station 1",
            "MH19P8488",
        ),
        (2, datetime.datetime(2011, 11, 7, 12, 12, 13), 1, "Customer 1", "MH19P8488"),
        (
            3,
            datetime.datetime(2011, 11, 5, 12, 12, 13),
            0,
            "Refilling Station 1",
            "MH19P8488",
        ),
        (4, datetime.datetime(2011, 11, 5, 12, 12, 13), 1, "Customer 1", "MH19P8488"),
    ]

    cur.executemany(
        "INSERT INTO challan VALUES(?, ?, ?, ?, ?)",
        challan_data,
    )

    cur.execute(
        "CREATE TABLE challan_cylinder ( \
        challan_id INT, \
        cylinder_id INT, \
        FOREIGN KEY (challan_id) REFERENCES challan(challan_id), \
        FOREIGN KEY (cylinder_id) REFERENCES cylinder_info(cylinder_id) \
    )"
    )

    challan_cylinder_data = [
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
        (3, 3),
        (3, 4),
        (4, 5),
        (4, 6),
    ]

    cur.executemany(
        "INSERT INTO challan_cylinder VALUES(?, ?)",
        challan_cylinder_data,
    )

    cur.execute(
        "CREATE TABLE billing ( \
            challan_id INTEGER, \
            total_cost INTEGER, \
            total_tax INTEGER, \
            FOREIGN KEY (challan_id) REFERENCES challan(challan_id))"
    )

    billing_data = [
        (1, 100, 100),
        (2, 100, 100),
        (3, 100, 100),
        (4, 100, 100),
    ]
    cur.executemany("INSERT INTO billing VALUES (?, ?, ?)", billing_data)

    cur.execute("INSERT INTO admins VALUES(?, ?)", ("admin1", "admin123"))

    con.commit()

    res = cur.execute("SELECT * FROM sqlite_master")
    # print(*res.fetchall(), sep='\n')


def check_admin(username, password):
    con, cur = connect_db()
    cur.execute(
        "SELECT * FROM admins WHERE username = ? AND password = ?", (username, password)
    )
    if cur.fetchone() == None:
        return False
    else:
        return True


def check_driver(username, password):
    con, cur = connect_db()
    cur.execute(
        "SELECT * FROM drivers WHERE username = ? AND password = ?",
        (username, password),
    )
    if cur.fetchone() == None:
        return False
    else:
        return True


def get_cylinder_hist(cylinder_id):
    con, cur = connect_db()
    cur.execute(
        "SELECT * FROM cylinder_hist WHERE cylinder_id = ? ORDER BY hist_datetime DESC",
        (cylinder_id,),
    )
    x = cur.fetchall()
    # print(x)
    return x


def get_cylinder_where_now(cylinder_id):
    con, cur = connect_db()
    cur.execute(
        "SELECT * FROM cylinder_hist WHERE cylinder_id = ? ORDER BY hist_datetime DESC",
        (cylinder_id,),
    )
    return cur.fetchone()


def get_billing_item(challan_id):
    con, cur = connect_db()
    cur.execute("SELECT * FROM billing WHERE challan_id = ?", (challan_id, ))
    return cur.fetchone()


def get_inventory_items():
    con, cur = connect_db()
    cur.execute(
        "SELECT * FROM cylinder_info cc WHERE ( \
            SELECT place FROM cylinder_hist WHERE cylinder_id = cc.cylinder_id AND \
            hist_datetime = ( \
                SELECT MAX(hist_datetime) FROM cylinder_hist WHERE cylinder_id = cc.cylinder_id)) = 0"
    )
    return cur.fetchall()


def get_empty_cylinder_ids():
    con, cur = connect_db()
    cur.execute(
        "SELECT cylinder_id FROM cylinder_info cc WHERE \
            cc.current_condition = 'Empty' AND ( \
            SELECT place FROM cylinder_hist WHERE cylinder_id = cc.cylinder_id AND \
            hist_datetime = ( \
                SELECT MAX(hist_datetime) FROM cylinder_hist WHERE cylinder_id = cc.cylinder_id)) = 0"
    )
    return cur.fetchall()


def get_full_cylinder_ids():
    con, cur = connect_db()
    cur.execute(
        "SELECT cylinder_id FROM cylinder_info cc WHERE \
            cc.current_condition = 'Full' AND ( \
            SELECT place FROM cylinder_hist WHERE cylinder_id = cc.cylinder_id AND \
            hist_datetime = ( \
                SELECT MAX(hist_datetime) FROM cylinder_hist WHERE cylinder_id = cc.cylinder_id)) = 0"
    )
    return cur.fetchall()


def get_inventory_item(cylinder_id):
    con, cur = connect_db()
    cur.execute("SELECT * FROM cylinder_info WHERE cylinder_id = ?", (cylinder_id,))
    return cur.fetchone()


def modify_inventory_item(data):
    con, cur = connect_db()
    cur.execute(
        "UPDATE cylinder_info SET cylinder_type = ?, capacity = ?, manufacturer = ?, current_condition = ? WHERE cylinder_id = ?",
        (
            data["cylinder_type"],
            data["capacity"],
            data["manufacturer"],
            data["current_condition"],
            data["cylinder_id"],
        ),
    )
    con.commit()


def insert_inventory_item(data):
    con, cur = connect_db()
    cur.execute(
        "INSERT INTO cylinder_info VALUES (?, ?, ?, ?, ?)",
        (
            data["cylinder_id"],
            data["cylinder_type"],
            data["capacity"],
            data["manufacturer"],
            data["current_condition"],
        ),
    )
    cur.execute(
        "INSERT INTO cylinder_hist VALUES (?, ?, ?, ?, ?)",
        (data["cylinder_id"], 0, None, None, datetime.datetime.now()),
    )
    con.commit()


def get_refilling_items():
    con, cur = connect_db()
    cur.execute(
        "SELECT cc.*, ch.refilling \
        FROM cylinder_info cc \
        JOIN cylinder_hist ch ON cc.cylinder_id = ch.cylinder_id \
        WHERE ch.hist_datetime = ( \
            SELECT MAX(hist_datetime) \
            FROM cylinder_hist \
            WHERE cylinder_id = cc.cylinder_id \
        ) \
        AND (SELECT place FROM cylinder_hist WHERE \
            cylinder_id = cc.cylinder_id AND hist_datetime = ch.hist_datetime) = 1"
    )
    return cur.fetchall()


def get_customer_items():
    con, cur = connect_db()
    cur.execute(
        "SELECT cc.*, ch.customer \
        FROM cylinder_info cc \
        JOIN cylinder_hist ch ON cc.cylinder_id = ch.cylinder_id \
        WHERE ch.hist_datetime = ( \
            SELECT MAX(hist_datetime) \
            FROM cylinder_hist \
            WHERE cylinder_id = cc.cylinder_id \
        ) \
        AND (SELECT place FROM cylinder_hist WHERE \
            cylinder_id = cc.cylinder_id AND hist_datetime = ch.hist_datetime) = 2"
    )
    return cur.fetchall()


def get_challan_items():
    con, cur = connect_db()
    cur.execute("SELECT * FROM challan ORDER BY challan_id DESC")

    return cur.fetchall()


def get_challan_cylinder_items(challan_id):
    con, cur = connect_db()
    cur.execute(
        "SELECT * FROM challan_cylinder t1 JOIN cylinder_info t2 \
                WHERE challan_id = ? AND t1.cylinder_id = t2.cylinder_id",
        (challan_id,),
    )
    return cur.fetchall()


def new_empty_challan(data):
    con, cur = connect_db()
    cur.execute(
        "INSERT INTO challan VALUES (?, ?, ?, ?, ?)",
        (
            data["challan_id"],
            data["challan_date"],
            0,
            data["challan_where"],
            data["vehicle"],
        ),
    )
    for cylinder_id in data["cylinder_id"]:
        cur.execute(
            "INSERT INTO challan_cylinder VALUES (?, ?)",
            (data["challan_id"], cylinder_id),
        )
        cur.execute(
            "INSERT INTO cylinder_hist VALUES (?, ?, ?, ?, ?)",
            (cylinder_id, 1, data["challan_where"], None, data["challan_date"]),
        )
    con.commit()


def new_full_challan(data):
    con, cur = connect_db()
    cur.execute(
        "INSERT INTO challan VALUES (?, ?, ?, ?, ?)",
        (
            data["challan_id"],
            data["challan_date"],
            1,
            data["challan_where"],
            data["vehicle"],
        ),
    )
    cur.execute(
        "INSERT INTO billing VALUES (?, ?, ?)",
        (data["challan_id"], data["total_cost"], data["total_tax"]),
    )
    for cylinder_id in data["cylinder_id"]:
        cur.execute(
            "INSERT INTO challan_cylinder VALUES (?, ?)",
            (data["challan_id"], cylinder_id),
        )
        cur.execute(
            "INSERT INTO cylinder_hist VALUES (?, ?, ?, ?, ?)",
            (cylinder_id, 2, None, data["challan_where"], data["challan_date"]),
        )
    con.commit()


def refill_come_back(cylinder_id):
    con, cur = connect_db()
    curtime = datetime.datetime.now()
    cur.execute(
        "INSERT INTO cylinder_hist VALUES (?, ?, ?, ?, ?)",
        (cylinder_id, 0, None, None, curtime),
    )
    cur.execute(
        "UPDATE cylinder_info SET current_condition = ? WHERE cylinder_id = ?",
        ("Full", cylinder_id),
    )
    con.commit()


def customer_come_back(cylinder_id):
    con, cur = connect_db()
    curtime = datetime.datetime.now()
    cur.execute(
        "INSERT INTO cylinder_hist VALUES (?, ?, ?, ?, ?)",
        (cylinder_id, 0, None, None, curtime),
    )
    cur.execute(
        "UPDATE cylinder_info SET current_condition = ? WHERE cylinder_id = ?",
        ("Empty", cylinder_id),
    )
    con.commit()
