import os
from django.core.files import File
from cropapp.models import CropDetail

BASE_IMAGE_PATH = 'media/crop_images/'

CROPS = [
    {
        "name": "rice",
        "description": "A staple grain crop grown widely in warm, wet environments.",
        "image": "rice.jpg",
        "best_season": "Kharif (June to October)",
        "common_pests_diseases": "Stem borer, rice blast, brown spot",
        "recommended_fertilizer": "Urea, DAP, MOP"
    },
    {
        "name": "maize",
        "description": "A cereal crop used for food and fodder.",
        "image": "maize.jpg",
        "best_season": "Kharif or Rabi",
        "common_pests_diseases": "Stem borers, fall armyworm",
        "recommended_fertilizer": "NPK (20:20:0), Urea"
    },
    {
        "name": "chickpea",
        "description": "A legume crop rich in protein, usually grown in dry regions.",
        "image": "chickpea.jpg",
        "best_season": "Rabi (October to February)",
        "common_pests_diseases": "Pod borer, Fusarium wilt",
        "recommended_fertilizer": "Super phosphate, Rhizobium culture"
    },
    {
        "name": "kidneybeans",
        "description": "Popular pulses known for their kidney-like shape.",
        "image": "kidneybeans.jpg",
        "best_season": "Rabi or Zaid",
        "common_pests_diseases": "Rust, aphids, leaf spot",
        "recommended_fertilizer": "NPK, FYM, DAP"
    },
    {
        "name": "pigeonpeas",
        "description": "Leguminous crop grown mainly in semi-arid regions.",
        "image": "pigeonpeas.jpg",
        "best_season": "Kharif",
        "common_pests_diseases": "Wilt, pod fly, leaf hopper",
        "recommended_fertilizer": "Rhizobium, SSP"
    },
    {
        "name": "mothbeans",
        "description": "Drought-resistant legume grown in arid areas.",
        "image": "mothbeans.jpg",
        "best_season": "Kharif",
        "common_pests_diseases": "Pod borers, leaf curl",
        "recommended_fertilizer": "FYM, Rhizobium culture"
    },
    {
        "name": "mungbean",
        "description": "Commonly used pulse in South Asia, rich in protein.",
        "image": "mungbean.jpg",
        "best_season": "Kharif or Summer",
        "common_pests_diseases": "Yellow mosaic, aphids",
        "recommended_fertilizer": "SSP, Rhizobium inoculant"
    },
    {
        "name": "blackgram",
        "description": "Important pulse crop, source of protein and iron.",
        "image": "blackgram.jpg",
        "best_season": "Kharif and Rabi",
        "common_pests_diseases": "Root rot, leaf spot",
        "recommended_fertilizer": "FYM, SSP, Rhizobium"
    },
    {
        "name": "lentil",
        "description": "Cool-season legume rich in protein and iron.",
        "image": "lentil.jpg",
        "best_season": "Rabi",
        "common_pests_diseases": "Wilt, rust, aphids",
        "recommended_fertilizer": "NPK, SSP, Rhizobium"
    },
    {
        "name": "pomegranate",
        "description": "Fruit crop with high antioxidant content.",
        "image": "pomegranate.jpg",
        "best_season": "July to September",
        "common_pests_diseases": "Fruit borer, leaf spot",
        "recommended_fertilizer": "FYM, Potash, Urea"
    },
    {
        "name": "banana",
        "description": "Tropical fruit grown year-round in humid climates.",
        "image": "banana.jpg",
        "best_season": "Year-round",
        "common_pests_diseases": "Panama disease, banana weevil",
        "recommended_fertilizer": "NPK, Urea, Compost"
    },
    {
        "name": "mango",
        "description": "Popular tropical fruit grown in summer.",
        "image": "mango.jpg",
        "best_season": "Spring-Summer",
        "common_pests_diseases": "Powdery mildew, fruit fly",
        "recommended_fertilizer": "FYM, Potassium, Urea"
    },
    {
        "name": "grapes",
        "description": "Fruit crop grown in dry temperate regions.",
        "image": "grapes.jpg",
        "best_season": "November to January",
        "common_pests_diseases": "Downy mildew, mealy bugs",
        "recommended_fertilizer": "Phosphorous, Potash"
    },
    {
        "name": "watermelon",
        "description": "Summer fruit with high water content.",
        "image": "watermelon.jpg",
        "best_season": "Summer (March to June)",
        "common_pests_diseases": "Fruit fly, powdery mildew",
        "recommended_fertilizer": "NPK, Cow dung manure"
    },
    {
        "name": "muskmelon",
        "description": "Aromatic summer fruit grown in dry climates.",
        "image": "muskmelon.jpg",
        "best_season": "Summer (March to June)",
        "common_pests_diseases": "Red pumpkin beetle, aphids",
        "recommended_fertilizer": "Compost, Urea"
    },
    {
        "name": "apple",
        "description": "Temperate fruit grown in cold regions.",
        "image": "apple.jpg",
        "best_season": "Spring (flowering) to Autumn (harvest)",
        "common_pests_diseases": "Scab, apple aphid",
        "recommended_fertilizer": "Potash, Superphosphate"
    },
    {
        "name": "orange",
        "description": "Citrus fruit rich in vitamin C.",
        "image": "orange.jpg",
        "best_season": "Winter (November to January)",
        "common_pests_diseases": "Citrus canker, aphids",
        "recommended_fertilizer": "Compost, NPK"
    },
    {
        "name": "papaya",
        "description": "Fast-growing fruit crop with high nutritional value.",
        "image": "papaya.jpg",
        "best_season": "Summer or Spring",
        "common_pests_diseases": "Mosaic virus, aphids",
        "recommended_fertilizer": "Cow dung, Urea"
    },
    {
        "name": "coconut",
        "description": "Tropical palm crop for oil and water.",
        "image": "coconut.jpg",
        "best_season": "Summer or Monsoon",
        "common_pests_diseases": "Rhinoceros beetle, red palm weevil",
        "recommended_fertilizer": "Neem cake, Super phosphate"
    },
    {
        "name": "cotton",
        "description": "Fiber crop used in textile industry.",
        "image": "cotton.jpg",
        
        "best_season": "Kharif",
        "common_pests_diseases": "Bollworm, aphids",
        "recommended_fertilizer": "Potash, DAP"
    },
    {
        "name": "jute",
        "description": "Bast fiber crop used for making sacks and ropes.",
        "image": "jute.jpg",

        "best_season": "Monsoon",
        "common_pests_diseases": "Stem rot, pests",
        "recommended_fertilizer": "Urea, Phosphate"
    },
    {
        "name": "coffee",
        "description": "Commercial beverage crop grown in hilly areas.",
        "image": "coffee.jpg",
        "best_season": "June to September",
        "common_pests_diseases": "Berry borer, leaf rust",
        "recommended_fertilizer": "Potassium sulfate, FYM"
    }
]

def populate():
    for crop in CROPS:
        image_path = os.path.join(BASE_IMAGE_PATH, crop["image"])
        if not os.path.exists(image_path):
            print(f"Image not found for {crop['name']} at {image_path}")
            continue

        with open(image_path, 'rb') as img_file:
            image_file = File(img_file)
            obj, created = CropDetail.objects.get_or_create(
                name=crop["name"],
                defaults={
                    "description": crop["description"],
                    "best_season": crop["best_season"],
                    "common_pests_diseases": crop["common_pests_diseases"],
                    "recommended_fertilizer": crop["recommended_fertilizer"]
                }
            )
            if created:
                obj.image.save(crop["image"], image_file, save=True)
                print(f"✔ Created: {crop['name']}")
            else:
                print(f"⚠ Already exists: {crop['name']}")
