from flask import Flask, request

app = Flask('__name__')

stores = [{
    "name": "test",
    "items": [
        {"name": "chair",
         "price": 15.99}

    ]
}]

@app.get('/store') # 127.0.0.1:500/store
def get_store():
    return stores


@app.post('/store')
def send_store():
    request_data = request.get_json()
    store = {"name": request_data["name"], "item": []}
    stores.append(store)
    return store, 201


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item
    return {"message": "Store not found"}, 404