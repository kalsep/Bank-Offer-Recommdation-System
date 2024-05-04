from config import *

def scrap_pnb_offers(url):
    soup = get_soup(url)
    brand_category_dict_lower = {
        key.lower(): value for key, value in brand_category_dict.items()
    }
    heading_content = soup.find("div", class_="cotnent-outer")
    merchant_name = heading_content.text.strip().split("-")[0].strip()
    offer_title = heading_content.text.strip().split("\n")[0].strip()
    detailed_offer_text = (
        soup.find("div", class_="description-widget ls-widget")
        .find("div", class_="widget-content")
        .text.strip()
    )
    end_date = (
        soup.find("div", class_="sidebar-side col-lg-4 col-md-12 col-sm-12")
        .find("b")
        .text.strip()
    )
    redeem_link = (
        soup.find("div", class_="sidebar-side col-lg-4 col-md-12 col-sm-12")
        .find_all("a")[1]
        .text.strip()
        .replace("Go to Website", "")
        .strip()
    )
    if merchant_name.lower() in brand_category_dict_lower:
        category = brand_category_dict_lower[merchant_name.lower()]
    else:
        category = None

    if redeem_link:
        Offer_redumption_mode = "Online"
    else:
        Offer_redumption_mode = "Offline"

    data = {
        "Bank Name": "PNB",
        "Merchant Name": merchant_name,
        "Link to offer on Bank site (for reference)": url,
        "Category": category,
        "Offer title (if available)": offer_title,
        "Start date": None,
        "End date": end_date,
        "Detailed offer text (if available)": detailed_offer_text,
        "Logo link": None,
        "Offer image": None,
        "Redeem link": redeem_link,
        "Promo code (if available)": None,
        "Online/ Offline": Offer_redumption_mode,
        "If offline, cities": None,
    }
    return data


def get_links(base_url):
    soup = get_soup(base_url)
    offers_content = soup.find("section", class_="ls-section style-two").find(
        "div", "content-column col-lg-12 col-md-12 col-sm-12"
    )
    offers_content.find_all(
        "div",
        "listing-block col-lg-4 col-md-6 col-sm-12 a_online_offer cls_brand_type_shopping",
    )
    # Find all anchor tags
    anchor_tags = offers_content.find_all("a")

    # Extract href attributes from anchor tags
    links = set([tag["href"] for tag in anchor_tags if not tag["href"] == "#"])
    return links


if __name__ == "__main__":
    base_url = "https://offers.pnbcards.in/#listing"
    links = get_links(base_url)
    final_data = []
    for each_url in links:
        final_data.append(scrap_pnb_offers(each_url))
    df = pd.DataFrame(final_data, columns=columns_to_use)
    df.to_excel(
        os.path.join(base_directory, "data", "pnb_offers.xlsx"), engine="openpyxl"
    )
