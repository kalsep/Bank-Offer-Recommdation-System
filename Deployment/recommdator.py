import pandas as pd
import joblib
import streamlit as st
pd.set_option("display.max_columns", 100)




@st.cache_data
def get_df():
    dataframe = pd.read_excel(
        r"C:\Users\Pravin\Documents\Github\Bank Offer Recommdation System\Deployment\final_df.xlsx"
    ).drop("Unnamed: 0", axis=1)
    return dataframe

# @st.cache_resource
# def filter_data(search_query):
#     try:
#         df = get_df()
#         if search_query:
#             filtered_df = df[df["Merchant Name"]==search_query]
#             if filtered_df.empty():
#                 filtered_df = df[df.apply(lambda row: search_query.lower() in " ".join(map(str, row)).lower(), axis=1)]
            
#             if filtered_df.empty:
#                 return None
#         else:
#             return None  # Return None if no filter text is available
#         return filtered_df.sample(n=1).index if not filtered_df.empty else None
#     except Exception as e:
#         st.error(f"An error occurred while filtering data: {e}")
#         return None

@st.cache_resource
def filter_data(search_query):
    try:
        df = get_df()
        if search_query:
            filtered_df = df[df["Merchant Name"]==search_query]
            if filtered_df.empty:
                filtered_df = df[df.apply(lambda row: search_query.lower() in " ".join(map(str, row)).lower(), axis=1)]
        else:
            return None  # Return None if no filter text is available
        
        if filtered_df.empty:
            return None  # Return None if the filtered DataFrame is empty
        
        return filtered_df.sample(n=1).index
    except Exception as e:
        st.error(f"An error occurred while filtering data: {e}")
        return None


def recommend_similar_offers(offer_id, similarity_matrix, offers_df, top_n=10):
    similar_indices = similarity_matrix[offer_id].argsort()[-top_n - 1 : -1][::-1]
    similar_offers = offers_df.iloc[similar_indices]
    return similar_offers


# Load the model
model = joblib.load(
    r"C:\Users\Pravin\Documents\Github\Bank Offer Recommdation System\recommendation_model_similarity_index.pkl"
)

# Define a function to generate recommendations
def generate_recommendations(offer_id):
    final_df = get_df()
    # Get recommendations using the loaded model
    recommended_offers = recommend_similar_offers(offer_id, model, final_df)
    return recommended_offers
