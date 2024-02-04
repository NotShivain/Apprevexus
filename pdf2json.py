import pdfplumber
import json
import string
import re
import os
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

def score_tool(product):
    score = common_attributes_score(product)
    if "category" in product and product["category"].lower() =="tool":
        score+=4
    return score

def score_jewellery(product):
    score = common_attributes_score(product)
    if "category" in product and product["category"].lower() =="jewellery":
        score+=4
    return score

def score_book(product):
    score = common_attributes_score(product)
    if "category" in product and product["category"].lower() =="book":
        score+=4
    return score


def extract_product_info(data, category_keywords):
    products = []
    current_product = None

    for item in data:
        if item.startswith("2024"):
            if current_product:
                products.append(current_product)
            current_product = {"category":"","name": item, "description": "", "price": ""}
        elif item.startswith("Nestl\u00e9"):
            current_product["category"] = "food"
        elif item.startswith("RRP"):
            match = re.search(r'\d+', item)
            if match:
                current_product["price"] = match.group()
        else:
            if current_product:
                current_product["description"] += item + " "

    if current_product:
        products.append(current_product)

    return products

def print_product_info(product, category):
    if product:
        product_score = calculate_score(product, category)
        print(f"Product: {product['name']}, Category: {category}, Score: {product_score}")

def calculate_score(product, category):
    score = common_attributes_score(product)

    if category == "medicine":
        score += score_medicine(product)
    elif category == "office supplies":
        score += score_office_supplies(product)
    elif category == "home decor":
        score += score_home_decor(product)
    elif category == "food":
        score += score_food(product)
    elif category == "tool":
        score += score_tool(product)
    elif category == "jewellery":
        score += score_jewellery(product)
    elif category == "book":
        score += score_book(product)

    return score

def detect_category(final_txt):
    for item in final_txt:
        if any(keyword in item for keyword in ["Medicine", "Tablets", "Prescription"]):
            return "medicine"
        elif any(keyword in item for keyword in ["Office Supplies", "Stationery", "Notebook"]):
            return "office supplies"
        elif any(keyword in item for keyword in ["Decor", "Furniture", "Home"]):
            return "home decor"
        elif any(keyword in item for keyword in [ "Chocolate", "Candy", "Chips", "Cookies", "Biscuits", "Nuts", "Popcorn", "Crackers",
    "Pretzels", "Gummies", "Snack Bars", "Granola Bars", "Vanilla", "Strawberry", "Caramel",
    "BBQ", "Sour", "Spicy", "Honey", "Salted", "Sweet", "Salty", "Cheese", "Units", "Weight",
    "Packaging", "Box", "Bag", "Pouch", "Multi-pack", "RRP", "Discounts", "Special Offers",
    "Price per unit", "Brand", "Brand names", "Product lines", "Dietary", "Gluten-free", "Vegan",
    "Limited edition", "Top-selling", "Recommended", "Edition", "Promotion", "Limited-time",
    "Flavor", "Crunchy", "Chewy", "Savory", "Sweetened", "Organic", "Natural", "Fresh", "Unique",
    "Exotic", "Artisan", "Classic", "Traditional", "Rich", "Premium", "Authentic", "Homemade",
    "Family recipe", "Irresistible", "Indulgent", "Delight", "Zesty", "Tangy", "Tasty", "Delicious",
    "Gourmet", "Wholesome", "Nutritious", "Refreshing", "Crispy", "Luscious", "Juicy", "Zingy",
    "Mouthwatering", "Satisfying", "Yummy", "Tempting", "Flavorful", "Robust", "Sizzling",
    "Tantalizing", "Scrumptious", "Hearty", "Spiced", "Crave", "Zippy", "Divine", "Velvety",
    "Piquant", "Peppery", "Chewy", "Munchable", "Nourishing"]):
            return "food"
    
    return None

def process_category(pdf_path, json_path):
    text_content = extract_text_from_pdf(pdf_path)
    final_txt = convert_txt(text_content)
    data = load_json(json_path)
    category = detect_category(final_txt)

    if category:
        products = extract_product_info(data, [])
        for product in products:
            product["category"] = category
            print_product_info(product, category)
    else:
        print("Could not detect the category.")

if __name__ == "__main__":
    pdf_path = r"../Nestle_Catalogue_web.pdf"
    json_file_path = r"../Nestle_Catalogue_web.json"
    if not os.path.exists(json_file_path):
        text_content = extract_text_from_pdf(pdf_path)
        final_txt = convert_txt(text_content)
        with open(json_file_path, "w") as json_file:
            json.dump(final_txt, json_file, indent=2)
        print(f"Data extracted and saved to '{json_file_path}'.")
        process_category(pdf_path,json_file_path)
    else:
        process_category(pdf_path, json_file_path)