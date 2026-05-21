import pandas as pd
import random

random.seed(42)

MALE_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard",
    "Joseph", "Thomas", "Charles", "Daniel", "Paul", "Mark", "Donald",
    "George", "Kenneth", "Steven", "Edward", "Brian", "Ronald", "Anthony",
    "Kevin", "Jason", "Matthew", "Gary", "Timothy", "Larry", "Jeffrey",
    "Frank", "Scott", "Eric", "Stephen", "Andrew", "Raymond", "Gregory",
    "Joshua", "Jerry", "Dennis", "Walter", "Harold",
]

FEMALE_NAMES = [
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth",
    "Susan", "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty",
    "Dorothy", "Sandra", "Ashley", "Donna", "Carol", "Ruth", "Sharon",
    "Michelle", "Laura", "Amanda", "Melissa", "Rebecca", "Virginia",
    "Kathleen", "Pamela", "Martha", "Debra", "Stephanie", "Carolyn",
    "Christine", "Marie", "Janet", "Catherine", "Frances", "Ann", "Joyce",
    "Diane",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Wilson", "Anderson", "Taylor", "Thomas", "Jackson", "White",
    "Harris", "Martin", "Thompson", "Martinez", "Robinson", "Clark",
    "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young",
    "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green",
    "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell",
    "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans",
    "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed",
    "Cook", "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper",
    "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray",
    "Ramirez", "Watson", "Brooks", "Kelly", "Sanders", "Price",
    "Bennett", "Wood", "Barnes", "Ross", "Henderson", "Coleman", "Jenkins",
    "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores", "Washington",
    "Butler", "Simmons", "Foster", "Bryant", "Alexander", "Russell",
    "Griffin", "Diaz", "Hayes",
]

FARM_PREFIXES = [
    "Sunrise", "Golden", "Green Valley", "Blue Ridge", "Prairie", "Timber Creek",
    "Clearwater", "Heartland", "Silver Creek", "Red Oak", "Maple Ridge",
    "Cedar", "Willow Springs", "Elk Creek", "Blue Sky", "Rolling Hills",
    "Morning Star", "Big Sky", "Whispering Pines", "Iron Creek",
    "Twin Oaks", "White Oak", "Black Creek", "Eagle Nest", "Hawk Ridge",
    "Bear Creek", "Deer Run", "Fox Hollow", "Turkey Creek", "Cottonwood",
    "Sycamore", "Hickory Hills", "Walnut Grove", "Plum Creek",
    "Sand Hill", "Rock River", "Stone Creek", "Long Prairie",
    "High Plains", "Wind River", "Sun Valley", "Meadow View", "Crest",
    "Summit", "Valley View", "River Bend", "Hilltop", "Lakeside",
    "Spring Creek", "Pinewood",
]

FARM_TYPES = [
    "Farm", "Farms", "Ranch", "Ranches", "Acres", "Agriculture",
    "Livestock", "Grain", "Operations", "Holdings", "Enterprises",
    "Organics", "Produce", "Family Farm", "Land & Cattle", "Crop Production",
]

LOCATIONS = [
    ("IA", "Boone", "50036"), ("IA", "Polk", "50309"), ("IA", "Linn", "52401"),
    ("IA", "Scott", "52801"), ("IA", "Black Hawk", "50701"), ("IA", "Story", "50011"),
    ("IA", "Dallas", "50263"), ("IA", "Johnson", "52240"), ("IA", "Dubuque", "52001"),
    ("IA", "Pottawattamie", "51501"),
    ("NE", "Lancaster", "68502"), ("NE", "Douglas", "68102"), ("NE", "Sarpy", "68005"),
    ("NE", "Hall", "68801"), ("NE", "Buffalo", "68802"), ("NE", "Dodge", "68025"),
    ("NE", "Madison", "68701"), ("NE", "Platte", "68601"), ("NE", "Dawson", "68840"),
    ("NE", "Lincoln", "69101"),
    ("KS", "Sedgwick", "67201"), ("KS", "Riley", "66502"), ("KS", "Douglas", "66044"),
    ("KS", "Shawnee", "66603"), ("KS", "Saline", "67401"), ("KS", "Reno", "67501"),
    ("KS", "Butler", "67042"), ("KS", "Ellis", "67601"), ("KS", "Finney", "67846"),
    ("KS", "Ford", "67801"),
    ("IL", "Champaign", "61820"), ("IL", "Sangamon", "62701"), ("IL", "Peoria", "61602"),
    ("IL", "Knox", "61401"), ("IL", "Macon", "62521"), ("IL", "Tazewell", "61554"),
    ("IL", "Will", "60432"), ("IL", "Kane", "60134"), ("IL", "Winnebago", "61101"),
    ("IL", "DeKalb", "60115"),
    ("MN", "Kandiyohi", "56201"), ("MN", "Stearns", "56301"), ("MN", "Olmsted", "55901"),
    ("MN", "Clay", "56560"), ("MN", "Otter Tail", "56537"), ("MN", "Crow Wing", "56401"),
    ("MN", "Rice", "55021"), ("MN", "Steele", "55060"), ("MN", "Waseca", "56093"),
    ("MN", "Sibley", "55338"),
    ("TX", "Lubbock", "79401"), ("TX", "Randall", "79106"), ("TX", "Potter", "79101"),
    ("TX", "Hale", "79072"), ("TX", "Floyd", "79235"), ("TX", "Swisher", "79095"),
    ("TX", "Castro", "79019"), ("TX", "Parmer", "79009"), ("TX", "Bailey", "79316"),
    ("TX", "Lamb", "79339"),
    ("OK", "Tulsa", "74103"), ("OK", "Cleveland", "73069"), ("OK", "Comanche", "73501"),
    ("OK", "Garfield", "73701"), ("OK", "Logan", "73044"), ("OK", "Grady", "73018"),
    ("OK", "Creek", "74066"), ("OK", "Pottawatomie", "74801"), ("OK", "Pontotoc", "74820"),
    ("OK", "Muskogee", "74401"),
    ("IN", "Tippecanoe", "47901"), ("IN", "Allen", "46802"), ("IN", "Hamilton", "46032"),
    ("IN", "Delaware", "47302"), ("IN", "Bartholomew", "47201"), ("IN", "Madison", "46001"),
    ("IN", "Hendricks", "46123"), ("IN", "Vigo", "47802"), ("IN", "Monroe", "47401"),
    ("IN", "Howard", "46901"),
    ("OH", "Wayne", "44691"), ("OH", "Holmes", "44654"), ("OH", "Knox", "43050"),
    ("OH", "Tuscarawas", "44663"), ("OH", "Stark", "44702"), ("OH", "Ashland", "44805"),
    ("OH", "Medina", "44256"), ("OH", "Licking", "43055"), ("OH", "Delaware", "43015"),
    ("OH", "Fairfield", "43130"),
    ("OR", "Marion", "97301"), ("OR", "Clackamas", "97045"), ("OR", "Lane", "97402"),
    ("OR", "Yamhill", "97128"), ("OR", "Polk", "97361"), ("OR", "Benton", "97330"),
    ("OR", "Tillamook", "97141"), ("OR", "Washington", "97006"), ("OR", "Clatsop", "97103"),
    ("OR", "Lincoln", "97365"),
    ("VA", "Augusta", "24401"), ("VA", "Shenandoah", "22657"), ("VA", "Page", "22835"),
    ("VA", "Clarke", "22611"), ("VA", "Frederick", "22601"), ("VA", "Warren", "22630"),
    ("VA", "Rappahannock", "22733"), ("VA", "Madison", "22727"), ("VA", "Greene", "22932"),
    ("VA", "Albemarle", "22902"),
]

# Generate 2000 background records
records = []
for i in range(2000):
    state, county, zip_code = random.choice(LOCATIONS)
    first = random.choice(MALE_NAMES + FEMALE_NAMES)
    last = random.choice(LAST_NAMES)
    prefix = random.choice(FARM_PREFIXES)
    ftype = random.choice(FARM_TYPES)
    records.append({
        "unique_id": i + 1,
        "farm_name": f"{prefix} {ftype}",
        "operator_first_name": first,
        "operator_last_name": last,
        "state": state,
        "county": county,
        "zip_code": zip_code,
    })

# Overwrite specific indices with carefully crafted duplicate pairs.
# unique_id = index + 1, so index 46 → unique_id 47, etc.
DUPLICATE_PAIRS = [
    # Pair 1 (Easy) — farm name singular/plural + nickname
    (46, {"farm_name": "Sunrise Valley Farm",   "operator_first_name": "Michael",  "operator_last_name": "Johnson",  "state": "KS", "county": "Saline",    "zip_code": "67401"}),
    (310, {"farm_name": "Sunrise Valley Farms", "operator_first_name": "Mike",     "operator_last_name": "Johnson",  "state": "KS", "county": "Saline",    "zip_code": "67401"}),

    # Pair 2 (Easy-Medium) — LLC suffix added + nickname
    (87,  {"farm_name": "Clearwater Ranch",     "operator_first_name": "Patricia", "operator_last_name": "Williams", "state": "OK", "county": "Garfield",  "zip_code": "73701"}),
    (440, {"farm_name": "Clearwater Ranch LLC", "operator_first_name": "Pat",      "operator_last_name": "Williams", "state": "OK", "county": "Garfield",  "zip_code": "73701"}),

    # Pair 3 (Medium) — "Agriculture" abbreviated to "Ag" + first-name initial only
    (132, {"farm_name": "Golden Acres Agriculture", "operator_first_name": "David", "operator_last_name": "Thompson", "state": "IL", "county": "Champaign", "zip_code": "61820"}),
    (600, {"farm_name": "Golden Acres Ag",          "operator_first_name": "D.",    "operator_last_name": "Thompson", "state": "IL", "county": "Champaign", "zip_code": "61820"}),

    # Pair 4 (Medium) — "Timber Creek" compounded to "Timbercreek" + nickname
    (200, {"farm_name": "Timber Creek Organics", "operator_first_name": "James", "operator_last_name": "Anderson", "state": "OR", "county": "Benton", "zip_code": "97330"}),
    (750, {"farm_name": "Timbercreek Organics",  "operator_first_name": "Jim",   "operator_last_name": "Anderson", "state": "OR", "county": "Benton", "zip_code": "97330"}),

    # Pair 5 (Hard) — plural "Winds" + nickname + zip off by 1
    (350, {"farm_name": "Prairie Wind Farm",  "operator_first_name": "Susan", "operator_last_name": "Martinez", "state": "NE", "county": "Hall", "zip_code": "68801"}),
    (820, {"farm_name": "Prairie Winds Farm", "operator_first_name": "Sue",   "operator_last_name": "Martinez", "state": "NE", "county": "Hall", "zip_code": "68802"}),

    # Pair 6 (Medium) — "Company" abbreviated to "Co" + nickname
    (500,  {"farm_name": "Heartland Grain Company", "operator_first_name": "William", "operator_last_name": "Wilson", "state": "MN", "county": "Kandiyohi", "zip_code": "56201"}),
    (1050, {"farm_name": "Heartland Grain Co",      "operator_first_name": "Bill",    "operator_last_name": "Wilson", "state": "MN", "county": "Kandiyohi", "zip_code": "56201"}),

    # Pair 7 (Hard) — single-character typo "Ridge"→"Rdge" + nickname
    (700,  {"farm_name": "Blue Ridge Livestock", "operator_first_name": "Elizabeth", "operator_last_name": "Garcia", "state": "VA", "county": "Augusta", "zip_code": "24401"}),
    (1400, {"farm_name": "Blue Rdge Livestock",  "operator_first_name": "Beth",      "operator_last_name": "Garcia", "state": "VA", "county": "Augusta", "zip_code": "24401"}),
]

for idx, fields in DUPLICATE_PAIRS:
    records[idx].update(fields)

df = pd.DataFrame(records)