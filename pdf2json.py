import pdfplumber
import json
import string
import re
# Convert pdf to string
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text_content = ""
        for page in pdf.pages:
            text_content += page.extract_text()
    return text_content

#Remove Punctutations
def remove_punctuation(text_content):
    #Translation table
    translation_table = str.maketrans("", "", string.punctuation)
    result_string = text_content.translate(translation_table)

    return result_string

def convert_txt(text_content):
    text_content=remove_punctuation(text_content)
    final_txt=text_content.split("\n")
    final_txt= [value for value in final_txt if value]
    return final_txt
def load_json(json_path):
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    return data


        
def common_attributes_score(product):
    score = 0

    if "description" in product:
        score += 1
    elif "name" in product:
        score+=1
    elif "price" in product:
        score += 1
    
    return score

def score_medicine(product):
    score = common_attributes_score(product)
    
    if "category" in product and product["category"].lower() == "medicine":
        score += 4
    
    return score

def score_office_supplies(product):
    score = common_attributes_score(product)
    
    if "category" in product and product["category"].lower() == "office supplies":
        score += 4
    
    return score

def score_home_decor(product):
    score = common_attributes_score(product)

    if "category" in product and product["category"].lower() == "home decor":
        score += 4
    
    return score
def score_food(product):
    score = common_attributes_score(product)
    if "category" in product and product["category"].lower() =="food":
        score+=4
    return score

if __name__ == "__main__":
    pdf_path =( r"C:\Imp stuff\Nestle_Catalogue_web.pdf")
    text_content = extract_text_from_pdf(pdf_path)
    final_txt=convert_txt(text_content)

   
    
    json_file_path =(r"C:\Imp stuff\Nestle_Catalogue_web.json")
    data = load_json(json_file_path)
    
    with open(json_file_path, "w") as json_file:
        json.dump(final_txt, json_file, indent=2)
    
    print(f"Data extracted and saved to '{json_file_path}'.")

    '''for i in range(len(final_txt)):
        print(final_txt[i])
        if i%3==0:
            print('\t')'''
    

data = [
    "Product Catalogue",
    "2024Nestl\u00e9 KITKAT Smooth",
    "Hazelnut 45g",
    "Units per outer 40",
    "RRP 220",
    "Nestl\u00e9 KITKAT 4 Finger 45g",
    "Units per outer 48",
    "RRP 220",
    # ... (the rest of your data)
    "Top Ranking Nestl\u00e9 Product"
]

# Initialize a list to store dictionaries of product information
products = []
current_product = None

# Iterate through the data
for item in data:
    # Check if the item starts with "2024" to identify the start of a new product
    if item.startswith("2024"):
        # Save the previous product information if available
        if current_product:
            products.append(current_product)
        
        # Initialize a new product dictionary
        current_product = {"category":"","name": item, "description": "", "price": "", "units_per_outer": ""}
    
    # Check if the item starts with "Units per outer" to get additional information
    elif item.startswith("Units per outer"):
        current_product["units_per_outer"] = re.search(r'\d+', item).group()

    #category  (abhi sirf dekhne ke liye daal rha hu)- Shivain
    elif item.startswith("Nestl\u00e9"):
        current_product["category"] = "Food"
    # Check if the item starts with "RRP" to get the price
    elif item.startswith("RRP"):
        current_product["price"] = re.search(r'\d+', item).group()

    # If none of the conditions match, consider it as a description
    else:
        if current_product:
            current_product["description"] += item + " "

# Append the last product to the products list
if current_product:
    products.append(current_product)

# Display the extracted information
for product in products:
    print(product)
    for product in products:
        if product:
            if "category" in product:
                category = product["category"].lower()
                if category == "medicine":
                    product_score = score_medicine(product)
                elif category == "office supplies":
                    product_score = score_office_supplies(product)
                elif category == "home decor":
                    product_score = score_home_decor(product)
                elif category == "food":
                    product_score = score_food(product)
                else:
                    # Default case for unknown categories
                    product_score = common_attributes_score(product)
                
                print(f"Product: {product['name']}, Category: {category}, Score: {product_score}")