from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch, NotFoundError
import logging

app = Flask(__name__)

es = Elasticsearch("http://localhost:9200")
logging.basicConfig(level=logging.INFO)

if not es.ping():
    logging.error("Cannot connect to Elasticsearch. Please check your connection.")
else:
    logging.info("Connected to Elasticsearch.")

def validate_product(product):
    required_fields = ["product_id", "name", "price"]
    for field in required_fields:
        if field not in product:
            return False, f"Field '{field}' is required."
    return True, ""

@app.route("/products", methods=["POST"])
def add_product():
    product = request.json
    is_valid, message = validate_product(product)
    if not is_valid:
        return jsonify({"error": "Invalid product data", "message": message}), 400
    try:
        res = es.index(index="products", id=product["product_id"], body=product)
        return jsonify({"result": res['result'], "id": res['_id']}), 201
    except Exception as e:
        logging.error(f"Failed to add product: {e}")
        return jsonify({"error": "Failed to add product", "message": str(e)}), 500

@app.route("/products", methods=["GET"])
def get_all_products():
    page = int(request.args.get("page", 1))
    size = int(request.args.get("size", 10))
    start = (page - 1) * size
    
    try:
        query = {
            "query": {
                "match_all": {}
            },
            "from": start,
            "size": size
        }
        
        res = es.search(index="products", body=query)

        response = {
            "page": page,
            "page_size": size,
            "total_items": res["hits"]["total"]["value"],
            "products": [hit["_source"] for hit in res["hits"]["hits"]]
        }
        
        return jsonify(response), 200
    except Exception as e:
        logging.error(f"An error occurred while retrieving all products: {e}")
        return jsonify({"error": "An error occurred", "message": str(e)}), 500


@app.route("/products/<id>", methods=["GET"])
def get_product(id):
    try:
        res = es.get(index="products", id=id)
        return jsonify(res["_source"]), 200
    except NotFoundError:
        logging.warning(f"Product with id {id} not found.")
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        logging.error(f"An error occurred while retrieving product {id}: {e}")
        return jsonify({"error": "An error occurred", "message": str(e)}), 500

@app.route("/products/<id>", methods=["PUT"])
def update_product(id):
    product_data = request.json
    try:
        res = es.update(index="products", id=id, body={"doc": product_data})
        return jsonify({"result": res["result"]}), 200
    except NotFoundError:
        logging.warning(f"Product with id {id} not found.")
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        logging.error(f"Failed to update product {id}: {e}")
        return jsonify({"error": "Failed to update product", "message": str(e)}), 500

@app.route("/products/<id>", methods=["DELETE"])
def delete_product(id):
    try:
        es.delete(index="products", id=id)
        return jsonify({"result": "deleted"}), 200
    except NotFoundError:
        logging.warning(f"Product with id {id} not found.")
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        logging.error(f"Failed to delete product {id}: {e}")
        return jsonify({"error": "Failed to delete product", "message": str(e)}), 500

@app.route("/products/search", methods=["GET"])
def search_products():
    search = request.args.get("q")
    if not search:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    query = {
        "query": {
            "match_phrase_prefix": {
                "name": search
            }
        },
        "sort": [
            {
                "rating": {
                    "order": "desc"
                }
            }
        ]
    }
    try:
        res = es.search(index="products", body=query)
        return jsonify([hit["_source"] for hit in res["hits"]["hits"]]), 200
    except Exception as e:
        logging.error(f"An error occurred during search: {e}")
        return jsonify({"error": "An error occurred", "message": str(e)}), 500
    
@app.route("/products/bulk", methods=["POST"])
def bulk_add_products():
    products = request.json
    actions = []

    for product in products:
        is_valid, message = validate_product(product)
        if not is_valid:
            return jsonify({"error": "Invalid product data", "message": message}), 400

        action = {
            "index": {
                "_index": "products",
                "_id": product["product_id"]
            }
        }
        actions.append(action)
        actions.append(product)

    try:
        res = es.bulk(body=actions)
        if res['errors']:
            logging.error("Some documents failed to index.")
            return jsonify({"error": "Some products failed to insert", "details": res}), 500
        return jsonify({"result": "success", "indexed": len(products)}), 201
    except Exception as e:
        logging.error(f"Failed to bulk insert products: {e}")
        return jsonify({"error": "Failed to bulk insert products", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
