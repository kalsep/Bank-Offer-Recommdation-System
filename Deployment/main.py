from recommdator import *

st.set_page_config(layout="wide")  # noqa: F405

st.title("Bank Offers Recommdation System")  # noqa: F405
st.divider()  # noqa: F405
col1, col2 = st.columns([1, 3])  # noqa: F405, F405
search_text = col1.text_input(label="Input Text", placeholder="Brand, Category, Bank")
recom_button = col1.button("Recommand Me Offer")


if search_text is not None and recom_button:
    df = get_df()  # noqa: F405
    filtered_index = filter_data(search_text)  # noqa: F405
    if filtered_index is not None:
        offer_id = int(filtered_index[0])

        # st.subheader("Your Serach:")
        # st.table(df.iloc[filtered_index])

        col2.subheader("Your Recommdation:")
        col2.write("Top 10 Best Recommdation")
        recommended_offers = generate_recommendations(offer_id)  # noqa: F405
        recommended_offers.rename(
            columns={
                "Merchant Name": "Brand",
                "Link to offer on Bank site (for reference)": "Offer Link",
                "Detailed offer text (if available)": "Offer",
                "Promo code (if available)": "Promo Code",
                "Online/ Offline": "Redumption Mode",
            },
            inplace=True,
        )
        recommended_offers.sample(frac=1)

        with st.container():  # noqa: F405
            col2.dataframe(
                recommended_offers,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Offer Link": st.column_config.LinkColumn("App URL"),  # noqa: F405
                },
            )

    else:
        col2.warning("Sorry No Recommandation, Please Try Refing Your Search")
        # col2.
