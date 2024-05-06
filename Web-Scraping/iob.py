from config import *

def run_iob_offer():
    base_url = "https://www.iob.in/Upload/CEDocuments/iobDomestic_Offers_OfferZone.xlsx"
    data = pd.read_excel(
        "https://www.iob.in/Upload/CEDocuments/iobDomestic_Offers_OfferZone.xlsx",
        engine="openpyxl",
    )

    brand_category_dict_lower = {key.lower(): value for key, value in brand_category_dict.items()}

    data = data[data["Promotion Country "].str.contains("India")]
    final_df = pd.DataFrame(columns=columns_to_use)
    final_df["Merchant Name"] = data["Merchant"]
    final_df["Category"] = final_df["Merchant Name"].str.strip().str.lower().map(brand_category_dict_lower)
    final_df["Offer title (if available)"] = None
    final_df["End date"] = data["Offer validity date"]
    final_df["Detailed offer text (if available)"] = data["Offer Details "]
    final_df["Logo link"] = None
    final_df["Offer image"] = None
    final_df["Redeem link"] = data["Offer Links "]
    final_df["Promo code (if available)"] = None
    final_df["Online/ Offline"] = data["Offline/Online"]
    final_df["If offline, cities"] = None
    final_df["Bank Name"] = "Indian Overseas Bank"
    final_df["Link to offer on Bank site (for reference)"] = "https://www.iob.in/OfferZone.aspx"

    final_df.to_excel(
        os.path.join(base_directory, "data", "indian_oversease_bank.xlsx"),
        engine="openpyxl",
    )
    return final_df