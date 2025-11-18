import requests
import json

# categorias = [112, 156, 135, 118, 89, 164, 86, 46, 78, 48, 147, 122, 27, 77, 32, 65, 897, 105, 99]
count = 0
todos_los_nombres = []

def extraer_nombres(category):
    if "products" in category:
        for producto in category["products"]:
            todos_los_nombres.append(producto["display_name"]+"-"+str(producto["bulk_price"]))
    if "categories" in category:
        for subcategoria in category["categories"]:
            extraer_nombres(subcategoria)

for cat_id in range(0, 1001):
    url = f"https://tienda.mercadona.es/api/categories/{cat_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        extraer_nombres(data)
        print(count)
        count += 1

    else:
        print(f"No se pudo obtener la categoría {cat_id}, status code: {response.status_code}")

with open("productos_mercadona.json", "w", encoding="utf-8") as f:
    json.dump(todos_los_nombres, f, ensure_ascii=False, indent=4)

print(f"Se guardaron {len(todos_los_nombres)} productos en 'productos_mercadona.json'.")
