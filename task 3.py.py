from flask import Flask, render_template, request
import uuid
from db import get_db, create_tables

app = Flask(__name__)
create_tables()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book")
def book():
    return render_template("book.html")

@app.route("/confirm", methods=["POST"])
def confirm():
    name = request.form["name"]
    route = request.form["route"]

    # Server-side fixed pricing
    pricing = {
        "Route A": 50,
        "Route B": 70,
        "Route C": 100
    }

    price = pricing.get(route, 0)
    ticket_id = str(uuid.uuid4())

    db = get_db()
    db.execute(
        "INSERT INTO tickets (name, route, price, ticket_id) VALUES (?, ?, ?, ?)",
        (name, route, price, ticket_id)
    )
    db.commit()
    db.close()

    return render_template("ticket.html",
                           name=name,
                           route=route,
                           price=price,
                           ticket_id=ticket_id)

if __name__ == "__main__":
    app.run(debug=True)
