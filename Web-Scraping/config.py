import pandas as pd
import numpy as np
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import time

base_directory = os.getcwd()

# from standard_charted_bank import *
pd.set_option("display.max_colwidth", 200)
columns_to_use = [
    "Bank Name",
    "Merchant Name",
    "Link to offer on Bank site (for reference)",
    "Category",
    "Offer title (if available)",
    "Start date",
    "End date",
    "Detailed offer text (if available)",
    "Logo link",
    "Offer image",
    "Redeem link",
    "Promo code (if available)",
    "Online/ Offline",
    "If offline, cities",
]
columns_to_use = [
    "Bank Name",
    "Merchant Name",
    "Link to offer on Bank site (for reference)",
    "Category",
    "Offer title (if available)",
    "Start date",
    "End date",
    "Detailed offer text (if available)",
    "Logo link",
    "Offer image",
    "Redeem link",
    "Promo code (if available)",
    "Online/ Offline",
    "If offline, cities",
]
brand_category_dict = {
    "Netmeds": "Healthcare", 
    "Tata 1mg": "Healthcare", 
    "Via.Com": "Travel", 
    "Myntra": "Fashion", 
    "ITC Store": "Retail", 
    "Fabhotels": "Hospitality", 
    "Onefinerate.Com": "Travel",
    "Ferns N Petals": "Gifts",
    "Ferns and Petals": "Gifts",
    "Beardo": "Personal Care", 
    "Thrive Co": "Health & Wellness", 
    "Lee": "Fashion", 
    "Ixigo": "Travel", 
    "Behrouz Biryani": "Food", 
    "Faasos": "Food",
    "St. Botanica": "Personal Care", 
    "Thyrocare": "Healthcare", 
    "Candy Floss": "Food", 
    "Myglamm": "Beauty", 
    "Sweet Truth": "Food", 
    "Rapido": "Transportation", 
    "Kalki Fashion": "Fashion",
    "Lifestyle": "Retail",
    "Firangi Bake": "Food",
    "The Good Bowl": "Food",
    "The Lunch Box": "Food",
    "Oven Story": "Food",
    "Eatsure": "Food",
    "Eat Sure":"Food",
    "Slay Coffee": "Food & Beverage",
    "Arata": "Personal Care",
    "Boheco Life": "Health & Wellness",
    "Healthkart": "Health & Fitness",
    "Pee Safe": "Personal Care",
    "Cityfurnish": "Furniture",
    "Daily Objects": "Accessories",
    "Matrix (Sim Cards)": "Telecommunications",
    "Matrix (Travel Insurance)": "Insurance",
    "Hype": "Fashion",
    "Fastrack": "Fashion",
    "Titan": "Fashion",
    "McCaffeine": "Personal Care",
    "Zingbus": "Transportation",
    "My Fitness": "Health & Fitness",
    "Macv": "Fashion",
    "Body Cupid": "Personal Care",
    "Wow Skin": "Personal Care",
    "Abhibus": "Transportation",
    "Lo Foods": "Food",
    "Fast&Up": "Health & Wellness",
    "Holiday Of Dreams": "Travel",
    "Igp": "Gifts",
    "Kidzania": "Entertainment",
    "Stayvista": "Hospitality",
    "Beyoung": "Fashion",
    "Mommypure": "Personal Care",
    "Leaf Studios": "Electronics",
    "Edureka": "Education",
    "Giva": "Gifts",
    "Zouk": "Fashion",
    "Medibuddy": "Healthcare",
    "Skullcandy": "Electronics",
    "Indus Health Plus": "Healthcare",
    "Khadi Naturals": "Personal Care",
    "Atulya Herbals": "Personal Care",
    "Tangyoak": "Food",
    "Desi Toys": "Toys & Games",
    "R For Rabbit": "Baby Products",
    "Clovia": "Fashion",
    "Kapiva": "Health & Wellness",
    "Rummy Circle": "Gaming",
    "Care Insurance": "Insurance",
    "Fitterfly": "Health & Wellness",
    "Sonata": "Fashion",
    "Uspa": "Fashion",
    "Nnnow": "Fashion",
    "Redcliffe Labs": "Healthcare",
    "Simple Skincare": "Personal Care",
    "Love, Beauty & Planet": "Personal Care",
    "Weber® – American Barbecue Grills And Accessories": "Home & Garden",
    "Musafir- Domestic Flight Bookings": "Travel",
    "Musafir-International Flight Bookings": "Travel",
    "Musafir-Dubai Visa": "Travel",
    "Ease My Trip": "Travel",
    "Acko Insurance": "Insurance",
    "Saffronstays": "Hospitality",
    "Yatra": "Travel",
    "Musafir": "Travel",
    "Sleepy Owl Coffee": "Food & Beverage",
    "Metro Shoes": "Fashion",
    "Mochi Shoes": "Fashion",
    "Imagicaa": "Entertainment",
    "Rideev": "Transportation",
    "Jaipur Rugs": "Home & Decor",
    "Celio": "Fashion",
    "Tattva Spa": "Health & Wellness",
    "Jar": "Home & Kitchen",
    "Find Your Happy Place": "Lifestyle",
    "Acnesquad": "Personal Care",
    "Livspace": "Home & Decor",
    "The Man Company": "Personal Care",
    "Muscletech": "Health & Fitness",
    "Cloudtailor": "Fashion",
    "Gaana Plus": "Entertainment",
    "Max Online (Offer 1)": "Retail",
    "Homecentre (Offer 1)": "Home & Decor",
    "Lenovo (Offer 1)": "Electronics",
    "Lenovo (Offer 2)": "Electronics",
    "Boat": "Electronics",
    "Jivisa": "Fashion",
    "Tupperware": "Kitchenware",
    "Wendy'S": "Food",
    "Max Online (Offer 2)": "Retail",
    "Koskii": "Fashion",
    "Knowledge Hut": "Education",
    "Woggles": "Fashion",
    "Happinetz": "Entertainment",
    "Salty": "Food",
    "Plum (Offer 1)": "Beauty",
    "Plum (Offer 2)": "Beauty",
    "Snitch (Offer 2)": "Fashion",
    "Meolaa": "Fashion",
    "Arrow": "Fashion",
    "Flying Machine": "Fashion",
    "Aeropostale": "Fashion",
    "Donuts": "Food",
    "Ruggers": "Fashion",
    "Colt": "Fashion",
    "Karigari": "Home & Decor",
    "Anahi": "Fashion",
    "Sugr": "Food",
    "Homcentre (Offer 2)": "Home & Decor",
    "Happilo": "Food",
    "Myntra (Offer 1)": "Fashion",
    "Myntra (Offer 2)": "Fashion",
    "Myntra (Offer 3)": "Fashion",
    "Codingal": "Education",
    "The Moms Co": "Personal Care",
    "Mirraw": "Fashion",
    "Fable Street": "Fashion",
    "Pink Fort": "Fashion",
    "March Jewellery": "Jewelry",
    "Healthifyme": "Health & Fitness",
    "Nutrabay": "Health & Wellness",
    "Howard Johnson": "Hospitality",
    "Bhairavgarh Palace": "Hospitality",
    "Zooboo": "Entertainment",
    "Mojo Bar": "Food",
    "Rentomojo": "Rental Services",
    "Dot & Key": "Personal Care",
    "Mcdelivery (Offer 1)": "Food",
    "Mcdelivery (Offer 2)": "Food",
    "Mcdelivery (Offer 3)": "Food",
    "Mcdelivery (Offer 4)": "Food",
    "Bewakoof": "Fashion",
    "Zee5": "Entertainment",
    "Foxtale": "Entertainment",
    "Kiro Beauty": "Personal Care",
    "Juicy Chemistry": "Personal Care",
    "Amazon Shopping Voucher": "Retail",
    "Archies Gallery": "Gifts",
    "Armani Exchange-Luxe": "Fashion",
    "Aurelia": "Fashion",
    "Balenzia": "Fashion",
    "Bata": "Fashion",
    "Bluestone Diamond": "Jewelry",
    "Bluestone Gold Jewellery": "Jewelry",
    "Bobbi Brown": "Beauty",
    "Brooks Brothers -Luxe": "Fashion",
    "Campus": "Fashion",
    "Candere Diamond Jewellery": "Jewelry",
    "Candere Gold Jewellery": "Jewelry",
    "Chumbak": "Lifestyle",
    "Decathlon": "Sports & Fitness",
    "Dune-Luxe": "Fashion",
    "Elleven": "Fashion",
    "Estele": "Fashion",
    "Euphoria Jewellery Gold Coin": "Jewelry",
    "Euphoria Jewellery Silver Coin": "Jewelry",
    "Fabindia": "Fashion",
    "Fashion Factory": "Fashion",
    "Fastrack Bags": "Fashion",
    "Flipkart": "Retail",
    "Freecultr": "Fashion",
    "G-Star-Luxe": "Fashion",
    "Gas-Luxe": "Fashion",
    "Gini & Jony": "Kids",
    "Grt Jewellers": "Jewelry",
    "Hamleys-Luxe": "Toys & Games",
    "Helios": "Fashion",
    "Hidesign": "Fashion",
    "Hush Puppies": "Fashion",
    "Jack & Jones": "Fashion",
    "Jockey": "Fashion",
    "Kalyan Diamond Jewellery": "Jewelry",
    "Kalyan Gold Jewellery": "Jewelry",
    "Ketan Diamonds Gold Coin": "Jewelry",
    "Kiehls": "Beauty",
    "Levis": "Fashion",
    "Lifestyle Online": "Retail",
    "Love Beauty & Planet": "Personal Care",
    "Luxe": "Gifts",
    "Max": "Fashion",
    "Max Online": "Fashion",
    "Mothercare-Luxe": "Kids",
    "Nykaa": "Beauty",
    "Nykaa Fashion": "Fashion",
    "Nykaa Man": "Fashion",
    "Only": "Fashion",
    "Pantaloons": "Fashion",
    "Pc Jeweller Diamond": "Jewelry",
    "Pc Jeweller Gold": "Jewelry",
    "Puma": "Fashion",
    "Relaxo": "Fashion",
    "Reliance Jewels": "Jewelry",
    "Reliance Smart": "Retail",
    "Reliance Smart Point": "Retail",
    "Reliance Trends": "Fashion",
    "Reliance Trends Footwear": "Fashion",
    "Replay- Luxe": "Fashion",
    "Shiv Naresh": "Fashion",
    "Shoppers Stop": "Retail",
    "Simple": "Personal Care",
    "Skechers": "Fashion",
    "Skinn": "Fashion",
    "Spencer'S Retail": "Retail",
    "Steve Madden-Luxe": "Fashion",
    "Superdry-Luxe": "Fashion",
    "Tata Cliq": "Fashion",
    "Tata Cliq Luxury": "Fashion",
    "Tata Cliq Palette": "Fashion",
    "Tego": "Fashion",
    "The Body Shop": "Beauty",
    "mCaffeine":"Beauty",
    "Snitch (Offer 1)":"Fashion",
    "The Raymond Shop": "Fashion",
    "Titan Minimals": "Fashion",
    "Unlimited": "Fashion",
    "V Mart": "Fashion",
    "Veromoda": "Fashion",
    "W": "Fashion",
    "Wildcraft": "Fashion",
    "William Penn": "Stationery",
    "Woodland": "Fashion",
    "American Tourister": "Fashion",
    "Assembly": "Fashion",
    "Fab Hotels": "Hospitality",
    "GoStops":"Hospitality",
    "Intermiles": "Travel",
    "Irctc": "Travel",
    "Makemytrip E-Pay": "Travel",
    "Makemytrip Holiday E-Pay": "Travel",
    "Makemytrip Hotel E-Pay": "Travel",
    "Ola Cabs": "Transportation",
    "Points For Good": "Rewards",
    "Samsonite": "Fashion",
    "Taj Experiences": "Hospitality",
    "Uber": "Transportation",
    "Yatra.Com": "Travel",
    "Amazon": "Retail",
    "Amazon Fresh": "Retail",
    "Apollo Pharmacy": "Healthcare",
    "Auric": "Fashion",
    "Avast": "Software",
    "Bakingo": "Food",
    "Bigbasket": "Food & Grocery",
    "Black + Decker": "Home & Garden",
    "Braingymjr": "Toys & Games",
    "Chicago Pizza": "Food",
    "Corseca": "Electronics",
    "Croma": "Electronics",
    "Discovery Plus": "Entertainment",
    "Docubay": "Entertainment",
    "Finusmart Easy Cash": "Finance",
    "Fitpass": "Health & Fitness",
    "Flower Aura": "Gifts",
    "Gnc": "Health & Wellness",
    "Hammer": "Fitness Equipment",
    "Healthians": "Healthcare",
    "Healthifyme Smart Plan": "Health & Fitness",
    "Hoichoi": "Entertainment",
    "Home Centre Online": "Home & Decor",
    "Mamaearth": "Personal Care",
    "Muthoot Gold Voucher": "Finance",
    "Mx Player": "Entertainment",
    "Myupchar Medicines": "Healthcare",
    "Organic India": "Health & Wellness",
    "Pvr": "Entertainment",
    "Renee Cosmetics": "Beauty",
    "Smile Foundation": "Charity",
    "Sonyliv": "Entertainment",
    "Superbottoms": "Baby Products",
    "Swiggy Money Voucher": "Food",
    "Swiss Beauty": "Beauty",
    "The Skin Story": "Beauty",
    "Veridicus": "Fashion",
    "Vrott": "Fashion",
    "Wonderchef": "Home & Kitchen",
    "Zomato": "Food",
    "Et Prime Subscription": "Subscription",
    "Barbeque Nation": "Food",
    "Baskin Robbins": "Food",
    "Beer Cafe": "Food & Beverage",
    "Cafe Delhi Heights": "Food & Beverage",
    "Costa Coffee": "Food & Beverage",
    "Domino'S Pizza": "Food",
    "Kfc": "Food",
    "Machaan": "Food",
    "Mainland China": "Food",
    "Oh! Calcutta": "Food",
    "Pizza Hut": "Food",
    "Sigree": "Food",
    "Sweet Bengal": "Food",
    "Tgif": "Food & Beverage",
    "Amazon Prime Membership": "Subscription",
    "dpauls travel & tours": "Travel",
    "home centre": "Home & Decor",
    "home stop": "Home & Decor",
    "kama ayurveda": "Health & Wellness",
    "more": "Retail",
    "prestige": "Home & Kitchen",
    "reliance jio mart": "Retail",
    "sleepwell": "Home & Decor",
    "truefitt & hill": "Personal Care",
    "reliance digital": "Electronics",
    "reliance my jio store": "Retail",
    "vijay sales": "Electronics"
}

secondary_brand_categories = {
    'Amazon': 'Online marketplace',
    'Archies Gallery': 'Specialty gift store',
    'Armani Exchange': 'Luxury clothing retailer',
    'Arrow': "Men's formal wear retailer",
    'Aurelia': "Women's ethnic wear boutique",
    'Balenzia': 'Socks and hosiery shop',
    'Bata': 'Footwear store',
    'Bewakoof': 'Casual apparel retailer',
    'Beyoung': 'Youth fashion store',
    'Bluestone Diamond': 'Online diamond jewelry boutique',
    'Bluestone Gold Jewellery': 'Online gold jewelry boutique',
    'Bobbi Brown': 'Cosmetic boutique',
    'Brooks Brothers': "Men's luxury fashion boutique",
    'Campus': 'College apparel store',
    'Candere Diamond Jewellery': 'Online diamond jewelry retailer',
    'Candere Gold Jewellery': 'Online gold jewelry retailer',
    'Celio': "Men's fashion boutique",
    'Chumbak': 'Quirky lifestyle products store',
    'Decathlon': 'Sporting goods retailer',
    'Dune': 'Luxury fashion boutique',
    'Elleven': "Women's fashion boutique",
    'Estele': "Women's apparel store",
    'Euphoria Jewellery Gold Coin': 'Gold coin jewelry retailer',
    'Euphoria Jewellery Silver Coin': 'Silver coin jewelry retailer',
    'Fabindia': 'Ethnic clothing and home decor store',
    'Fashion Factory': 'Fashion retailer',
    'Fastrack': 'Fashion accessories brand',
    'Fastrack Bags': 'Fashion bags brand',
    'Flipkart': 'Online marketplace',
    'Freecultr': 'Online fashion retailer',
    'G-Star-Luxe': 'Luxury fashion brand',
    'Gas-Luxe': 'Luxury fashion brand',
    'Gini & Jony': 'Kids fashion brand',
    'Giva': 'Gifts retailer',
    'Grt Jewellers': 'Jewelry retailer',
    'Hamleys-Luxe': 'Luxury toy store',
    'Helios': 'Fashion accessories store',
    'Hidesign': 'Fashion accessories brand',
    'Hush Puppies': 'Footwear brand',
    'Jack & Jones': 'Men’s clothing brand',
    'Jockey': 'Innerwear brand',
    'Kalyan Diamond Jewellery': 'Diamond jewelry retailer',
    'Kalyan Gold Jewellery': 'Gold jewelry retailer',
    'Ketan Diamonds Gold Coin': 'Gold coin retailer',
    'Kiehls': 'Beauty products brand',
    'Levis': 'Fashion apparel brand',
    'Lifestyle Online': 'Online retail store',
    'Love Beauty & Planet': 'Personal care products brand',
    'Luxe': 'Luxury gifts retailer',
    'Max': 'Fashion apparel retailer',
    'Max Online': 'Online fashion retailer',
    'Mothercare-Luxe': 'Luxury kid’s clothing brand',
    'Myntra': 'Online fashion retailer',
    'Nykaa': 'Beauty products retailer',
    'Nykaa Fashion': 'Fashion retailer',
    'Nykaa Man': 'Men’s grooming products retailer',
    'Only': 'Women’s clothing brand',
    'Pantaloons': 'Fashion apparel retailer',
    'Pc Jeweller Diamond': 'Diamond jewelry retailer',
    'Pc Jeweller Gold': 'Gold jewelry retailer',
    'Puma': 'Sportswear brand',
    'Relaxo': 'Footwear brand',
    'Reliance Jewels': 'Jewelry retailer',
    'Reliance Smart': 'Retail store',
    'Reliance Smart Point': 'Retail store',
    'Reliance Trends': 'Fashion retailer',
    'Reliance Trends Footwear': 'Footwear retailer',
    'Replay-Luxe': 'Luxury fashion brand',
    'Shiv Naresh': 'Sportswear brand',
    'Shoppers Stop': 'Retail store',
    'Simple': 'Personal care products brand',
    'Skechers': 'Footwear brand',
    'Skinn': 'Perfume brand',
    "Spencer'S Retail": 'Retail store',
    'Steve Madden-Luxe': 'Luxury fashion brand',
    'Superdry-Luxe': 'Luxury fashion brand',
    'Tata Cliq': 'Fashion retailer',
    'Tata Cliq Luxury': 'Luxury fashion retailer',
    'Tata Cliq Palette': 'Fashion retailer',
    'Tego': 'Fashion accessories brand',
    'The Body Shop': 'Beauty products retailer',
    'The Man Company': 'Personal care products brand',
    'The Raymond Shop': 'Fashion retailer',
    'Titan': 'Fashion accessories brand',
    'Titan Minimals': 'Fashion accessories brand',
    'Unlimited': 'Fashion retailer',
    'V Mart': 'Fashion apparel retailer',
    'Veromoda': 'Fashion apparel brand',
    'W': 'Women’s fashion brand',
    'Wildcraft': 'Outdoor gear brand',
    'William Penn': 'Stationery retailer',
    'Woggles': 'Fashion accessories brand',
    'Woodland': 'Footwear and outdoor gear brand',
    'American Tourister': 'Luggage brand',
    'Assembly': 'Fashion brand',
    'Fab Hotels': 'Hospitality brand',
    'Intermiles': 'Travel rewards program',
    'Irctc': 'Railway ticket booking platform',
    'Ixigo': 'Travel booking platform',
    'Makemytrip E-Pay': 'Travel booking platform',
    'Makemytrip Holiday E-Pay': 'Travel booking platform',
    'Makemytrip Hotel E-Pay': 'Travel booking platform',
    'Ola Cabs': 'Ride-hailing service',
    'Points For Good': 'Rewards program',
    'Samsonite': 'Fashion accessories brand',
    'Taj Experiences': 'Hospitality service',
    'Uber': 'Transportation service',
    'Yatra.Com': 'Travel booking platform',
    'Amazon Fresh': 'Online grocery delivery service',
    'Apollo Pharmacy': 'Healthcare retailer',
    'Auric': 'Fashion brand',
    'Avast': 'Software provider',
    'Bakingo': 'Food delivery service',
    'Bigbasket': 'Online food and grocery retailer',
    'Black + Decker': 'Home and garden tools brand',
    'Braingymjr': 'Toys and games retailer',
    'Chicago Pizza': 'Food delivery service',
    'Corseca': 'Electronics brand',
    'Croma': 'Electronics retailer',
    'Daily Objects': 'Fashion accessories brand',
    'Discovery Plus': 'Entertainment streaming platform',
    'Docubay': 'Entertainment streaming platform',
    'Ferns N Petals': 'Gifts retailer',
    'Finusmart Easy Cash': 'Finance service',
    'Fitpass': 'Health and fitness service',
    'Flower Aura': 'Gifts retailer',
    'Gnc': 'Health and wellness retailer',
    'Hammer': 'Fitness equipment brand',
    'Healthians': 'Healthcare service',
    'Healthifyme Smart Plan': 'Health and fitness service',
    'Healthkart': 'Health and fitness retailer',
    'Hoichoi': 'Entertainment streaming platform',
    'Home Centre Online': 'Home and decor retailer',
    'Igp': 'Gifts retailer',
    'Mamaearth': 'Personal care products brand',
    'Muthoot Gold': 'Finance service',
    'Mx Player': 'Entertainment streaming platform',
    'Myupchar Medicines': 'Healthcare retailer',
    'Organic India': 'Health and wellness brand',
    'Pvr': 'Entertainment service',
    'Renee Cosmetics': 'Beauty products brand',
    'Skullcandy': 'Electronics brand',
    'Smile Foundation': 'Charity organization',
    'Sonyliv': 'Entertainment streaming platform',
    'Superbottoms': 'Baby products brand',
    'Swiggy Money': 'Food delivery service',
    'Swiss Beauty': 'Beauty products brand',
    'The Skin Story': 'Beauty products brand',
    'Veridicus': 'Fashion brand',
    'Vrott': 'Fashion brand',
    'Wonderchef': 'Home and kitchen brand',
    'Zomato': 'Food delivery service',
    'Et Prime Subscription': 'Subscription service',
    'Zee5': 'Entertainment streaming platform',
    'Barbeque Nation': 'Food service',
    'Baskin Robbins': 'Food service',
    'Beer Cafe': 'Food and beverage service',
    'Cafe Delhi Heights': 'Food and beverage service',
    'Costa Coffee': 'Food and beverage service',
    "Domino's Pizza": 'Food delivery service',
    'Kfc': 'Food delivery service',
    'Machaan': 'Food service',
    'Mainland China': 'Food service',
    'Oh! Calcutta': 'Food service',
    'Pizza Hut': 'Food delivery service',
    'Sigree': 'Food service',
    'Sweet Bengal': 'Food service',
    'Tgif': 'Food and beverage service',
    'Amazon Prime Membership': 'Subscription service',
    'Dpauls Travel & Tours': 'Travel agency',
    'Home Centre': 'Home and decor retailer',
    'Home Stop': 'Home and decor retailer',
    'Kama Ayurveda': 'Health and wellness brand',
    'More': 'Retailer',
    'Prestige': 'Home and kitchen brand',
    'Reliance Jio Mart': 'Retailer',
    'Sleepwell': 'Home and decor brand',
    'Netmeds': 'Healthcare retailer',
    'Truefitt & Hill': 'Personal care brand',
    'Reliance Digital': 'Electronics retailer',
    'Reliance My Jio Store': 'Retailer',
    'Vijay Sales': 'Electronics retailer',
    'Beardo': 'Personal care brand',
    'St. Botanica': 'Personal care brand',
    'Thyrocare': 'Healthcare service',
    'Via.Com': 'Travel booking platform',
    'Behrouz Biryani': 'Food delivery service',
    'Thrive Co': 'Health and wellness service',
    'Tata 1Mg': 'Healthcare retailer',
    'Faasos': 'Food delivery service',
    'Sweet Truth': 'Food delivery service',
    'Onefinerate.Com': 'Travel booking platform',
    'Lee': 'Fashion brand',
    'Itc Store': 'Retailer',
    'Rapido': 'Transportation service',
    'Myglamm': 'Beauty products brand',
    'Candy Floss': 'Food service',
    'Fabhotels': 'Hospitality service',
    'Kalki Fashion': 'Fashion retailer',
    'Lifestyle': 'Retailer',
    'Firangi Bake': 'Food delivery service',
    'The Good Bowl': 'Food delivery service',
    'The Lunch Box': 'Food delivery service',
    'Oven Story': 'Food delivery service',
    'Eatsure': 'Food service',
    'Slay Coffee': 'Food and beverage service',
    'Ferns And Petals': 'Gifts retailer',
    'Arata': 'Personal care brand',
    'Boheco Life': 'Health and wellness brand',
    'Pee Safe': 'Personal care brand',
    'Cityfurnish': 'Furniture rental service',
    'Matrix (Sim Cards)': 'Telecommunications service',
    'Matrix (Travel Insurance)': 'Insurance service',
    'Hype': 'Fashion brand',
    'Gostops': 'Hospitality service',
    'Mcaffeine': 'Beauty products brand',
    'Zingbus': 'Transportation service',
    'My Fitness': 'Health and fitness service',
    'Macv': 'Fashion brand',
    'Body Cupid': 'Personal care brand',
    'Wow Skin': 'Personal care brand',
    'Abhibus': 'Transportation service',
    'Lo Foods': 'Food brand',
    'Fast&Up': 'Health and wellness brand',
    'Holiday Of Dreams': 'Travel service',
    'Kidzania': 'Entertainment venue',
    'Stayvista': 'Hospitality service',
    'Mommypure': 'Personal care brand',
    'Leaf Studios': 'Electronics brand',
    'Edureka': 'Education service',
    'Zouk': 'Fashion brand',
    'Medibuddy': 'Healthcare service',
    'Indus Health Plus': 'Healthcare service',
    'Khadi Naturals': 'Personal care brand',
    'Atulya Herbals': 'Personal care brand',
    'Tangyoak': 'Food brand',
    'Desi Toys': 'Toys and games retailer',
    'R For Rabbit': 'Baby products brand',
    'Clovia': 'Fashion brand',
    'Kapiva': 'Health and wellness brand',
    'Rummy Circle': 'Gaming platform',
    'Care Insurance': 'Insurance service',
    'Fitterfly': 'Health and wellness service',
    'Sonata': 'Fashion brand',
    'Uspa': 'Fashion brand',
    'Nnnow': 'Fashion retailer',
    'Redcliffe Labs': 'Healthcare service',
    'Simple Skincare': 'Personal care brand',
    'Love, Beauty & Planet': 'Personal care brand',
    'Weber® – American Barbecue Grills And Accessories': 'Home and garden brand',
    'Musafir- Domestic Flight Bookings': 'Travel booking service',
    'Musafir-International Flight Bookings': 'Travel booking service',
    'Musafir-Dubai Visa': 'Travel visa service',
    'Ease My Trip': 'Travel booking platform',
    'Acko Insurance': 'Insurance service',
    'Saffronstays': 'Hospitality service',
    'Yatra': 'Travel booking platform',
    'Musafir': 'Travel booking platform',
    'Sleepy Owl Coffee': 'Food and beverage brand',
    'Metro Shoes': 'Fashion brand',
    'Mochi Shoes': 'Fashion brand',
    'Imagicaa': 'Entertainment venue',
    'Rideev': 'Transportation service',
    'Jaipur Rugs': 'Home and decor brand',
    'Snitch': 'Fashion brand',
    'Tattva Spa': 'Health and wellness service',
    'Jar': 'Home and kitchen brand',
    'Find Your Happy Place': 'Lifestyle brand',
    'Acnesquad': 'Personal care brand',
    'Livspace': 'Home and decor service',
    'Muscletech': 'Health and fitness brand',
    'Cloudtailor': 'Fashion brand',
    'Gaana Plus': 'Entertainment streaming service',
    'Homecentre': 'Home and decor retailer',
    'Lenovo': 'Electronics brand',
    'Boat': 'Electronics brand',
    'Jivisa': 'Fashion brand',
    'Tupperware': 'Kitchenware brand',
    "Wendy's": 'Food service',
    'Koskii': 'Fashion brand',
    'Knowledge Hut': 'Education service',
    'Happinetz': 'Entertainment brand',
    'Salty': 'Food brand',
    'Plum': 'Beauty brand',
    'Meolaa': 'Fashion brand',
    'Flying Machine': 'Fashion brand',
    'Aeropostale': 'Fashion brand',
    'Donuts': 'Food service',
    'Ruggers': 'Fashion brand',
    'Colt': 'Fashion brand',
    'Karigari': 'Home and decor brand',
    'Anahi': 'Fashion brand',
    'Sugr': 'Food brand',
    'Homcentre': 'Home and decor brand',
    'Happilo': 'Food brand',
    'Codingal': 'Education service',
    'The Moms Co': 'Personal care brand',
    'Mirraw': 'Fashion brand',
    'Fable Street': 'Fashion brand',
    'Pink Fort': 'Fashion brand',
    'March Jewellery': 'Jewelry brand',
    'Healthifyme': 'Health and fitness service',
    'Nutrabay': 'Health and wellness brand',
    'Howard Johnson': 'Hospitality service',
    'Bhairavgarh Palace': 'Hospitality service',
    'Zooboo': 'Entertainment brand',
    'Mojo Bar': 'Food brand',
    'Rentomojo': 'Rental service',
    'Dot & Key': 'Personal care brand',
    'Mcdelivery': 'Food delivery service',
    'Foxtale': 'Entertainment brand',
    'Kiro Beauty': 'Personal care brand',
    'Juicy Chemistry': 'Personal care brand',
}



def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    else:
        return None
