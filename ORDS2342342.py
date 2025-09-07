import matplotlib.pyplot as plt

# Data
data = [
    {"SOLD_TO_PARTY": "BH_EQUINOR ASA", "TOTAL_ORDER_VOLUME": "32406363.58"},
    {"SOLD_TO_PARTY": "First Assembly of God", "TOTAL_ORDER_VOLUME": "6216957.81"},
    {"SOLD_TO_PARTY": "ABCX Health Insurance", "TOTAL_ORDER_VOLUME": "4722200"},
    {"SOLD_TO_PARTY": "Apple Inc", "TOTAL_ORDER_VOLUME": "1893804.14"},
    {"SOLD_TO_PARTY": "ATHENS, CITY OF", "TOTAL_ORDER_VOLUME": "410325"},
    {"SOLD_TO_PARTY": "Garyville Refinery", "TOTAL_ORDER_VOLUME": "379618.7"},
    {"SOLD_TO_PARTY": "The Rivers Hospital", "TOTAL_ORDER_VOLUME": "321790"},
    {"SOLD_TO_PARTY": "BlueStar Inc", "TOTAL_ORDER_VOLUME": "269996.22"},
    {"SOLD_TO_PARTY": "AVANTI PRODUCTS INC", "TOTAL_ORDER_VOLUME": "51940.06"},
    {"SOLD_TO_PARTY": "New Start Gyms", "TOTAL_ORDER_VOLUME": "44300"},
]

# Extracting data for plotting
parties = [item["SOLD_TO_PARTY"] for item in data]
volumes = [float(item["TOTAL_ORDER_VOLUME"]) for item in data]

# Colors for bars
colors = [
    "silver",
    "darksalmon",
    "peru",
    "burlywood",
    "goldenrod",
    "darkkhaki",
    "darkseagreen",
    "cadetblue",
    "cornflowerblue",
    "slateblue",
]

# Creating the bar graph
plt.figure(figsize=(10, 6))
bars = plt.bar(parties, volumes, color=colors)
plt.xlabel("SOLD TO PARTY")
plt.ylabel("TOTAL ORDER VOLUME")
plt.title("Total Order Volume by Sold To Party")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

# Saving the plot as a JPG file
plt.savefig("ORDI2342342.jpg")