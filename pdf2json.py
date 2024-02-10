import pdfplumber
import json
import string
import re
import os
import streamlit as st
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
def common_attributes_score(product,count):
    score = 0
    avg_desc_len = len(product['description']) // count
    if "description" in product:
        score += 1
    elif "name" in product:
        score+=1
    elif "price" in product:
        score += 1
    if 40<avg_desc_len<60:
        score+=1
    if 30<avg_desc_len<70:
        score+=1
    if 20<avg_desc_len<80:
        score+=1
    return score

def score_medicine(product,count):
    score = common_attributes_score(product,count)
    
    if "category" in product and product["category"].lower() == "medicine":
        score += 4
    
    return score

def score_office_supplies(product,count):
    score = common_attributes_score(product,count)
    
    if "category" in product and product["category"].lower() == "office supplies":
        score += 4
    
    return score

def score_home_decor(product,count):
    score = common_attributes_score(product,count)

    if "category" in product and product["category"].lower() == "home decor":
        score += 4
    
    return score

def score_food(product,count):
    score = common_attributes_score(product,count)
    if "category" in product and product["category"].lower() =="food":
        score+=4
    return score

def score_tool(product,count):
    score = common_attributes_score(product,count)
    desc_criteria=['name','model','brand','tool type','type','size','dimensions',
    'power','source','battery','manual','weight','kg','pound','heavy','light',
    'durability', "material","features", "usage","application","quality", "price", "warranty",
    "compatibility", "safety","features", "maintenance", "accessories",
    "certifications","standards", "reviews","testimonials", "technical","specifications",
    "country of manufacture","country","country of origin","origin", "environmental impact", "packaging", "shipping"]
    
    if "category" in product and product["category"].lower() =="tool":
        score+=4
    if product["description"].length() in range(250,350):
        score+=1
    for word in desc_criteria:
        if word in set(product["description"].lower().split()):
            score+=1
    return score

def score_jewellery(product,count):
    score = common_attributes_score(product,count)
    desc_criteria=["name","model", "brand", "material", "metal", "gemstone", "size","dimensions", "weight",
    "style", "design", "occasion", "price", "availability", "certifications","standards", 
    "customer","review","testimonials", "care","instructions", "packaging", "shipping",
    "type","clasp","chain", "earring","type", "ring","size", "bracelet","length", "necklace",
     "finishing", "hallmark", "engraving", "birthstone", "diamond","clarity",
    "cut", "color", "pearl", "customization","purity"]
    if "category" in product and product["category"].lower() =="jewellery":
        score+=4
    for word in desc_criteria:
        if word in set(product["description"].lower().split()):
            score+=1
    
    return score

def score_book(product,count):
    score = common_attributes_score(product,count)
    desc_criteria=["title", "author", "publisher", "publication","date", "genre", "format", "language",
    "page","count", "ISBN", "summary", "reviews", "awards", "bestseller","contents","acknowledgments", "preface", "introduction",
    "plot", "characters", "setting", "themes", "style","demographic","edition",
    "conflict", "resolution", "climax", "symbolism", "motifs",
    "foreshadowing", "flashbacks", "tone", "mood", "narrative","structure","cover","hardcover","paperback","art","accolades"]
    if "category" in product and product["category"].lower() =="book":
        score+=4
    for word in desc_criteria:
        if word in set(product["description"].lower().split()):
            score+=1
    return score
def score_electronics(product,count):
    score=common_attributes_score(product,count)
    if "Power Consumption" in product["desription"]:
        score+=1
    if "Display Size" in product["description"]:
        score+=1
    if "Operating System" in product["description"]:
        score+=1
    if "Warranty" in product["description"]:
        score+=1
    if "Certificatoins" in product["description"]:
        score+=1
    return score
def score_cosmetics(product,count):
    score = common_attributes_score(product,count)
    if "Ingredients" in product["description"]:
        score += 1
    if "Type" in product["description"]:
        score += 1
    if "Usage" in product["description"]:
        score += 1
    if "Skin Type" in product["description"]:
        score += 1
    if "Expiry Date" in product["description"]:
        score += 1
    return score
def score_sports(product,count):
    score = common_attributes_score(product,count)
    if "Sport Type" in product["description"]:
        score += 1
    if "Durability" in product["description"]:
        score += 1
    if "Size" in product["description"]:
        score += 1
    if "Weight" in product["description"]:
        score += 1
    if "Material" in product["description"]:
        score += 1
    return score
def score_grocery(product,count):
    score = common_attributes_score(product,count)
    if "Weight" in product["description"]:
        score +=1
    if "Price" in product["description"]:
        score +=1
    if "Expiry Date" in product["description"]:
        score +=1
    if "Packaging" in product["description"]:
        score +=1
    return score
def  score_apparel(product,count):
    score = common_attributes_score(product,count)
    if "Size" in product["description"]:
        score +=1
    if "Color" in product["description"]:
        score +=1
    if "Material" in product["description"]:
        score +=1
    if "Price" in product["description"]:
        score +=1
    if  "Care Instructions" in product["description"]:
        score +=1
    return score 
def score_appliances(product,count):
    score =common_attributes_score(product,count)
    if "Category" in product["description"]:
        score +=1
    if "Model Number" in product["description"]:
        score +=1
    if "Power Consumption" in product["description"]:
        score +=1
    if "Warranty" in product["description"]:
        score +=1
    if "User Manual" in product["description"]:
        score +=1
    return score


def extract_product_info(data, category_keywords):
    products = []
    current_product = None
    count=0
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
                count+=1
    if current_product:
        products.append(current_product)

    return products,count

def print_product_info(product, category,count):
    if product:
        product_score = calculate_score(product, category,count)
        print(f"Product: {product['name']}, Category: {category}, Score: {product_score}")

def calculate_score(product, category,count):
    score = common_attributes_score(product,count)

    if category == "medicine":
        score += score_medicine(product,count)
    elif category == "office supplies":
        score += score_office_supplies(product,count)
    elif category == "home decor":
        score += score_home_decor(product,count)
    elif category == "food":
        score += score_food(product,count)
    elif category == "tool":
        score += score_tool(product,count)
    elif category == "jewellery":
        score += score_jewellery(product,count)
    elif category == "book":
        score += score_book(product,count)
    elif category=="electronics":
        score+=score_electronics(product,count)
    elif category=="cosmetics":
        score+=score_cosmetics(product,count)
    elif category=="sports":
        score+=score_sports(product,count)
    elif category=="grocery":
        score += score_grocery(product,count)
    elif category=="apparels":
        score+= score_apparel(product,count)
    elif category=="appliances":
        score+=score_appliances(product,count)


    return score

def detect_category(final_txt):
    for item in final_txt:
        if any(keyword in item for keyword in ["Medicine", "Tablets", "Prescription"]):
            return "medicine"
        elif any(keyword in item for keyword in ["Office Supplies", "Stationery", "Notebook"]):
            return "office supplies"
        elif any(keyword in item for keyword in ["Decor", "Furniture", "Home"]):
            return "home decor"
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
        elif any(keyword in item for keyword in ["Grocery", "Fruits", "Vegetables", "Lean Protein", "Chicken", "fish", "Tofu",
                        "Whole Grains", "Nuts", "Seeds", "Dairy", "Dairy Alternatives", "Water", "Sports Drinks",
            "Healthy Snacks", "Nuts", "Greek Yogurt", "Trail Mix", "Fresh Herbs",
            "Cooking Oils", "Olive Oil", "Avocado Oil", "Eggs", "Quinoa",
            "Sweet Potatoes", "Leafy Greens", "Berries", "Bananas", "Whole Wheat Bread", "Brown Rice",
            "Milk", "Eggs", "Chicken Breast", "Salmon", "Quinoa", "Spinach",
            "Broccoli", "Blueberries", "Bananas", "Greek Yogurt", "Almonds", "Whole Wheat Pasta",
            "Avocado", "Tomatoes", "Sweet Potatoes", "Oranges", "Green Beans", "Brown Rice",
            "Olive Oil", "Cottage Cheese", "Whole Grain Bread", "Salad Greens", "Romaine Lettuce", "Red Leaf Lettuce", "Iceberg Lettuce", "Arugula", 
            "Radicchio", "Endive", "Spring Mix", "Cabbage", "Cranberry Sauce", "Pumpkin Puree", "Peaches", "Plums", "Cherries", "Bok Choy", "Snow Peas", 
            "Snap Peas", "Parsnips", "Turnips", "Rutabaga", "Watercress", "Capers", "Shallots", "Scallions", "Jicama", "Squash", "Cottage Cheese", "Blue Cheese",
            "Feta Cheese", "Gouda Cheese", "Cottage Cheese", "Ricotta Cheese", "Sour Cream", "Heavy Cream", "Coconut Cream", "Yeast", "Molasses", "Sesame Oil", "Rice Noodles",
            "Vermicelli", "Soy Milk", "Cottage Cheese", "Pumpkin Seeds", "Sunflower Seeds", "Sesame Seeds", "Popcorn Kernels", "Brown Sugar", "Powdered Sugar", "Coconut Flour", 
            "Almond Flour", "Flaxseed Meal", "Chickpea Pasta", "Whole Wheat Couscous", "Raisins", "Dates", "Walnuts", "Cashews", "Pecans", "Pumpkin Seeds", "Sunflower Oil", "Coconut Oil",
            "Flour", "Baking Powder", "Baking Soda", "Vanilla Extract", "Cinnamon", "Nutmeg", "Paprika", "Cumin", "Curry Powder", "Dijon Mustard", "Kale", "Zucchini", "Asparagus", "Eggplant", 
            "Radishes", "Beets", "Brussels Sprouts", "Cauliflower", "Artichokes", "Cilantro", "Parsley", "Thyme", "Rosemary", "Sage", "Basil", "Cocoa Powder", "Chickpea Flour", "Rice Vinegar", 
            "Apple Cider Vinegar", "Hot Sauce", "Whole Wheat English Muffins", "Cranberries", "Mangoes", "Kiwi", "Pears", "Pomegranates", "Tahini", "Provolone Cheese", "Parmesan Cheese", "Whole Wheat Bagels",
            "Shrimp", "Tilapia", "Tofu", "Tempeh", "Dark Leafy Greens", "Coconut Water", "Sparkling Water", "Whole Wheat Panko Breadcrumbs", "Whole Wheat Flour", "Honey", "Maple Syrup", "Peanut Butter", "Almond Butter", 
            "Oats", "Whole Wheat Tortillas", "Hummus", "Black Beans", "Chickpeas", "Lentils", "Ground Turkey", "Lean Beef", "Pork", "Whole Wheat Crackers", "Quinoa Pasta", 
            "Canned Tomatoes", "Cucumbers", "Carrots",
             "Bell Peppers", "Onions", "Garlic"]):
            return "grocery"
        elif any(keyword in item for keyword in ["apparels","Anorak", "Parka", "Windbreaker", "Raincoat", "Puffer Jacket", "Denim Jacket", "Leather Jacket", "Bomber Jacket", 
            "Vests", "Blazers", "Trench Coat", "Fur Coat", "Pea Coat", "Sweatpants", "Track Pants", "Cargo Pants", "Capris", 
            "Joggers", "Tunic", "Blazer Dresses", "Shift Dresses", "Wrap Dresses", "Maxi Dresses", "Mini Dresses", 
            "Midi Dresses", "Sheath Dresses", "A-Line Dresses", "Fit and Flare Dresses", "Sundresses", "Jeggings", 
            "Culottes", "Palazzo Pants", "Turtlenecks", "Tank Tops", "Camisoles", "Crop Tops", "Bodysuits", "Graphic Tees", 
            "Polo Shirts", "Henley Shirts", "Tunics", "Camisoles", "Kimono", "Shrugs", "Capes", "Ponchos", "Tuxedos", 
            "Clogs", "Mules", "Slides", "Platform Shoes", "Ballet Flats", "Wedges", "Derby Shoes", "Monk Strap Shoes", 
            "Chukka Boots", "Chelsea Boots", "Moccasins", "Snow Boots", "Rain Boots", "Wingtip Shoes", "Loafers", 
            "Driving Shoes", "Boat Shoes", "Satchels", "Crossbody Bags", "Hobo Bags", "Bucket Bags", "Messenger Bags", 
            "Satchels", "Totes", "Backpack Purses", "Duffel Bags", "Weekender Bags", "Wallets", "Clutches", "Berets", 
            "Fedora Hats", "Panama Hats", "Newsboy Caps", "Trapper Hats", "Sun Hats", "Berets", "Bucket Hats", "Visors", 
            "Beanies", "Sun Visors", "Turbans", "Fedoras", "Newsboy Caps", "Trapper Hats", "Sun Hats", "Trilby Hats", 
            "Boater Hats", "Baseball Caps", "Cowboy Hats", "Bucket Hats", "Berets", "Bowler Hats", "Panama Hats", "Visors", 
            "Fedoras", "Newsboy Caps", "Boater Hats", "Top Hats", "Beanies", "Cloche Hats", "Fascinators", "Derby Hats", 
            "Safari Hats", "Brimmed Hats", "Bandanas", "Neckerchiefs", "Pocket Squares", "Ascots", "Ties", "Bow Ties", 
            "Bolo Ties", "Cravats", "Scarves", "Mufflers", "Neck Warmers", "Shawls", "Stoles", "Snoods", "Gloves", "Mittens", 
            "Fingerless Gloves", "Touchscreen Gloves", "Arm Warmers", "Leg Warmers", "Socks", "Stockings", "Tights", 
            "Knee-High Socks", "Ankle Socks", "No-Show Socks", "Boot Socks", "Over-the-Knee Socks", "Thigh-High Socks", 
            "Compression Socks", "Fishnet Stockings", "Opaque Tights", "Sheer Tights", "Patterned Tights", "Athletic Socks", 
            "Running Socks", "Crew Socks", "Quarter Socks", "Dress Socks", "Hiking Socks", "Calf Sleeves", "Shoe Insoles", 
            "Shoe Trees", "Boot Shapers", "Shoe Polish", "Shoe Cleaning Kits", "Shoe Horns", "Shoe Bags", "Shoe Racks", 
            "Shoe Organizers", "Shoe Dryers", "Boot Brushes", "Shoe Shields", "Shoehorns", "Boot Jacks", "Shoe Stretchers", 
            "Shoe Inserts", "Shoe Deodorizers", "Shoe Laces", "Shoe Repair Kits", "Shoe Polish", "Shoe Cleaning Brushes", 
            "Shoe Storage Boxes", "Shoe Cabinets", "Shoe Benches", "Shoe Ottomans", "Shoe Cubbies", "Shoe Shelves", "Shoe Holders", 
            "Shoe Racks", "Shoe Organizers", "Shoe Hangers", "Shoe Hooks", "Shoe Bags", "Shoe Totes", "Shoe Covers", "Shoe Protectors", 
            "Shoe Shields", "Shoe Trees", "Shoe Horns", "Shoe Stretchers", "Shoe Inserts", "Shoe Insoles", "Shoe Liners","Shoe Pads"]):
            return "apparels"
        elif any(keyword in item for keyword in ["appliances",
            "Electric Fan", "Ceiling Fan", "Air Fryer Oven", "Electric Can Opener", "Electric Kettle",
            "Electric Blanket", "Electric Toothbrush Charger", "Handheld Vacuum", "Portable Heater", 
            "Portable Air Conditioner", "Food Chopper", "Electric Grater", "Soda Maker", "Egg Cooker", 
            "Crock-Pot", "Portable Induction Cooktop", "Electric Skillet", "Countertop Ice Maker", 
            "Deep Fryer", "Electric Smoker", "Electric Wine Opener", "Hand Blender", "Electric Milk Frother", 
            "Electric Peeler", "Electric Griddle", "Electric Food Warmer", "Electric Pasta Maker", 
            "Electric Can Opener", "Electric Knife Sharpener", "Electric Salt and Pepper Grinder", 
            "Electric Corkscrew", "Electric Jar Opener", "Electric Spiralizer", "Electric Wok", 
            "Electric Crepe Maker", "Electric Popcorn Popper", "Electric Food Slicer", "Electric Bread Slicer", 
            "Electric Tortilla Maker", "Electric Soup Maker", "Electric Meat Grinder", 
            "Electric Quesadilla Maker", "Electric Fondue Pot", "Electric Food Dehydrator", 
            "Electric Ice Cream Maker", "Electric Yogurt Maker", "Electric Pizzelle Maker", 
            "Electric Egg Poacher", "Electric Sausage Stuffer", "Electric Potato Peeler", 
            "Electric Cookie Press", "Electric Nut Grinder", "Electric Omelette Maker", 
            "Electric Bacon Cooker", "Electric Donut Maker", "Electric Gravy Warmer", 
            "Electric Hot Dog Cooker", "Electric Marshmallow Roaster", "Electric Pancake Maker", 
            "Electric Rice Cooker", "Electric S'mores Maker", "Refrigerator", "Microwave", 
            "Dishwasher", "Oven", "Stove", "Range Hood", "Blender", "Toaster", "Coffee Maker", 
            "Food Processor", "Stand Mixer", "Juicer", "Slow Cooker", "Pressure Cooker", 
            "Air Fryer", "Waffle Maker", "Rice Cooker", "Hand Mixer", "Kettle", 
            "Espresso Machine", "Grill", "Electric Griddle", "Food Steamer", 
            "Immersion Blender", "Can Opener", "Ice Cream Maker", "Bread Maker", 
            "Vacuum Sealer", "Toaster Oven", "Deep Fryer", "Dehydrator", "Electric Knife", 
            "Electric Skillet", "Sous Vide Precision Cooker", "Instant Pot", "Electric Grill", 
            "Popcorn Maker", "Hot Plate", "Garbage Disposal", "Water Dispenser", 
            "Wine Cooler", "Air Purifier", "Humidifier", "Air Conditioner", "Heater", 
            "Dehumidifier", "Washing Machine", "Dryer", "Iron", "Steam Cleaner", 
            "Vacuum Cleaner", "Dustbuster", "Robot Vacuum", "Hair Dryer", 
            "Hair Straightener", "Curling Iron", "Electric Toothbrush", 
            "Water Heater", "Garage Door Opener", "Smart Thermostat", 
            "Security Camera", "Smart Doorbell", "Smart Lock", "Smart Lighting", 
            "Smart Speaker", "Smart TV", "Smart Refrigerator", 
            "Smart Washer and Dryer", "Smart Vacuum"]):
            return"appliances"
        return None

def process_category(pdf_path, json_path):
    text_content = extract_text_from_pdf(pdf_path)
    final_txt = convert_txt(text_content)
    data = load_json(json_path)
    category = selected_category.lower

    if category:
        products,count = extract_product_info(data, [])
        for product in products:
            product["category"] = category
            print_product_info(product, category,count)
    else:
        print("Could not detect the category.")

st.title("Catalogue Scoring App")

    # Spinner for selecting categories
selected_category = st.selectbox("Select Category", ["Electronics","Cosmetics","Sports","Grocery","Pet","Apparel",
"Appliances", 
"Jewelry",
"Books",
"Tools",
"Medicine",
"Office Supplies",
"Home and decor"])

    # File uploader
uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

    # Button to trigger scoring
if st.button("Score"):
        if uploaded_file is not None:
            json_file_path = r"../Nestle_Catalogue_web.json"
            if not os.path.exists(json_file_path):
                text_content = extract_text_from_pdf(uploaded_file)
                print("extract text")
                final_txt = convert_txt(text_content)
                print("convert")
                with open(json_file_path, "w") as json_file:
                    json.dump(final_txt, json_file, indent=2)
                    print(f"Data extracted and saved to '{json_file_path}'.")
                    result = process_category(uploaded_file,json_file_path)
                    st.write("Scoring Result:")
                    st.write(result)

            else:
                result = process_category(uploaded_file, json_file_path)
                st.write("Scoring Result:")
                st.write(result)
        else:
            st.write("Please upload a file first")