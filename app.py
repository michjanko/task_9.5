from flask import Flask, request, make_response, render_template, redirect, url_for, jsonify, abort

from forms import CoinForm
from models import coins

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error(r)': 'Not found(d)', 'status_code(e)': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error(r)': 'Bad request(t)', 'status_code(e)': 400}), 400)

@app.route('/coins/', methods=["GET", "POST"])
def coins_list():
    form = CoinForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            coins.create(form.data)
            coins.save_all()
        return redirect(url_for("coins_list"))
    
    return render_template("coins.html", form=form, coins=coins.all(), error=error)

@app.route("/coin/<int:coin_id>/", methods=["GET", "POST"])
def coin_details(coin_id):
    coin = coins.get(coin_id)
    form = CoinForm(data=coin)

    if request.method == "POST":
        if form.validate_on_submit():
            coins.update(coin_id, form.data)
        return redirect(url_for("coins_list"))
    return render_template("coin.html", form=form, coin_id=coin_id)

@app.route("/api/v1/coins/", methods=["GET"])
def coins_list_api_v1():
    return jsonify(coins.all())
    
@app.route("/api/v1/coin/<int:coin_id>", methods=["GET"])
def get_coin(coin_id):
    coin = coins.get(coin_id)
    if not coin:
        abort(404)
    return jsonify({"coin": coin})

@app.route("/api/v1/coins/", methods=["POST"]) #do sprawdzenia nie wiem jak daje się załączniki/ kilka wierszy w terminalu
def create_coin():
    if not request.json or not 'full_name' in request.json:
        abort(400)
    coin = {
        'full_name': request.json['full_name'],
        'short_name': request.json['short_name'],
        'price': request.json['price'],
        'logo': request.json['logo'],
        #'id': coins[-1]["id"] + 1 - id -> jest dodawane w models.py w funkcji create
        }
    coins.create(coin)
    return jsonify({'coin': coin}, 201)

@app.route("/api/v1/coin/<int:coin_id>", methods=['DELETE'])
def delete_coin(coin_id):
    result = coins.delete(coin_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/coin/<int:coin_id>", methods=["PUT"]) #pisane na odwal bez sprawdzania. idę spać
def update_coin(coin_id):
    coin = coins.get(coin_id)
    if not coin:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'full_name' in data and not isinstance(data.get('full_name'), str),
        'short_name' in data and not isinstance(data.get('short_name'), str) #tu powinienem dopisać warunki
    ]):
        abort(400)
    coin = {
        'full_name': data.get('full_name', coin['full_name']),
        'short_name': data.get('short_name', coin['short_name']),
        'price': data.get('price', coin['price']),
        'logo': data.get('logo', coin['logo']),
    }
    coins.update(coin_id, coin)
    return jsonify({'coin': coin})

if __name__ == "__main__":
    app.run(debug=True)
