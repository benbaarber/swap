"""
Funky crypto game website, some dumb name for money, admin can POST and DELETE different coins, another role can
PATCH (withdraw or add funds to invest) and all roles can GET. maybe free and premium versions where free can only access
bitcoin and premium can access more.
"""

import datetime
from importlib.metadata import requires
import json
import os

from flask import Flask, Response, abort, redirect, send_from_directory,jsonify, make_response, request
from flask_cors import CORS

from swap.crypto import get_current_value
from swap.db_util.orm import Investment, User, db, setup_db
from auth import AuthError, requires_auth, requires_scope

# from auth import requires_auth, username


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)
    setup_db(app)

    # @requires_auth('get:investments')
    @requires_auth
    @app.get("/user/<username>/investments")
    def list_investments(username):
        if requires_scope("read:investments"):
            if db.session.query(User).get(username) is None:
                abort(404)
            investments = (
                db.session.query(Investment).filter(Investment.username == username).all()
            )
            data = []
            total_asset_value = float(0)
            for investment in investments:
                data.append(investment.serialize())
                total_asset_value += investment.amount * get_current_value(investment.coin)

            return make_response(
                (dict(total_asset_value=total_asset_value, data=data), 200, {})
            )
        abort(401)

    @requires_auth
    @app.post("/user/<username>/investments")
    def buy(username):
        if requires_scope("create:investments"):
            coin = request.json.get("coin")
            amount = request.json.get("amount")
            current_user = db.session.query(User).get(username)

            if None in [coin, amount]:
                abort(400)

            coin_price = get_current_value(coin)

            if coin_price is None:
                abort(422)

            if coin_price * amount > current_user.balance:
                abort(409)

            current_user.balance -= coin_price * amount
            current_user.update()
            investment = Investment(
                username=username,
                coin=coin,
                amount=amount,
                date=datetime.datetime.now(),
            )
            investment.insert()
            return make_response((dict(investment_id=investment.id), 201, {}))
        abort(401)

    # Add choice between flat currency amount and coin ammount
    @requires_auth
    @app.delete("/user/<username>/investments/<id>")
    def sell(username, id):
        if requires_scope("delete:investments"):
            investment = db.session.query(Investment).get(id)

            if investment is None:
                abort(404)

            coin_price = float(get_current_value(investment.coin))
            user = db.session.query(User).get(username)

            user.balance += coin_price * investment.amount
            user.update()
            investment.delete()

            return Response(status=204)
        abort(401)

    @requires_auth
    @app.get("/user/<username>")
    def get_user_info(username):
        if requires_scope("read:user"):
            user_model = db.session.query(User).get(username)
            return (
                make_response((user_model.serialize(), 200, {}))
                if user_model
                else abort(404)
            )
        abort(401)

    @requires_auth
    @app.post("/user")
    def new_account():
        username = request.json.get("username")
        if username is None:
            abort(406)
        if db.session.query(User).get(username):
            return make_response(({"message": "Username taken"}, 409, {}))
        User(username=username, balance=float(50000), swap_metadata={}).insert()
        return make_response(({"message": "Account created"}, 201, {}))

    # Requires admin role
    @requires_auth
    @app.patch("/user/<username>")
    def give_bonus(username):
        if requires_scope("update:user"):
            bonus = float(request.json.get("bonus"))
            one_lucky_sob = db.session.query(User).get(username)
            if one_lucky_sob is None or bonus <= 0:
                abort(400)
            one_lucky_sob.balance += bonus
            one_lucky_sob.update()
            return make_response((one_lucky_sob.serialize(), 202, {}))
        abort(403)

    @app.route('/', defaults={'path': '/index.html'})
    @app.route("/<path:path>")
    def send_client(path):
        return send_from_directory(os.environ.get("CLIENT_DIR"), path)

    @app.route("/oauth")
    def login():
        return redirect("https://dev-h0m7eost.us.auth0.com/authorize")

    # Error Handlers
 
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400, 
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False, 
            "error": 400, 
            "message": "unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False, 
            "error": 400, 
            "message": "forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404, 
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405, 
            "message": "method not allowed"
        }), 405
    
    @app.errorhandler(406)
    def not_acceptable(error):
        return jsonify({
            "success": False, 
            "error": 405, 
            "message": "not acceptable"
        }), 406

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            "success": False, 
            "error": 405, 
            "message": "conflict"
        }), 409

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422, 
            "message": "unprocessable"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


APP = create_app()

if __name__ == "__main__":
    print(f"RUNNING IN: {os.path.dirname(os.path.realpath(__file__))}")
    print(f"CLIENT AT: {os.environ.get('CLIENT_DIR')}")
    print(f"PORT: {os.environ.get('PORT')}")
    APP.run(host="0.0.0.0", port=os.environ.get("PORT"), debug=True)
