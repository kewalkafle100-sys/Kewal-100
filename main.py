from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

PASSWORD = "1234"
logged_in = False

items = {
    "cleaning": ["handwash", "lizol", "harpic", "toilet paper", "paper towel"],
    "gifts": ["tshirt black", "tshirt blue", "tote bag", "cup", "pen", "copy", "key ring", "bottle"]
}

stock = {}
logs = []

for group in items:
    for item in items[group]:
        stock[item] = 0


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Stock System</title>
<style>
body {font-family: Arial; margin:0; background: #1e3c72; color:white;}
.container {padding:20px;}
.box {background: rgba(255,255,255,0.1); padding:15px; margin:10px; border-radius:10px;}
input, select {width:100%; padding:8px; margin:5px 0;}
button {width:100%; padding:10px; background:#00c6ff; border:none;}
.grid {display:grid; grid-template-columns:1fr 1fr; gap:10px;}
.card {background:rgba(255,255,255,0.1); padding:10px; border-radius:8px;}
</style>
</head>
<body>

<div class="container">

<h2>📦 Stock Management System</h2>

{% if not logged_in %}

<div class="box">
<form method="POST">
<input type="password" name="password" placeholder="Enter Password">
<button type="submit">Login</button>
</form>
</div>

{% else %}

<div class="box">
<form method="POST">

<input name="person" placeholder="Person Name">
<input name="vendor" placeholder="Vendor Name">
<select name="action">
<option value="in">Stock IN</option>
<option value="out">Stock OUT</option>
</select>

<h3>Cleaning Items</h3>
<div class="grid">
{% for i in items['cleaning'] %}
<div class="card">
{{i}}<input name="{{i}}" placeholder="Qty">
</div>
{% endfor %}
</div>

<h3>Gift Items</h3>
<div class="grid">
{% for i in items['gifts'] %}
<div class="card">
{{i}}<input name="{{i}}" placeholder="Qty">
</div>
{% endfor %}
</div>

<button type="submit">Submit</button>
</form>
</div>

<div class="box">
<h3>Stock</h3>
{% for k,v in stock.items() %}
<p>{{k}} : {{v}}</p>
{% endfor %}
</div>

<div class="box">
<h3>Logs</h3>
{% for l in logs %}
<p>{{l}}</p>
{% endfor %}
</div>

{% endif %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET","POST"])
def home():
    global logged_in, stock, logs

    if request.method == "POST":

        if not logged_in:
            if request.form.get("password") == PASSWORD:
                logged_in = True
            return render_template_string(HTML, logged_in=logged_in, stock=stock, logs=logs, items=items)

        person = request.form.get("person","-")
        vendor = request.form.get("vendor","-")
        action = request.form.get("action")

        date = datetime.now().strftime("%Y-%m-%d")

        log = f"{date} | {person} | {vendor} | {action} | "

        for item in stock:
            qty = request.form.get(item)
            if qty and qty.isdigit():
                qty = int(qty)

                if action == "in":
                    stock[item] += qty
                    log += f"{item}+{qty} "

                else:
                    stock[item] -= qty
                    if stock[item] < 0:
                        stock[item] = 0
                    log += f"{item}-{qty} "

        logs.append(log)

    return render_template_string(HTML, logged_in=logged_in, stock=stock, logs=logs, items=items)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
