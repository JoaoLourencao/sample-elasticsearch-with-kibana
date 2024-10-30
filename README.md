# Product Catalog API with Flask, Elasticsearch, and Kibana

## 📄 Project Overview

This project is a RESTful API built with Flask for managing a product catalog with CRUD functionalities. The data is stored and queried using Elasticsearch, and Kibana is used to visualize insights about product categories, pricing, availability, and ratings.

## 🚀 Features

- **CRUD Operations**: Add, retrieve, update, and delete products with various attributes.
- **Bulk Product Insertion**: Insert multiple products at once for efficient data management.
- **Advanced Filtering and Pagination**: Sort, filter, and paginate product data for enhanced user experience.
- **Data Visualization in Kibana**: Visual dashboards for monitoring stock status, product ratings, and price distributions by category.

## 🛠️ Tech Stack

- **Flask**: Web framework for building the API.
- **Elasticsearch**: Search engine for efficient data storage and retrieval.
- **Kibana**: Visualization tool for building dashboards and analyzing product data.

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/product-catalog-api.git
cd product-catalog-api
```

### 2. Set up the Environment

#### Create a virtual environment (optional but recommended):

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Elasticsearch and Kibana

Ensure that Elasticsearch and Kibana are installed and running locally.

1. **Start Elasticsearch**:
   - Download and install Elasticsearch.
   - After installation, navigate to the Elasticsearch folder and run:
  
   ```bash
   # Start Elasticsearch
   ./bin/elasticsearch
   ```
   
  - Elasticsearch will be available at http://localhost:9200.
  
2. **Start Kibana**:
    - Download and install Kibana from Kibana Downloads.
    - After installation, navigate to the Kibana folder and run:
      
   ```bash
    # Start Kibana
    ./bin/kibana
   ```
   
  - Kibana will be available at http://localhost:5601.


## 🚀 Running the API

To start the Flask server, run:

```bash
python app.py
```

## 📊 Kibana Setup

1. Open Kibana in your browser at [http://localhost:5601](http://localhost:5601).
2. Go to **Management** > **Index Patterns** to create an index pattern for `products`.
3. Use **Visualizations** to create charts and dashboards for monitoring product data, such as price ranges, availability, and ratings.

