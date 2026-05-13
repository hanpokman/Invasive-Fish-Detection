# DOUBLE CLICK ME - creates the fish database

import json
import os

# create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

fish_database = {
    "Bluegill": {
        "avg_length_cm": 20.0,
        "invasive": False,
        "common_names": ["sunfish", "bream"],
        "region": "North America",
        "color": "blue/green with orange belly",
        "danger_level": "none",
        "description": "Common native sunfish, harmless"
    },
    "Largemouth Bass": {
        "avg_length_cm": 38.0,
        "invasive": False,
        "common_names": ["bass", "green bass", "bucketmouth"],
        "region": "North America",
        "color": "green with dark horizontal stripe",
        "danger_level": "low",
        "description": "Popular sport fish, native to North America"
    },
    "Northern Snakehead": {
        "avg_length_cm": 45.0,
        "invasive": True,
        "common_names": ["snakehead", "frankenfish", "changsha"],
        "region": "Asia (invasive in US)",
        "color": "brown with snake-like pattern",
        "danger_level": "high",
        "description": "Highly invasive, can breathe air and walk on land!"
    },
    "Lionfish": {
        "avg_length_cm": 30.0,
        "invasive": True,
        "common_names": ["zebra fish", "turkey fish", "red lionfish"],
        "region": "Indo-Pacific (invasive in Atlantic)",
        "color": "red/white stripes with venomous spines",
        "danger_level": "high",
        "description": "Venomous spines, destroying Atlantic reef ecosystems"
    },
    "Asian Carp": {
        "avg_length_cm": 70.0,
        "invasive": True,
        "common_names": ["silver carp", "bighead carp", "flying carp"],
        "region": "Asia (invasive in US rivers)",
        "color": "silver/grey",
        "danger_level": "medium",
        "description": "Jumps out of water when boats pass, outcompetes natives"
    },
    "Rainbow Trout": {
        "avg_length_cm": 40.0,
        "invasive": False,
        "common_names": ["steelhead", "rainbow"],
        "region": "North America",
        "color": "silver with pink/red stripe",
        "danger_level": "none",
        "description": "Popular game fish, native to Pacific coast"
    },
    "Round Goby": {
        "avg_length_cm": 12.0,
        "invasive": True,
        "common_names": ["goby", "neogobius"],
        "region": "Eurasia (invasive in Great Lakes)",
        "color": "brown/grey with black spot",
        "danger_level": "medium",
        "description": "Small but aggressive, eats native fish eggs"
    },
    "Smallmouth Bass": {
        "avg_length_cm": 35.0,
        "invasive": False,
        "common_names": ["smallie", "bronzeback"],
        "region": "North America",
        "color": "bronze/brown with vertical bars",
        "danger_level": "low",
        "description": "Native bass species, great fighter"
    },
    "Sea Lamprey": {
        "avg_length_cm": 50.0,
        "invasive": True,
        "common_names": ["lamprey eel", "jawless fish"],
        "region": "Atlantic (invasive in Great Lakes)",
        "color": "eel-like with sucker mouth",
        "danger_level": "high",
        "description": "Parasitic, attaches to native fish and sucks blood"
    }
}

# save to file
with open("data/fish_database.json", "w") as f:
    json.dump(fish_database, f, indent=2)

print("✅ Fish database created at data/fish_database.json")
print(f"📊 Loaded {len(fish_database)} fish species")
print("\nSpecies in database:")
for i, species in enumerate(fish_database.keys(), 1):
    invasive_marker = "🚨 INVASIVE" if fish_database[species]["invasive"] else "✅ Native"
    print(f"  {i}. {species} ({invasive_marker})")

input("\nPress Enter to exit...")