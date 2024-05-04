from config import *

def process_final_df(data):
    try:
        print("Inside final df creation")
        data_for_df = []
        brand_category_dict_lower = {key.lower(): value for key, value in brand_category_dict.items()}
        for index, row in data.iterrows():
            brand_url = row["Brand url"]
            print(brand_url)
            # category = row["Category"]
            brand_url_response = get_soup(brand_url)
            merchant_name, offer_text, promo_code, Offer_redumption_mode,redeem_link = (
                process_and_scrap_stnd_char_bank_offer_df(brand_url_response)
            )
            if merchant_name.lower() in brand_category_dict_lower:
                category = brand_category_dict_lower[merchant_name.lower()]
            else:
                category = None
            data = {
                "Bank Name": "standard chartered",
                "Merchant Name": merchant_name,
                "Link to offer on Bank site (for reference)": brand_url,
                "Category": category,
                "Offer title (if available)": None,
                "Start date": None,
                "End date": None,
                "Detailed offer text (if available)": offer_text,
                "Logo link": None,
                "Offer image": None,
                "Redeem link": redeem_link,
                "Promo code (if available)": promo_code,
                "Online/ Offline": Offer_redumption_mode,
                "If offline, cities": None,
            }
            data_for_df.append(data)
            print("Appended")
        return pd.DataFrame(data_for_df, columns=columns_to_use)
    except Exception:
        df = pd.DataFrame(data_for_df, columns=columns_to_use)
        return df


def process_and_scrap_stnd_char_bank_offer_df(response):
    try:
        brand_name = (
            response.find("div", class_="productPageBox p-3")
            .find("ol", class_="breadcrumb bg-transparent p-0 fs-14 fw-600 m-0")
            .find("li", class_="breadcrumb-item active")
            .text
        )
        redeemable_status_html_block = response.find(
            "div", class_="productPageBoxNew px-3"
        )
        # if redeemable_status_html_block:
        #     cant_use_online = redeemable_status_html_block.find("li", class_="dont")
        #     if cant_use_online:
        #         Offer_redumption_mode = "Offline"
        #     else:
        #         Offer_redumption_mode = "Online"
        # else:
        #     Offer_redumption_mode = None
        offer_banner = response.find(
            "div", class_="productPageCoupon OrangeBox GreenBox px-3 py-1 my-3"
        )
        if offer_banner:
            promo_code = offer_banner.find(
                "label", class_="custom-control-label fs-16 fw-600"
            ).text
            offer_text = offer_banner.find("div", class_="col").text
            # print(offer_text,promo_code)
        else:
            promo_code = None
            offer_text = None
            
        redeem_link_div = response.find_all("div",class_='col-6 col-sm-auto text-center')
        # Find the anchor tag
        redeem_link = None
        if redeem_link_div:
            anchor_tag = redeem_link_div[0].find('a')
            # Extract the link
            if anchor_tag:
                redeem_link = anchor_tag.get('href')
        
        if redeem_link:
            Offer_redumption_mode ="Online"
        else:
            Offer_redumption_mode ="Offline"
            
        return brand_name, offer_text, promo_code, Offer_redumption_mode,redeem_link
    
    except Exception as e:
        print(e)
def get_Stnd_char_bank_offer_df():
    base_url = "https://www.gyftr.com/sc-instavouchers"
    base_html = get_soup(base_url)
    footer_menus = base_html.find("div", class_="col-12 pb-3")
    list_items = footer_menus.find_all(class_="footerVerticalLinks-item")
    # Create a dictionary to store category names and href links
    category_dict = {}

    # Extract category names and href links
    for item in list_items:
        # Exclude the first list item which is just "CATEGORY"
        if item.text != "CATEGORY":
            category_name = item.text
            href_link = item.find("a")["href"]
            category_dict[category_name] = href_link
    # print(category_dict)
    brand_offers_list = []
    for category_name, category_temp_url in category_dict.items():
        offer_url = urljoin(base_url, category_temp_url)
        base_html_offer_category = get_soup(offer_url)
        inside_grid = base_html_offer_category.find("div", class_="row gridList")
        list_of_offers = inside_grid.find_all(
            "div", class_="col-12 col-sm-6 col-md-4 p-3"
        )
        for item in list_of_offers:
            href_link = item.find("a")["href"]

            # new_brand = brand_offers_list[category_name] = href_link
            brand_offers_list.append(
                {"Brand url": str(urljoin(base_url, href_link))}
            )

    df = pd.DataFrame(brand_offers_list, columns=["Brand url"])
    return df


if __name__ == "__main__":
    # print(offer_links_df)
    if os.path.exists("stb.xlsx"):
        print("File Avaialble")
        offer_links_df = pd.read_excel("stb.xlsx")
        final_df = process_final_df(offer_links_df)
        final_df.to_excel(os.path.join(base_directory, "data", "standard_charted_bank_offers.xlsx"))
    else:
        print("File not Avaialble")
        offer_links_df = get_Stnd_char_bank_offer_df()
        offer_links_df.to_excel("stb.xlsx",engine='openpyxl')
        final_df = process_final_df(offer_links_df)
        final_df.to_excel(os.path.join(base_directory, "data", "standard_charted_bank_offers.xlsx"))
    
