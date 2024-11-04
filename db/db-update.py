import mysql.connector
import requests
from PyPDF2 import PdfReader
import hashlib
import subprocess
import datetime

PDF_FILE_PATH = 'db/menu.pdf'
COMMON_PHP_PATH = 'frontend/common.php'

class Product:
    def __init__(self, product_info: dict):
        self.name = product_info['name']
        self.category = product_info['category']
        self.flavor = product_info['flavor']
        self.ingredients = product_info['ingredients']
        self.allergens = product_info['allergens']
        self.warning = product_info['warning']

    def __repr__(self):
        ret = f'product name - {self.name}\n'
        ret += f'category - {self.category}\n'
        ret += f'flavor - {self.flavor}\n'
        ret += f'ingredients - {self.ingredients}\n'
        ret += f'allergens - {self.allergens}\n'
        if len(self.warning.strip()) > 0: ret += f'warning - {self.warning}\n'
        ret += '\n\n'
        return ret

def extract_product(raw: str) -> dict:
    ret = {}
    ret['name'] = raw.split('PRODUCT NAME')[0].replace('PRODUCT NAME', '').split('CATEGORY')[0].strip()
    ret['category'] = raw.split('CATEGORY')[-1].replace('CATEGORY', '').split('FLAVOR')[0].strip()
    ret['flavor'] = raw.split('FLAVOR')[-1].replace('FLAVOR', '').split('INGREDIENTS')[0].strip()
    ret['ingredients'] = raw.split('INGREDIENTS')[-1].split('ALLERGENS')[0].strip().replace('\n', ' ')
    ret['allergens'] = raw.split('ALLERGENS')[-1].replace('ALLERGENS', '').split('WARNING')[0].strip().replace('\n', ' ')
    ret['warning'] = raw.split('WARNING')[-1].replace('WARNING', '').strip().replace('\n', ' ') if 'WARNING' in raw else ''
    return ret

if __name__ == '__main__':
    # Get the current menu's hash
    calculated_hash = None
    with open(PDF_FILE_PATH, 'rb') as menu_file:
        data = menu_file.read()
        calculated_hash = hashlib.md5(data).hexdigest()

    print(calculated_hash)
    # Download the most recent menu
    url = 'https://www.dunkindonuts.com/content/dam/dd/pdf/allergy_ingredient_guide.pdf'
    request = requests.get(url, allow_redirects=True)
    if hashlib.md5(request.content).hexdigest() == calculated_hash:
        # Exit if not different from current menu
        print('No need to update menu. Exiting now')
        exit()
    with open(PDF_FILE_PATH, 'wb') as menu_file:
        menu_file.write(request.content)
        print('Menu downloaded')

    # Update frontend novelty display
    with open(COMMON_PHP_PATH, 'w') as file:
        file.write(f"""<?php
    $time_fetched = "{datetime.datetime.now().strftime('%I:%M %p').lstrip('0')} US/Eastern";
    $date_fetched = "{datetime.date.today().strftime('%m.%d.%Y')}";
?>
<meta charset="utf-8">
<link rel="stylesheet" href="https://unpkg.com/simpledotcss/simple.min.css">
<link rel="stylesheet" href="custom.css">
<title>Dunkin' Allergen Search</title>
                   """)

    # Connect to database
    allergens_db = None
    try:
        allergens_db = mysql.connector.connect(
            host='localhost',
            user='dunkin_admin',
            password='TODO CHANGE ME',
            database='dunkin_allergens'
        )
        print('Database connection succeeded')
    except:
        print('Failed to connect to database')

    # Extract data from menu
    with open(PDF_FILE_PATH, 'rb') as menu_file:
        # Open PDF
        pdfdoc = PdfReader(menu_file)
        
        # Get all text from the menu
        pages = ''.join([x.extract_text() for x in pdfdoc.pages])
        
        # Chop to limited time products
        pages = pages.rsplit('LIMITED TIME PRODUCTS')[1]
        
        # Split limited time products and permanent products
        limited = pages.split('PERMANENT PRODUCTS')[0].split('Allergen information is available at www')[0]
        permanent = pages.split('PERMANENT PRODUCTS')[1]

        # Serialize products
        limited_products = list(set([Product(extract_product(x)) for x in limited.split('PRODUCT NAME')]))
        permanent_products = list(set([Product(extract_product(x)) for x in permanent.split('PRODUCT NAME') if extract_product(x)['name'] != '']))

        # Write products to database
        cursor = allergens_db.cursor()
        for p in limited_products:
            query = f'INSERT INTO menu (product_name, category, flavor, ingredients, allergens, warning) VALUES ("{p.name}", "{p.category}", "{p.flavor}", "{p.ingredients}", "{p.allergens}", "{p.warning}")'
            cursor.execute(query)
        
        for p in permanent_products:
            try:
                query = f'INSERT INTO menu (product_name, category, flavor, ingredients, allergens, warning) VALUES ("{p.name}", "{p.category}", "{p.flavor}", "{p.ingredients}", "{p.allergens}", "{p.warning}")'
                cursor.execute(query)
            except:
                query = f'SELECT product_name FROM menu WHERE LOWER(product_name) LIKE "%{p.name.lower()}%"'
                cursor.execute(query)
                for x in cursor:
                    print(x)

        allergens_db.commit()