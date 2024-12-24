import uuid
from flask import Flask, request
from db import stores, items
from flask_smorest import abort


app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "descripcion" not in store_data:
        abort(
            400, 
            message="Bad request. asegurese de que la descripcion este incluida en el json"
        )
    for store in stores.values():
        if store_data["descripcion"] == store["descripcion"]:
            abort(400, message=f"el store ya existe.")
       
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


@app.post("/item")  
def create_item():
    item_data = request.get_json()
    if (        
        "store_id" not in item_data 
        or "precio" not in item_data           
        or "descripcion" not in item_data        
    ):
        abort(400, message="Bad request. Asegure que el precio y el id esten incluidos en el json"
        )
    for item in items.values():
        if (
            item_data["descripcion"] == item_data["descripcion"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"El item ya existe")

    if item_data["store_id"] not in stores:
        abort(404, message= "Store not found")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
        
    return item, 201


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "El item fue eliminado."}
    except KeyError: 
        abort(404, message= "Item not found")


# enpoint para eliminar un store con su respectivo id
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "El store fue eliminado."}
    except KeyError: 
        abort(404, message= "Store not found")        


# enpoint para actualizar un item con su respectivo id
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "precio" not in item_data or "descripcion" not in item_data:
        abort(400, message="Bad request. Asegurese de que el precio y descripcion esten en el json")
    
    try:
        item = item[item_id]
        item |= item_id
        return item
    except KeyError:
        abort(404, message="Item not found")


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
        abort(404, message= "Store not found"), 404
