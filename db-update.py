import mysql.connector
import requests
from PyPDF2 import PdfReader
from io import StringIO

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
        ret += f'ingredients -\n'
        for ingredient in self.ingredients:
            ret += f'\t{ingredient.split(":")[0]}:\n'
            for constituent in ingredient.split(':')[1:]:
                ret += f'\t\t{constituent}\n'
        ret += f'allergens - {self.allergens}\n'
        if len(self.warning.strip()) > 0: ret += f'warning - {self.warning}\n'
        ret += '\n\n'
        return ret

def extract_product(raw: str) -> dict:
    ret = {}
    ret['name'] = raw.split('PRODUCT NAME')[0].replace('PRODUCT NAME', '').split('CATEGORY')[0].strip()
    ret['category'] = raw.split('CATEGORY')[-1].replace('CATEGORY', '').split('FLAVOR')[0].strip()
    ret['flavor'] = raw.split('FLAVOR')[-1].replace('FLAVOR', '').split('INGREDIENTS')[0].strip()
    ret['ingredients'] = raw.split('INGREDIENTS')[-1].split('ALLERGENS')[0].strip().replace('\n', ' ').split('; ')
    ret['allergens'] = raw.split('ALLERGENS')[-1].replace('ALLERGENS', '').split('WARNING')[0].strip().replace('\n', ' ')
    ret['warning'] = raw.split('WARNING')[-1].replace('WARNING', '').strip().replace('\n', ' ') if 'WARNING' in raw else ''
    return ret

if __name__ == '__main__':
    # Download the most recent menu
    url = 'https://www.dunkindonuts.com/content/dam/dd/pdf/allergy_ingredient_guide.pdf'
    request = requests.get(url, allow_redirects=True)
    with open('menu.pdf', 'wb') as menu_file:
        menu_file.write(request.content)
        print('Menu downloaded')

    # Establish in-memory collections
    limited_time_products = set()
    permanent_products = set()

    # Extract data from menu
    # TODO: Exit if hash is same as that of last menu parsed
    with open('menu.pdf', 'rb') as menu_file:
        pdfdoc = PdfReader(menu_file)
        
        # Get all text from the menu
        pages = ''.join([x.extract_text() for x in pdfdoc.pages])
        
        # Chop to limited time products
        pages = pages.rsplit('LIMITED TIME PRODUCTS')[1]
        
        # Split limited time products and permanent products
        limited = pages.split('PERMANENT PRODUCTS')[0].split('Allergen information is available at www')[0]
        permanent = pages.split('PERMANENT PRODUCTS')[1]

        # Serialize products
        limited_products = [Product(extract_product(x)) for x in limited.split('PRODUCT NAME')]
        for product in limited_products[1:5]:
            print(product)

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


    