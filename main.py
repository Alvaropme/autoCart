from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()  
driver.get("https://tienda.mercadona.es/#content")
time.sleep(2) 

with open('list.txt', 'r', encoding='utf-8') as file:
    products = file.readlines()

count = products.__len__()

cookies_btn = driver.find_element(By.XPATH, '//button[contains(@class, "ui-button--positive") and text()="Aceptar"]')
cookies_btn.click()
print("Cookies aceptadas.")

postal_Input = driver.find_element(By.NAME, "postalCode")
postal_Input.send_keys("15002")
search_btn = driver.find_element(By.XPATH, "//*[@id=\"root\"]/div[5]/div/div[2]/div/form/button")
search_btn.click()
print("Código postal enviado.")
time.sleep(2)

for product in products[0].split(','):
    product = product.strip()
    print(f"Buscando producto: {product}")
    input_search = driver.find_element(By.ID, 'search')
    input_search.clear()
    input_search.send_keys(product)
    time.sleep(2)
    print(f"Quedan {count} productos por buscar.")
    count -= 1  
    try:
        counts = getattr(driver, "_product_counts", {})
        count = counts.get(product, 0)

        if count == 0:
            first_result = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[1]/div/section/div/div[1]/div/div/div[2]/button')
            first_result.click()
        else:
            try:
                increase_btn = driver.find_element(By.XPATH, '//*[@id="button-picker-increase"]')
                increase_btn.click()
            except Exception:
                first_result = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[2]/div[1]/div/section/div/div[1]/div/div/div[2]/button')
                first_result.click()

        counts[product] = count + 1
        setattr(driver, "_product_counts", counts)
        print(f"Producto '{product}' añadido al carrito.")
        if not getattr(driver, "_popup_closed_once", False):
            time.sleep(1)
            try:
                close_popup = driver.find_element(By.XPATH, '//*[@id="modal-info"]/div/div/div/button[2]')
                close_popup.click()
                print("Popup cerrado.")
            except Exception:
                print("No hay popup para cerrar.")
            finally:
                setattr(driver, "_popup_closed_once", True)
        time.sleep(1)
    except Exception as e:
        print(f"No se encontró el producto: {product}. Error: {e}")

input("Comprueba que todo está correcto y presiona Enter para cerrar...")


