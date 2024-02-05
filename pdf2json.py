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


#Define scoring criteria
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
def score_electronics(product):
    score=common_attributes_score(product)
    if "Power Consumption" in product["desription"]:
        score+=3
    if "Display Size" in product["description"]:
        score+=2
    if "Operating System" in product["description"]:
        score+=3
    if "Warranty" in product["description"]:
        score+=3
    if "Certificatoins" in product["description"]:
        score+=2
    return score
def score_cosmetics(product):
    score = common_attributes_score(product)
    if "Ingredients" in product["description"]:
        score += 3
    if "Type" in product["description"]:
        score += 2
    if "Usage" in product["description"]:
        score += 2
    if "Skin Type" in product["description"]:
        score += 2
    if "Expiry Date" in product["description"]:
        score += 3
    return score
def score_sports(product):
    score = common_attributes_score(product)
    if "Sport Type" in product["description"]:
        score += 3
    if "Durability" in product["description"]:
        score += 2
    if "Size" in product["description"]:
        score += 2
    if "Weight" in product["description"]:
        score += 2
    if "Material" in product["description"]:
        score += 3
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
    elif category=="electronics":
        score+=score_electronics(product)
    elif category=="cosmetics":
        score+=score_cosmetics(product)
    elif category=="sports":
        score+=score_sports(product)

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
        elif any(keyword in item for keyword in ["screwdriver", "pliers", "wrench", "hammer", "tape measure", 
            "saw", "drill", "nut driver", "bolt cutter", "level", 
            "vise", "hacksaw", "chisel", "soldering iron", "multimeter", 
            "cable tester", "pliers", "wire stripper", "screwdriver set", "socket wrench", 
            "power drill", "pliers set", "adjustable wrench", "utility knife", "crescent wrench", 
            "allen wrench", "safety glasses", "work gloves", "tool belt", "laser level", 
            "workbench", "tool chest", "air compressor", "measuring tape", "pliers", 
            "hex key set", "c-clamp", "vice grip", "crowbar", "bolt", 
            "nut", "washer", "dremel", "angle grinder", "screw assortment", 
            "nail gun", "staple gun", "router", "circular saw", "band saw", 
            "belt sander", "jigsaw", "mallet", "trowel", "putty knife", 
            "hobby knife", "stud finder", "screw extractor", "pipe wrench", "plunger", 
            "pipe cutter", "pipe threader", "pipe bender", "heat gun", "paint scraper", 
            "wire brush", "flashlight", "headlamp", "cabinet hardware", "drawer slides", 
            "door hinge", "lockset", "latch", "fasteners", "nuts and bolts", 
            "abrasive paper", "sandpaper", "epoxy", "wood glue", "adhesive", 
            "sealant", "caulk", "lubricant", "grease", "WD-40", 
            "tool organizer"]):
            return "tool"
        elif any(keyword in item for keyword in ["necklace", "bracelet", "earrings", "ring", "pendant", 
            "brooch", "choker", "anklet", "bangle", "locket", 
            "cufflinks", "watch", "tiara", "hairpin", "charms", 
            "pearls", "gemstone", "diamond", "gold", "silver", 
            "platinum", "rose gold", "engagement ring", "wedding band", "hoop earrings", 
            "statement necklace", "birthstone", "sterling silver", "vintage jewelry", "costume jewelry", 
            "beaded bracelet", "charm bracelet", "fine jewelry", "jewelry box", "jewelry organizer", 
            "pendant necklace", "gemstone earrings", "diamond pendant", "bracelet stack", "stackable rings", 
            "initial necklace", "personalized jewelry", "jewelry set", "art deco jewelry", "bohemian jewelry", 
            "cubic zirconia", "filigree", "lock and key jewelry", "layered necklace", "cross necklace", 
            "pearl necklace", "agate", "amethyst", "sapphire", "ruby", 
            "emerald", "topaz", "opal", "turquoise", "peridot", 
            "moonstone", "quartz", "jade", "malachite", "onyx", 
            "agate", "garnet", "morganite", "tanzanite", "cameo jewelry", 
            "coral jewelry", "victorian jewelry", "art nouveau jewelry", "edwardian jewelry", "georgian jewelry", 
            "estate jewelry", "custom jewelry", "handmade jewelry", "fashion jewelry", "jewelry making", 
            "jewelry designer", "jewelry workshop", "jewelry repair", "beading", "wire wrapping", 
            "jewelry appraisal", "jewelry cleaning", "jewelry care", "jewelry display", "jewelry exhibition", 
            "precious stones", "semi-precious stones", "jewelry trends", "birthstone jewelry", "ethical jewelry", 
            "fair trade jewelry", "sustainable jewelry", "vintage-inspired jewelry", "modern jewelry", "minimalist jewelry", 
            "contemporary jewelry", "boho chic jewelry", "luxury jewelry", "affordable jewelry", "ethnic jewelry"]):
            return "jewellery"
        elif any(keyword in item for keyword in ["novel", "fiction", "non-fiction", "bestseller", "literature",
            "mystery", "thriller", "science fiction", "fantasy", "romance",
            "historical fiction", "biography", "autobiography", "memoir", "self-help",
            "business", "economics", "history", "philosophy", "psychology",
            "science", "technology", "art", "music", "poetry",
            "classic literature", "young adult", "children's books", "picture book", "graphic novel",
            "comic book", "manga", "cookbook", "travel", "adventure",
            "dystopian", "political thriller", "coming-of-age", "bestselling author", "book series",
            "book club", "library", "bookstore", "e-book", "audiobook",
            "hardcover", "paperback", "book cover", "bookshelf", "reading list",
            "literary award", "book review", "book adaptation", "fictional characters", "plot twists",
            "page-turner", "bibliophile", "book lover", "bookworm", "reading glasses",
            "book signing", "author interview", "book recommendation", "book release", "book sale",
            "book launch", "book festival", "literary festival", "book fair", "reading habits",
            "bookbinding", "book design", "book illustration", "first edition", "rare books",
            "book collecting", "book donation", "book donation drive", "book subscription", "book swap",
            "book synopsis"]):
            return "book"
        elif any(keyword in item for keyword in ["Electricals", "Electronics", "Mobile", "Smartphone", "Gadget","DSLR",
             "Mirrorless", "Camcorder", "Photography", "Lens", "Tripod", 
            "Camera", "Memory Card", "Gaming Console", "PC", 
            "Gaming Laptop", "Monitor","Keyboard", "Gaming Mouse", "Headset", "Gaming Chair", "Desk", 
            "Gaming Controller", "iPhone", "Android", "Samsung Galaxy", "Smartphone Accessories", "Mobile Phones", 
            "Television", "Smart TV", "LED TV", "OLED TV", "QLED TV", "4K TV", "8K TV", "TV Stand", 
            "TV Wall Mount", "TV Accessories", "Video Camera", "Action Camera", "Camcorder", 
            "Video Editing Software", "Video Production", "Video Accessories", "Smartwatch", 
            "Fitness Tracker", "Activity Tracker", "Smart Glasses", "Wearable Technology", "Wearable Accessories", 
            "Over-Ear Headphones", "On-Ear Headphones", "In-Ear Headphones", "Wireless Headphones", 
            "Noise-Canceling Headphones", "Earbuds", "Headphone Amplifier", "Headphone Case", "Desktop PC", 
            "All-in-One PC", "Workstation", "Mini PC", "PC Accessories", "PC Components", "PC Peripherals", "iPad", 
            "Android Tablet", "Windows Tablet", "Tablet Accessories", "Tablet Stands", "Tablet Cases", "Amazon Echo", 
            "Amazon Kindle", "Amazon Fire Tablet", "Amazon Fire TV", "Amazon Echo Accessories", "DVD Player", "DVD Recorder", 
            "Portable DVD Player", "DVD Movies", "DVD Storage", "Laptops", "Ultrabooks", "Chromebooks", "2-in-1 Laptops", "Laptop Accessories", 
            "Laptop Bags", "Nintendo Switch", "Switch Controllers", "Switch Games", "Switch Dock", "Switch Case", "Switch Screen Protector", 
            "Projector", "Home Theater Projector", "Mini Projector", "4K Projector", "Projector Screen"]):
            return "electronics"
        elif any(keyword in item for keyword in ["Cosmetics", "Beauty", "Makeup", "Skincare", "Perfume", "Lipstick","Foundation", "Eyeshadow", "Mascara", "Eyeliner", "Blush", "Bronzer", 
            "Highlighter", "Concealer", "Primer", "Setting Spray", "Setting Powder", 
            "BB Cream", "CC Cream", "Tinted Moisturizer", "Lip Gloss", "Lip Liner", 
            "Lip Balm", "Lip Stain", "Lip Plumper", "Lip Scrub", "Eyebrow Pencil", 
            "Eyebrow Gel", "Eyebrow Powder", "Eyebrow Pomade", "Eyebrow Tint", 
            "Eyelash Curler", "False Eyelashes", "Eyelash Glue", "Makeup Brushes", 
            "Makeup Sponges", "Makeup Remover", "Face Wash", "Cleanser", "Toner", 
            "Serum", "Moisturizer", "Face Oil", "Face Mask", "Sheet Mask", "Eye Cream", 
            "Night Cream", "Day Cream", "Sunscreen", "Body Lotion", "Body Butter", 
            "Body Oil", "Body Wash", "Shampoo", "Conditioner", "Hair Mask", "Hair Oil", 
            "Hair Serum", "Dry Shampoo", "Hair Spray", "Hair Gel", "Hair Wax", 
            "Hair Mousse", "Hair Styling Cream", "Nail Polish", "Nail Polish Remover", 
            "Nail Strengthener", "Nail Growth Serum", "Nail Care Kit", "Cuticle Oil", 
            "Cuticle Cream", "Nail File", "Nail Buffer", "Nail Clippers", 
            "Nail Scissors", "Nail Art Kit", "Nail Stickers", "Nail Decals", 
            "Nail Gems", "Nail Brushes", "Nail Drying Spray", "Nail Dryer", 
            "Nail UV Lamp", "Nail Top Coat", "Nail Base Coat", "Nail Hardener", 
            "Nail Wraps", "Nail Dip Powder", "Nail Extension Kit", "Nail Tips", 
            "Nail Glue", "Nail Acetone", "Nail Fungus Treatment", 
            "Nail Antibacterial Solution", "Nail Dehydrator", "Nail Cleanser"]):
            return "cosmetics"
        elif any(keyword in item for keyword in ["Sports", "Fitness", "Athletics", "Exercise", "Workout", "Sportswear", "Equipment", "Gym","Sports", "Fitness", "Athletics", "Exercise", "Workout", "Sportswear", 
            "Equipment", "Gym", "Running", "Cycling", "Swimming", "Yoga", "Pilates", 
            "CrossFit", "Weightlifting", "Cardio", "Strength Training", "Endurance", 
            "Training", "Training Shoes", "Running Shoes", "Sports Shoes", 
            "Athletic Shoes", "Exercise Mat", "Yoga Mat", "Resistance Bands", 
            "Jump Rope", "Dumbbells", "Kettlebells", "Barbells", "Weight Plates", 
            "Treadmill", "Exercise Bike", "Elliptical Trainer", "Rowing Machine", 
            "Fitness Tracker", "Fitness Watch", "Heart Rate Monitor", 
            "Activity Tracker", "Sports Bra", "Athletic Wear", "Compression Clothing", 
            "Moisture-Wicking Apparel", "Sports Shorts", "Athletic Pants", 
            "Sports Tops", "Athletic Jackets", "Sports Socks", "Sports Accessories", 
            "Water Bottle", "Sports Bag", "Gym Bag", "Fitness Gloves", "Gym Towel", 
            "Sports Sunglasses", "Sports Hat", "Headbands", "Wristbands", 
            "Compression Sleeves", "Sports Tape", "Muscle Rub", "Sports Nutrition", 
            "Protein Powder", "Pre-Workout Supplement", "Post-Workout Supplement", 
            "Energy Bars", "Sports Drinks", "Electrolyte Replenishment", 
            "Hydration Packs", "Foam Roller", "Massage Ball", "Massage Stick", 
            "Sports Medicine", "First Aid Kit", "Injury Support", 
            "Recovery Accessories", "Fitness Technology", "Smart Fitness Equipment", 
            "Fitness Apps", "Training Programs", "Online Coaching", 
            "Sports Performance Analysis", "Fitness Community", "Athlete Training", 
            "Sports Psychology", "Mindfulness Training", "Motivational Tools", 
            "Sports Recovery", "Rest and Recovery", "Sleep Optimization", 
            "Stretching Routine", "Hydrotherapy", "Cryotherapy", "Massage Therapy", 
            "Heat Therapy", "Cold Therapy", "Compression Therapy", "Float Tanks", 
            "Sauna", "Steam Room"]):
            return "sports"
    
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