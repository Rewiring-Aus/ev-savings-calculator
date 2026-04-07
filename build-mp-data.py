#!/usr/bin/env python3
"""Build mp-data.json from AEC electorates data."""
import json, urllib.request

url = "https://raw.githubusercontent.com/pmcau/AustralianElectorates/main/Data/electorates.json"
data = json.loads(urllib.request.urlopen(url).read())

# Build postcode -> electorates
pc_map = {}
for elec in data:
    if not elec.get('Exist2025'):
        continue
    name = elec['Name']
    for loc in elec.get('Locations', []):
        pc = str(loc['Postcode'])
        if pc not in pc_map:
            pc_map[pc] = []
        if name not in pc_map[pc]:
            pc_map[pc].append(name)

for pc in pc_map:
    pc_map[pc].sort()

# MP data (48th Parliament, 2025-2028)
mps = {
    "Adelaide":"Steve Georganas","Aston":"Mary Doyle","Ballarat":"Catherine King",
    "Banks":"Zhi Soon","Barker":"Tony Pasin","Barton":"Ash Ambihaipahar",
    "Bass":"Jess Teesdale","Bean":"David Smith","Bendigo":"Lisa Chesters",
    "Bennelong":"Jerome Laxale","Berowra":"Julian Leeser","Blair":"Shayne Neumann",
    "Blaxland":"Jason Clare","Bonner":"Kara Cook","Boothby":"Louise Miller-Frost",
    "Bowman":"Henry Pike","Braddon":"Anne Urquhart","Bradfield":"Nicolette Boele",
    "Brand":"Madeleine King","Brisbane":"Madonna Jarrett","Bruce":"Julian Hill",
    "Bullwinkel":"Trish Cook","Burt":"Matt Keogh","Calare":"Andrew Gee",
    "Calwell":"Basem Abdo","Canberra":"Alicia Payne","Canning":"Andrew Hastie",
    "Capricornia":"Michelle Landry","Casey":"Aaron Violi","Chifley":"Ed Husic",
    "Chisholm":"Carina Garland","Clark":"Andrew Wilkie","Cook":"Simon Kennedy",
    "Cooper":"Ged Kearney","Corangamite":"Libby Coker","Corio":"Richard Marles",
    "Cowan":"Anne Aly","Cowper":"Pat Conaghan","Cunningham":"Alison Byrnes",
    "Curtin":"Kate Chaney","Dawson":"Andrew Willcox","Deakin":"Matt Gregg",
    "Dickson":"Ali France","Dobell":"Emma McBride","Dunkley":"Jodie Belyea",
    "Durack":"Melissa Price","Eden-Monaro":"Kristy McBain","Fadden":"Cameron Caldwell",
    "Fairfax":"Ted O'Brien","Farrer":"Sussan Ley","Fenner":"Andrew Leigh",
    "Fisher":"Andrew Wallace","Flinders":"Zoe McKenzie","Flynn":"Colin Boyce",
    "Forde":"Rowan Holzberger","Forrest":"Ben Small","Fowler":"Dai Le",
    "Franklin":"Julie Collins","Fraser":"Daniel Mulino","Fremantle":"Josh Wilson",
    "Gellibrand":"Tim Watts","Gilmore":"Fiona Phillips","Gippsland":"Darren Chester",
    "Goldstein":"Tim Wilson","Gorton":"Alice Jordan-Baird","Grayndler":"Anthony Albanese",
    "Greenway":"Michelle Rowland","Grey":"Tom Venning","Griffith":"Renee Coffey",
    "Groom":"Garth Hamilton","Hasluck":"Tania Lawrence","Hawke":"Sam Rae",
    "Herbert":"Phillip Thompson","Hindmarsh":"Mark Butler","Hinkler":"David Batt",
    "Holt":"Cassandra Fernando","Hotham":"Clare O'Neil","Hughes":"David Moncrieff",
    "Hume":"Angus Taylor","Hunter":"Dan Repacholi","Indi":"Helen Haines",
    "Isaacs":"Mark Dreyfus","Jagajaga":"Kate Thwaites","Kennedy":"Bob Katter",
    "Kingsford Smith":"Matt Thistlethwaite","Kingston":"Amanda Rishworth",
    "Kooyong":"Monique Ryan","La Trobe":"Jason Wood","Lalor":"Joanne Ryan",
    "Leichhardt":"Matt Smith","Lilley":"Anika Wells","Lindsay":"Melissa McIntosh",
    "Lingiari":"Marion Scrymgour","Longman":"Terry Young","Lyne":"Alison Penfold",
    "Macarthur":"Mike Freelander","Mackellar":"Sophie Scamps","Macnamara":"Josh Burns",
    "Macquarie":"Susan Templeman","Makin":"Tony Zappia","Mallee":"Anne Webster",
    "Maranoa":"David Littleproud","Maribyrnong":"Jo Briskey","Mayo":"Rebekha Sharkie",
    "McEwen":"Rob Mitchell","McMahon":"Chris Bowen","McPherson":"Leon Rebello",
    "Melbourne":"Sarah Witty","Menzies":"Gabriel Ng","Mitchell":"Alex Hawke",
    "Monash":"Mary Aldred","Moncrieff":"Angie Bell","Moore":"Tom French",
    "Moreton":"Julie-Ann Campbell","Newcastle":"Sharon Claydon",
    "New England":"Barnaby Joyce","Nicholls":"Sam Birrell","O'Connor":"Rick Wilson",
    "Oxley":"Milton Dick","Page":"Kevin Hogan","Parkes":"Jamie Chaffey",
    "Parramatta":"Andrew Charlton","Paterson":"Meryl Swanson","Pearce":"Tracey Roberts",
    "Perth":"Patrick Gorman","Petrie":"Emma Comer","Rankin":"Jim Chalmers",
    "Reid":"Sally Sitou","Richmond":"Justine Elliot","Riverina":"Michael McCormack",
    "Robertson":"Gordon Reid","Ryan":"Elizabeth Watson-Brown","Scullin":"Andrew Giles",
    "Shortland":"Pat Conroy","Solomon":"Luke Gosling","Spence":"Matt Burnell",
    "Sturt":"Claire Clutterham","Swan":"Zaneta Mascarenhas","Sydney":"Tanya Plibersek",
    "Tangney":"Sam Lim","Wannon":"Dan Tehan","Warringah":"Zali Steggall",
    "Watson":"Tony Burke","Wentworth":"Allegra Spender","Werriwa":"Anne Stanley",
    "Whitlam":"Carol Berry","Wide Bay":"Llew O'Brien","Wills":"Peter Khalil",
    "Wright":"Scott Buchholz","Lyons":"Rebecca White",
}

def make_email(name):
    parts = name.lower().split()
    first = parts[0]
    last = '.'.join(parts[1:])  # handles multi-word last names
    return f"{first}.{last}.mp@aph.gov.au"

special_emails = {
    "Ted O'Brien": "ted.o'brien.mp@aph.gov.au",
    "Llew O'Brien": "llew.o'brien.mp@aph.gov.au",
    "Clare O'Neil": "clare.o'neil.mp@aph.gov.au",
    "Elizabeth Watson-Brown": "elizabeth.watson-brown.mp@aph.gov.au",
    "Louise Miller-Frost": "louise.miller-frost.mp@aph.gov.au",
    "Alice Jordan-Baird": "alice.jordan-baird.mp@aph.gov.au",
    "Julie-Ann Campbell": "julie-ann.campbell.mp@aph.gov.au",
}

elec_data = {}
for elec, mp in mps.items():
    email = special_emails.get(mp, make_email(mp))
    elec_data[elec] = {"mp": mp, "email": email}

# Check coverage
missing = set()
for pc, elecs in pc_map.items():
    for e in elecs:
        if e not in elec_data:
            missing.add(e)
if missing:
    print(f"WARNING: Missing MP data for: {missing}")

out = {"pcToElec": pc_map, "elecToMp": elec_data}
with open('mp-data.json', 'w') as f:
    json.dump(out, f, separators=(',', ':'))

import os
print(f"mp-data.json: {os.path.getsize('mp-data.json')//1024}KB")
print(f"Postcodes: {len(pc_map)}, Electorates: {len(elec_data)}")
