import pdfplumber
import json
import string
import re
import os
import streamlit as st
import seaborn as sns
import plotly.express as px
# Convert pdf to string

def set_background_image():
    # Use HTML to set background image
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url(""https://wallpapersmug.com/large/c066e0/blue-abstract-wave-flow-minimalist.jpg"");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
    )

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
    if "name" in product:
        score+=1
    if "price" in product:
        score += 1
    if "manufactered" or "company" or "manufacturer" in product:
        score+= 1
    if 40<avg_desc_len<60:
        score+=1
    if 30<avg_desc_len<70:
        score+=1
    if 20<avg_desc_len<80:
        score+=1
    return score

def scale(total, score):
     value = (score/total)*10
     return round(value,2)

def score_medicine(product,count):
    score = common_attributes_score(product,count)
    desc_criteria=["drug", "dose", "dosage", "prescription", "storage", "cold", "dry", "disease", "flu", "fever", "kids", "adults",
                "manufactured", "science", "medical", "doctor", "expiry", "treatment", "symptom", "condition", "relief", "side effects", 
                "contraindications", "ingredients", "instructions", "tablet", "capsule", "liquid", "injection", "syringe", "pill", 
                "pain", "allergy", "infection", "antibiotic", "antiviral", "antifungal", "antiseptic", 
                "immunization", "vaccine", "supplement", "therapy", "recovery", "healing", "health", "wellness", 
                "warning", "adverse","effects", "consultation", "pharmacist", "pharmaceutics", "pharmacology", "formulation", 
                "patient", "compliance", "efficacy", "interactions"]
    if "category" in product and product["category"].lower() =="medicine":
        score+=4
    for word in desc_criteria:
        if word in set(product["description"].lower().split()):
            score+=1
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final

def score_office_supplies(product,count):
    score = common_attributes_score(product,count)
    desc_criteria=["quality", "paper", "tape", "print", "flow", "smooth", "sticky", "efficient", "manufactured", 
                                "stationery", "printer", "copier", "ink", "toner", "stapler", "staples", "binder", "folder", 
                                "organizer", "notebook", "pad", "pencil", "pen", "marker", "highlighter", "desk", "chair", 
                                "table", "shelf", "cabinet", "storage", "document", "file", "envelope", "mail", "shipping", 
                                "packing", "label", "post-it", "calendar", "planner", "tape dispenser", "glue", "scissors", 
                                "ruler", "calculator", "computer", "keyboard", "mouse", "monitor", "headset", "telephone", 
                                "fax", "scanner"]
    if "category" in product and product["category"].lower() =="office supplies":
        score+=4
    for word in desc_criteria:
        if word in set(product["description"].lower().split()):
            score+=1
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final

def score_home_decor(product,count):
    score = common_attributes_score(product,count)
    desc_criteria=["modern", "material", "quality", "beautiful", "home", "kitchen", "bathroom", "bedroom", "living", 
                           "space", "clean", "stylish", "customize", "personal", "color", "size", "durable", "design", 
                           "furniture", "decor", "accessories", "art", "lighting", "rug", "carpet", "curtain", "blind", 
                           "mirror", "frame", "painting", "decoration", "ornament", "vase", "pot", "plant", "flower", 
                           "cushion", "pillow", "throw", "blanket", "bedding", "mattress", "pillowcase", "duvet", "lamp", 
                           "chandelier", "fixture", "table", "chair", "sofa", "couch", "ottoman", "shelves", "cabinet", 
                           "storage", "organizer", "rack","help","contemporary"]
    
    if "category" in product and product["category"].lower() =="home decor":
        score+=4
    for word in desc_criteria:
        if word in set(product["description"].lower().split()):
            score+=1
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final

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
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final

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
    
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final

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
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final
def score_electronics(product,count):
    score=common_attributes_score(product,count)
    desc_criteria = ["name", "model", "brand", "type", "color", "material", "dimensions", "weight","screen",
    "screen size", "resolution", "processor", "RAM", "storage", "operating system",
    "battery", "capacity", "camera", "connectivity", "ports", "features", "compatibility",
    "warranty", "price", "availability", "ratings", "packaging", "shipping", "accessories",
    "certifications", "sensors", "input","output","input/output", "resolution", "display", "type", "audio",
    "processor speed", "graphics", "memory type", "network", 
    "accessibility", "power","consumption", "dimensions", "weight",
    "country of origin", "user manual", "software", "upgradability", "ergonomics","circuits" 
    "regulatory"," compliance"
    "Television", "TV", "Smartphone", "Phone", "Cellphone", "Mobile", "Computer", "Laptop", "Desktop", 
    "Tablet", "iPad", "Camera", "Digital camera", "DSLR", "Mirrorless camera", "Video camera", "Camcorder", 
    "Audio", "Speaker", "Headphones", "Earbuds", "Earphones", "Microphone", "Gaming", "Console", "PlayStation", 
    "Xbox", "Controller", "Remote", "Smartwatch", "Wearable", "Drone", 
    "Quadcopter", "Smart home", "Router", "Modem", "Printer", "Scanner", "Projector", "Monitor", "Display", 
    "Keyboard", "Mouse", "Mousepad", "Graphics card", "Processor", "CPU", "RAM", "Memory", "Hard drive", 
    "Solid state drive", "SSD", "Storage", "Battery", "Charger", "Adapter", "Dock", "Cable", "Wireless", 
    "Bluetooth", "Wi-Fi", "Internet", "Network", "Ethernet", "Fiber", "optic", "HDMI", "USB", "Thunderbolt", 
    "VGA", "DVI", "DisplayPort", "SD","card", "MicroSD", "Podcast", "E-book", "Kindle", "Nook", "Tablet", "App", "Software", "Operating system", 
    "iOS", "Android", "Windows", "MacOS", "Linux", "Virtual"," reality", "Augmented" "microchips", "AR", "VR"
]

    if "category" in product and product["category"].lower()=="electronics":
        score+=4
    for word in desc_criteria:
        if word in set(product["description"].lower().split()):
            score+=1
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final
def score_cosmetics(product,count):
    
    score = common_attributes_score(product,count)
    desc_criteria = ["name", "brand", "type", "color", "size", "shade", "formulation", "skin type",
    "skin concern", "coverage", "finish", "ingredients", "usage", "benefits", 
    "application", "scent", "packaging", "expiry date", "price", "availability",
    "ratings", "reviews", "certifications", "sustainability", "cruelty-free",
    "vegan", "dermatologist tested", "allergen information", "sensitivity",
    "patch test", "how to use", "directions", "warnings", "storage", 
    "country of origin", "user manual", "recommended age", "expiration date",
    "hypoallergenic", "non-comedogenic", "paraben-free", "sulfate-free",
    "phthalate-free", "gluten-free", "oil-free", "alcohol-free", "fragrance-free",
    "preservative-free", "silicone-free", "mineral oil-free", "dye-free",
    "artificial color-free", "oxybenzone-free", "water-resistant", "long-lasting"]
    if "category" in product and product["category"].lower() =="cosmetics":
        score+=4
    for word in desc_criteria:
        if word in set(product["description"].lower().split()):
            score+=1
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final
def score_sports(product,count):
    score = common_attributes_score(product,count)
    desc_criteria = ["name", "brand", "type", "sport", "color", "size", "material", "weight",
    "dimensions", "capacity", "fit", "closure", "sole", "upper material",
    "lining material", "design", "style", "technology", "features", 
    "durability", "comfort", "breathability", "flexibility", "traction",
    "support", "cushioning", "waterproof", "windproof", "thermal",
    "reflective", "UV protection", "pockets", "straps", "handles",
    "adjustability", "grip", "resistance", "performance", "maintenance",
    "assembly", "installation", "usage", "care", "instructions",
    "warnings", "safety", "certifications", "standards", "warranty",
    "price", "availability", "ratings", "reviews", "shipping",
    "packaging", "country of origin", "user manual", "recommended age",
    "suitable for", "level", "experience", "training", "competition",
    "recreation", "indoor", "outdoor", "terrain", "climate",
    "environment", "location", "season", "event", "league",
    "team", "player", "position", "activity", "exercise"]
    if "category" in product and product["category"].lower() =="sports":
        score+=4
    for word in desc_criteria:
        if word in set(product["description"].lower().split()):
            score+=1
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final


def score_grocery(product,count):
    score = common_attributes_score(product,count)
    desc_criteria=["name","product","top","tasty","useful","healthy","milk","chocolate","snacks","pet","cook","eat","home","kitchen","price","safe","RRP","weight","grocery", "supermarket", "food", "produce", "fruit", "vegetable", "grains", 
    "bread", "bakery", "dairy", "cheese", "yogurt", "eggs", "meat", "poultry", 
    "beef", "chicken", "pork", "seafood", "fish", "canned", "frozen", "fresh", 
    "organic", "natural", "snacks", "sweets", "candy", "cookies", "crackers", 
    "chips", "nuts", "beverages", "drinks", "juice", "soda", "water", "coffee", 
    "tea", "pantry", "spices", "condiments", "sauces", "oil", "vinegar", "salt", 
    "sugar", "flour", "rice", "pasta", "cereal", "soup", "canned", "beans", 
    "lentils", "baking", "mix", "dessert", "frozen", "pizza", "ice cream", 
    "frozen vegetables", "frozen fruits", "baby food", "pet food", "household", 
    "cleaning", "paper products", "toiletries", "personal care", "health", 
    "medicine", "vitamins", "supplements", "first aid"]
    if "category" in product and product["category"].lower() =="grocery":
        score+=4
    for word in desc_criteria:
        if word in set(product["description"].lower().split()):
            score+=1
    
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final
def  score_apparel(product,count):
    score = common_attributes_score(product,count)
    desc_criteria =["name","price","manufactured","Color", "Material", "Style", "Fit", "Pattern", "Length", "Neckline", 
                    "Sleeve length", "Details", "Occasion", "Brand", "Size range", "Seasonality", "Trendiness","collar"
    "Shirt", "T-shirt", "Top", "Pants", "Jeans", "Shorts", "Skirt", "Dress", "Jacket", "Coat", "Sweater", 
    "Hoodie", "Blazer", "Suit", "Vest", "Tunic", "Cardigan", "Kimono", "Romper", "Leggings", "Tights", 
    "Trousers", "Parka", "Anorak", "Raincoat", "Windbreaker", "Poncho", "Cape", "Swimsuit", "Bikini", 
    "Tankini", "Monokini", "Cover-up", "Sarong", "Robe", "Nightgown", "Pajamas", "Underwear", "Lingerie", 
    "Brassiere", "Bralette", "Panties", "Boxers", "Briefs", "Thong", "Bodysuit", "Camisole", "Corset", 
    "Garter", "Stockings", "Socks", "Tights", "Hosiery", "Slip", "Shapewear", "Athleisure", "Activewear", 
    "Swimwear", "Beachwear", "Loungewear", "Sleepwear", "Uniform", "Costume", "Outfit", "Attire", "Wear", "Denim", "Cotton", "Wool", "Leather", "Silk",
      "Linen", "Polyester", "Rayon", "Spandex", "Velvet",
    "Fleece", "Chiffon", "Satin", "Knit", "Cashmere", "Acrylic", "Flannel", "Twill", "Canvas", "Terry",
    "Corduroy", "Fur", "Suede", "Synthetic", "Microfiber", "Nylon", "Shearling", "Taffeta", "Tulle", "Lace",
    "Organza", "Brocade", "Mesh", "Gingham", "Seersucker", "Chambray", "Poplin", "Muslin", "Jacquard",
    "Batiste", "Georgette", "Voile", "Dupioni", "Damask", "Tweed", "Chenille", "Bouclé", "Crepe"]
    if "category" in product and product["category"].lower()=="apparel":
        score+=4
        for word in desc_criteria:
            if word in set(product["description"].lower().split()):
                score+=1
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final
def score_appliances(product,count):
    score =common_attributes_score(product,count)
    desc_criteria=["name","Refrigerator", "Freezer", "Oven", "Microwave", "Stove", "Cooktop", "Range", "Dishwasher", "Washer", 
    "Dryer", "Vacuum", "Blender", "Toaster", "Coffee", "Kettle", "Mixer", "Juicer", 
    "Cooker", "Purifier", "Humidifier", "Heater", "Fan", "Sewing", "Iron", "Disposal", 
    "Dispenser", "Purifier", "Cooler", "Fridge", "Cleaner", "Washer", "Timer", "Strip", "Protector", 
    "Cord", "Adapter", "Converter", "Thermostat", "Detector", "Extinguisher", "Blanket", "Kit",
    "Grill", "Fryer", "Steamer", "Dehydrator", "Purifier", "Sewing", "Disposal", "Heater", "Fan", 
    "Conditioner", "Cooler", "Cleaner", "Vacuum", "Extractor", "Chopper", "Fuser", "Dispenser", "Polisher", 
    "Sweeper", "Mop", "Washer", "Filter", "Timer", "Adapter", "Converter", "Thermostat", "Detector", 
    "Extinguisher", "Blanket", "Kit", "Slicer", "Extractor", "Grinder", "Squeezer", "Press", "Extractor", 
    "Steamer", "Sterilizer", "Deodorizer", "Airpot", "Roaster", "Extractor", "Sterilizer", "Warmer", "Holder", 
    "Organizer", "Masher", "Chopper", "Extractor", "Press", "Processor", "Container", "Packer", "Dispenser", 
    "Organizer", "Holder", "Organizer", "Organizer", "Charger", "Controller", "Inverter", "Regulator", 
    "Adapter", "Converter", "Converter", "Detector", "Alert", "Siren", "Alarm", "Beacon", "Lamp", "Bulb", 
    "Light", "Flashlight", "Torch", "Lantern", "Glow", "Glimmer", "Radiance", "Light", "Lamp"]
    if "category" in product and product["category"].lower()=="appliances":
        score+=4
        for word in desc_criteria:
            if word in set(product["description"].lower().split()):
                score+=1
    total = len(desc_criteria)+10
    final = scale(total,score)
    return final

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


def extract_product_info(data):
    products = []
    current_product = None
    count = 0
    for item in data:
        current_product = {"category": "", "name": item, "description": "", "price": ""}
        
        current_product["category"] = item.strip()
        if item.startswith("RRP") or "price" in item.lower():
            match = re.search(r'\d+', item)
            if match:
                current_product["price"] = match.group()
        else:
            if current_product:
                current_product["description"] += item + " "
                count += 1
    if current_product:
        products.append(current_product)

    return products, count

def print_product_info(product, category, count):
    if product:
        product_score = calculate_score(product, category, count)
        return f"Category: {category}, Score: {product_score}"


def process_category(pdf_path, json_path, selected_category):
    if not selected_category:
        return "Could not detect the category."

    text_content = extract_text_from_pdf(pdf_path)
    final_txt = convert_txt(text_content)
    data = load_json(json_path)
    category = selected_category.lower()

    if category:
        products, count = extract_product_info(data)
        scoring_results = []
        for product in products:
            product["category"] = category
            result = print_product_info(product, category, count)
            scoring_results.append(result)
        return scoring_results
    else:
        return "Could not detect the category."
st.markdown("<h1 style='text-align: center;'>Apprevexus</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;'>Catalogue Score Calculator </h1>", unsafe_allow_html=True)
with st.expander("Team Apprevexus"):
        st.info("""Kshitiz, Parth, Kartik, Shivain""")

#image_path = "https://static.vecteezy.com/system/resources/thumbnails/007/852/290/small/modern-wave-background-with-a-geometric-line-pattern-overlay-minimalist-smooth-curve-shapes-illustration-design-vector.jpg"
set_background_image()

def save_to_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Spinner for selecting categories
selected_category = st.selectbox("Select Category", ["Electronics","Cosmetics","Sports","Grocery","Apparel",
"Appliances", 
"Jewelry",
"Books",
"Tools",
"Medicine",
"Office Supplies",
"Home and decor"])

    # File uploader
uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])


json_file_path = "extracted_text.json"
    # Button to trigger scoring
if uploaded_file is not None:
        st.write("PDF file uploaded successfully!")

        # Extract text from PDF
        text = extract_text_from_pdf(uploaded_file)

        # Save extracted text to JSON file
        if st.button("Save to JSON"):
            json_data = {"text": text}
            json_file_path = "extracted_text.json"
            save_to_json(json_data, json_file_path)
            st.success(f"Text saved to {json_file_path}")


        if os.path.exists(json_file_path):
            if st.button("Score"):
                result = process_category(uploaded_file, json_file_path, selected_category)
                print(result)
                st.write("Scoring Result:")
                for res in result:
                    st.write(res)

        else:
            st.write("Please convert to json first")
                
else:
    st.write("Please upload a file first")

