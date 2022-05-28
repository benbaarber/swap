import pytest
from flask import Flask, url_for
from unittest.mock import patch

def test_post_user(client):
    res = client.post("/user", json=dict(username="foobar"))
    assert res.status_code == 201


def test_fail_post_user(client):
    res = client.post("/user", json=dict(noexisto="foobar"))
    assert res.status_code == 406


def test_get_user(client):
    res = client.get("/user/foobar")
    data = res.json
    assert res.status_code == 200
    assert all([i in data.keys() for i in ["username", "balance", "swap_metadata"]])


def test_fail_get_user(client):
    res = client.get("/user/nonehere")
    assert res.status_code == 404


def test_post_investment(client):
    res = client.post("/user/foobar/investments", json=dict(coin="LINK", amount=10))
    assert res.status_code == 201
    assert res.json.get("investment_id") is not None


def test_post_another_investment(client):
    res = client.post("/user/foobar/investments", json=dict(coin="BTC", amount=0.05))
    assert res.status_code == 201
    assert res.json.get("investment_id") is not None


def test_fail_post_investment(client):
    res = client.post("/user/foobar/investments", json=dict(coin="BUNGUS", amount=200))
    assert res.status_code == 422


def test_post_investment_insufficient_funds(client):
    res = client.post("/user/foobar/investments", json=dict(coin="BTC", amount=1000))
    assert res.status_code == 409


def test_get_investments(client):
    res = client.get("/user/foobar/investments")
    assert res.status_code == 200
    assert res.json is not None
    assert res.json.get("data") is not None
    assert isinstance(res.json.get("data"), list)
    assert len(res.json.get("data")) == 2
    assert res.json.get("data")[1].get("coin") == "BTC"


def test_fail_get_investments(client):
    res = client.get("/user/barfoo/investments")
    assert res.status_code == 404


def test_delete_investment(client):
    res = client.delete("/user/foobar/investments/2")
    res2 = client.get("/user/foobar/investments")
    assert res.status_code == 204
    assert len(res2.json.get("data")) == 1


def test_fail_delete_investment(client):
    res = client.delete("/user/foobar/investments/3")
    assert res.status_code == 404


def test_patch_user(client):
    res = client.patch("/user/foobar", json=dict(bonus=1500))
    assert res.status_code == 202
    assert res.json.get("balance") >= 0


def test_fail_patch_user(client):
    res = client.patch("/user/barfoo", json=dict(bonus=5000))
    assert res.status_code == 400
