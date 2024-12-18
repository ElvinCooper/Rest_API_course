import uuid
from flask import Flask, request
from db import stores, items
from flask_smorest import abort

app = Flask(__name__)



@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}

@app.get("/item")
def get_articulos():
    return {"items": list(items.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()    
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/item")  
def create_item():
    item_data = request.get_json()
    if (        
        "store_id" not in item_data 
        or "precio" not in item_data           
        or "descripcion" not in item_data        
    ):
        abort(400, message="Bad request. Asegure que el precio y el su id esten incluidos en el json")
    if item_data["store_id"] not in stores:
        abort(404, message= "Store not found")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
        
    return item, 201
        

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError: 
        abort(404, message= "Store not found")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items["item_id"]
    except KeyError:
        abort(404, message= "Store not found")
