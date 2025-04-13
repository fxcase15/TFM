import os
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from io import BytesIO
import re

# =====================================
# FUNCIONS DE PREPROCESSAMENT
# =====================================

def contains_any(text, keywords):
    if pd.isnull(text): return False
    return any(k.lower() in text.lower() for k in keywords)

def extract_kcal(val):
    if pd.isnull(val): return 0
    match = re.search(r"\((\d+)\s*kcal\)", str(val))
    return int(match.group(1)) if match else 0

def convert_grams(val):
    try:
        return float(str(val).replace("g", "").replace(",", ".").strip())
    except:
        return 0

def preprocess_products(df):
    gluten_kw = ["gluten", "glutamaat", "tarwe"]
    lactose_kw = ["lactose"]
    nuts_kw = ["noten", "amandel", "hazelnoot", "pecannoot", "cashewnoot", "kokosnoot", "macadamianoot", "pinda", "sesamzaad"]

    df['Nutriscore'] = df['product_descripion'].str.extract(r'Nutri-Score ([A-E])', expand=False).fillna("Unknown")
    df['Bio'] = df['product_descripion'].str.contains("Biologisch", case=False, na=False).astype(int)
    df['Vegan'] = df['product_descripion'].str.lower().str.contains("vegan", na=False).astype(int) | df['Kenmerken'].str.lower().str.contains("veganistisch", na=False).astype(int)
    df['Vegetarian'] = df['Vegan'] | df['product_descripion'].str.lower().str.contains("vega", na=False).astype(int) | df['Kenmerken'].str.lower().str.contains("vegetarisch", na=False).astype(int)
    df['Halal'] = df['Kenmerken'].str.lower().str.contains("halal", na=False).astype(int)
    df['Recyclable'] = df['Kenmerken'].str.lower().str.contains("recyclebaar|groene punt", na=False).astype(int)
    df['Responsible_producers'] = df['Kenmerken'].str.lower().str.contains("natuur & boer", na=False).astype(int)
    df['BestPrice'] = df['product_descripion'].str.contains("Prijsfavoriet", na=False).astype(int)
    df['Local_Products'] = df['product_descripion'].str.lower().str.contains("uit nederland", na=False).astype(int)

    df['Does_NOT_contain_Gluten'] = df['Allergie_informatie_Bevat'].apply(lambda x: int(not contains_any(str(x), gluten_kw)))
    df['Could_contain_Gluten'] = df['Allergie_informatie_kan_bevatten'].apply(lambda x: int(contains_any(str(x), gluten_kw)))
    df['Does_NOT_contain_Lactose'] = df['Allergie_informatie_Bevat'].apply(lambda x: int(not contains_any(str(x), lactose_kw)))
    df['Could_contain_Lactose'] = df['Allergie_informatie_kan_bevatten'].apply(lambda x: int(contains_any(str(x), lactose_kw)))
    df['Does_NOT_contain_Nuts'] = df['Allergie_informatie_Bevat'].apply(lambda x: int(not contains_any(str(x), nuts_kw)))
    df['Could_contain_Nuts'] = df['Allergie_informatie_kan_bevatten'].apply(lambda x: int(contains_any(str(x), nuts_kw)))

    df['Kcal'] = df['Energie'].apply(extract_kcal)
    df['Vet'] = df['Vet'].apply(convert_grams)
    df['verzadigd'] = df['waarvan_verzadigd'].apply(convert_grams)
    df['Koolhydraten'] = df['Koolhydraten'].apply(convert_grams)
    df['suikers'] = df['waarvan_suikers'].apply(convert_grams)
    df['Eiwitten'] = df['Eiwitten'].apply(convert_grams)
    df['Voedingsvezel'] = df['Voedingsvezel'].apply(convert_grams)
    df['Zout'] = df['Zout'].apply(convert_grams)

    df['Protein_from_energy'] = np.where(df['Kcal'] > 0, (df['Eiwitten'] * 4) / df['Kcal'], 0)
    df['Sat_Fat_from_energy'] = np.where(df['Kcal'] > 0, (df['verzadigd'] * 9) / df['Kcal'], 0)

    df['Calc_Gluten'] = np.where((df['Does_NOT_contain_Gluten'] == 1) & (df['Could_contain_Gluten'] == 0), 100, 0)
    df['Calc_Lactose'] = np.where((df['Does_NOT_contain_Lactose'] == 1) & (df['Could_contain_Lactose'] == 0), 100, 0)
    df['Calc_Nuts'] = np.where((df['Does_NOT_contain_Nuts'] == 1) & (df['Could_contain_Nuts'] == 0), 100, 0)
    df['Calc_Vegan'] = df['Vegan'] * 100
    df['Calc_Vegetarian'] = df['Vegetarian'] * 100
    df['Calc_Halal'] = np.where((df['category'] != "Alcoholic Drinks") & ((df['Halal'] == 1) | (df['Vegan'] == 1) | (df['Vegetarian'] == 1)), 100, 0)

    df['Calc_Diabetes'] = np.select(
        [df['suikers'] <= 2, df['suikers'] <= 4, df['suikers'] <= 6, df['suikers'] <= 8, df['suikers'] <= 10],
        [100, 80, 60, 40, 20],
        default=0
    )
    df['kcal_per_100g'] = np.where(df['quantity_normalized'] > 0, df['Kcal'] / df['quantity_normalized'] * 100, 0)

    df['Calc_Loosing_weight'] = np.select(
        [df['kcal_per_100g'] <= 100, df['kcal_per_100g'] <= 150, df['kcal_per_100g'] <= 200],
        [100, 70, 40],
        default=0
    )
    df['Calc_Eating_Healthy'] = df['Nutriscore'].map({'A': 100, 'B': 75, 'C': 50, 'D': 25, 'E': 0}).fillna(0)
    df.loc[df['category'] == 'Alcoholic Drinks', 'Calc_Eating_Healthy'] -= 25
    df['Calc_Eating_Healthy'] = df['Calc_Eating_Healthy'].clip(lower=0)

    df['Calc_Reducing_Colesterol'] = df['Sat_Fat_from_energy'].apply(lambda val: 100 if val < 0.02 else 80 if val < 0.04 else 60 if val < 0.06 else 40 if val < 0.08 else 20 if val < 0.1 else 0)
    df['Calc_High_Protein'] = df['Protein_from_energy'].apply(lambda val: 100 if val > 0.5 else 80 if val > 0.4 else 60 if val > 0.3 else 40 if val > 0.2 else 20 if val > 0.1 else 0)

    df['price_per_100g'] = df['price'] / df['quantity_normalized'] * 100
    df['Calc_Price'] = np.select(
        [df['BestPrice'] == 1, df['price_per_100g'] < 0.5, df['price_per_100g'] < 1, df['price_per_100g'] < 1.5, df['price_per_100g'] < 2],
        [100, 100, 75, 50, 25],
        default=0
    )
    df['Calc_Sustainability'] = np.where((df['Recyclable'] == 1) | (df['Bio'] == 1) | (df['Responsible_producers'] == 1), 100, 0)
    df['Calc_Local_Products'] = np.where(df['Local_Products'] == 1, 100, 0)

    return df

# =====================================
# FUNCIONS DE PUNTUACIÓ
# =====================================

def calculate_scores(df, user_priorities):
    scoring_columns = [
        'Calc_Gluten', 'Calc_Lactose', 'Calc_Nuts', 'Calc_Diabetes',
        'Calc_Vegan', 'Calc_Vegetarian', 'Calc_Halal', 'Calc_Loosing_weight',
        'Calc_Eating_Healthy', 'Calc_Reducing_Colesterol', 'Calc_High_Protein',
        'Calc_Price', 'Calc_Sustainability', 'Calc_Local_Products']

    product_features = StandardScaler().fit_transform(df[scoring_columns].fillna(0))
    weights = [user_priorities.get(col.replace("Calc_", "").replace("_", " "), 0) for col in scoring_columns]

    personalized_scores = df[scoring_columns].dot(weights) / (sum(weights) or 1)
    similarity_raw = cosine_similarity([weights], product_features)[0]
    similarity_scaled = MinMaxScaler().fit_transform(similarity_raw.reshape(-1, 1)).flatten() * 100

    results = []
    for i, row in df.iterrows():
        final_score = 0.7 * personalized_scores[i] + 0.3 * similarity_scaled[i]
        results.append({
            "Product_Name": row["product_name"],
            "Category": row["category"],
            "Price (€)": round(row["price"], 2),
            "Nutriscore": row["Nutriscore"],
            "Final_Score": round(final_score, 0),
            "URL": row["url"]
        })

    return pd.DataFrame(results)

# =====================================
# INTERFÍCIE STREAMLIT
# =====================================

st.set_page_config(page_title="Recommender", layout="wide")
st.title("🍎 Your Personalized Groceries Recommender")
st.sidebar.title("👤 User session")
user_id = st.sidebar.text_input("Please introduce your name", value="usuari_default")

if "user_id" not in st.session_state:
    st.session_state.user_id = user_id
else:
    st.session_state.user_id = user_id

@st.cache_data
def load_data():
    return pd.read_excel("products_quantities_normalized.xlsx")

product_data = load_data()

st.subheader("Please select your priorities")
high = st.multiselect("🎯 High Priority (x3)", ['Gluten', 'Lactose', 'Nuts', 'Diabetes', 'Vegan', 'Vegetarian', 'Halal'])
medium = st.multiselect("⚖️ Medium Priority (x2)", ['Loosing weight', 'Eating Healthy', 'Reducing Colesterol', 'High Protein'])
low = st.multiselect("💸 Low Priority (x1)", ['Price', 'Sustainability', 'Local Products'])

user_priorities = {k: 0 for k in [
    'Gluten', 'Lactose', 'Nuts', 'Diabetes', 'Vegan', 'Vegetarian', 'Halal',
    'Loosing weight', 'Eating Healthy', 'Reducing Colesterol', 'High Protein',
    'Price', 'Sustainability', 'Local Products'
]}
for k in high: user_priorities[k] = 3
for k in medium: user_priorities[k] = 2
for k in low: user_priorities[k] = 1

if "recs_ready" not in st.session_state:
    st.session_state.recs_ready = False

if st.button("🔍 Generate personalized recommendations"):
    st.session_state.recs_ready = True

if st.session_state.recs_ready:
    df = preprocess_products(product_data)
    recommendations = calculate_scores(df, user_priorities)
    sorted_recommendations = recommendations.sort_values("Final_Score", ascending=False)

    st.subheader("📦 Productes destacats per categoria")

    categories = sorted(sorted_recommendations["Category"].unique())
    filtered_by_category = (
        sorted_recommendations[sorted_recommendations["Final_Score"] > 90]
        .sort_values(["Category", "Final_Score"], ascending=[True, False])
        .groupby("Category")
        .head(3)
    )

    st.subheader("📦 Productes destacats per categoria (Final Score > 90)")

    for cat in filtered_by_category["Category"].unique():
        st.markdown(f"#### 🗂️ {cat}")
        subset = filtered_by_category[filtered_by_category["Category"] == cat]

        for i, row in subset.iterrows():
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"**[{row['Product_Name']}]({row['URL']})**", unsafe_allow_html=True)
                st.caption(f"💶 {row['Price (€)']}€ | 🥗 Nutri: {row['Nutriscore']} | ⭐ {row['Final_Score']}")
            with col2:
                st.checkbox("✅", key=f"buy_highscore_{cat}_{i}")



    st.subheader("🔎 Vols veure els 5 millors productes d'una categoria concreta?")
    categoria_seleccionada = st.selectbox("Tria la categoria", options=categories)

    top5_especific = (
        sorted_recommendations[sorted_recommendations["Category"] == categoria_seleccionada]
        .sort_values("Final_Score", ascending=False)
        .head(5)
    ).copy()

    top5_especific["Link"] = top5_especific["URL"].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>')
    top5_especific = top5_especific[["Product_Name", "Price (€)", "Nutriscore", "Final_Score", "Link"]]

    st.markdown(f"#### 🏆 Top 5 de la categoria: **{categoria_seleccionada}**")
    st.write(top5_especific.to_html(escape=False, index=False), unsafe_allow_html=True)


    st.subheader("🥇 Top 5 Recommended Groceries")

    def make_clickable(val):
        return f'<a href="{val}" target="_blank">Link</a>' if pd.notna(val) else ''

    display_df = sorted_recommendations.head(5).copy()
    display_df["Link"] = display_df["URL"].apply(make_clickable)
    display_df = display_df[["Product_Name", "Category", "Price (€)", "Nutriscore", "Final_Score", "Link"]]
    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    st.subheader("📦 Top 3 Products per category")
    top5_by_category = (
        sorted_recommendations.sort_values(["Category", "Final_Score"], ascending=[True, False])
        .groupby("Category")
        .head(3)
    )

    for cat in top5_by_category["Category"].unique():
        st.markdown(f"#### 🗂️ {cat}")
        subset = top5_by_category[top5_by_category["Category"] == cat]
        cols = st.columns(5)
        for i, (_, row) in enumerate(subset.iterrows()):
            with cols[i % 5]:
                st.markdown(f"**[{row['Product_Name']}]({row['URL']})**", unsafe_allow_html=True)
                st.caption(f"💶 {row['Price (€)']}€ | 🥗 Nutri: {row['Nutriscore']} | ⭐ {row['Final_Score']}")
                st.checkbox("✅ Add to basket", key=f"buy_{cat}_{i}")



    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Recomanacions')
        return output.getvalue()

    excel_data = convert_df_to_excel(sorted_recommendations)


    selected_products = []

    # Top 5 per categoria
    for cat in top5_by_category["Category"].unique():
        subset = top5_by_category[top5_by_category["Category"] == cat]
        for i, (_, row) in enumerate(subset.iterrows()):
            if st.session_state.get(f"buy_{cat}_{i}", False):
                product_id = str(row["URL"]).split("/")[-1]
                selected_products.append({
                    "Product_Name": row["Product_Name"],
                    "Product_ID": product_id,
                    "Quantity": 1
                })

    # Productes destacats per categoria (>90)
    for cat in filtered_by_category["Category"].unique():
        subset = filtered_by_category[filtered_by_category["Category"] == cat]
        for i, (_, row) in enumerate(subset.iterrows()):
            if st.session_state.get(f"buy_highscore_{cat}_{i}", False):
                product_id = str(row["URL"]).split("/")[-1]
                selected_products.append({
                    "Product_Name": row["Product_Name"],
                    "Product_ID": product_id,
                    "Quantity": 1
                })


    if selected_products:
        url_parts = [f"p={p['Product_ID']}:{p['Quantity']}" for p in selected_products]
        shopping_url = "https://www.ah.nl/mijnlijst/add-multiple?" + "&".join(url_parts)
        st.markdown(f"### 🔗 [Click here to add your groceries in the basket]({shopping_url})", unsafe_allow_html=True)
    if selected_products:
        st.subheader("👀 Your cart")
        preview_df = pd.DataFrame(selected_products)[["Product_Name", "Product_ID", "Quantity"]]
        preview_df["Link"] = preview_df["Product_ID"].apply(lambda x: f"https://www.ah.nl/producten/product/{x}")
        preview_df = preview_df[["Product_Name", "Quantity", "Link"]]
        preview_df["Link"] = preview_df["Link"].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>')
        st.write(preview_df.to_html(escape=False, index=False), unsafe_allow_html=True)

        # Excel amb productes seleccionats
        df_cart = pd.DataFrame(selected_products)

        def guardar_a_google_sheets(df_cart, usuari, priorities_dict):
            import gspread
            import json
            from oauth2client.service_account import ServiceAccountCredentials
            from datetime import datetime

            scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds_dict = json.loads(st.secrets["gcp_credentials"])
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
            client = gspread.authorize(creds)

            sheet = client.open("TFM - Cistells usuaris").sheet1  # Make sure this name matches your sheet
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Convert priorities dict to readable string (e.g. "Vegan(3), Price(1)")
            priorities_str = ", ".join([f"{k}({v})" for k, v in priorities_dict.items() if v > 0])

            for _, row in df_cart.iterrows():
                sheet.append_row([
                    timestamp,
                    usuari,
                    priorities_str,
                    row["Product_Name"],
                    row["Product_ID"]
                ])

        guardar_a_google_sheets(df_cart, st.session_state.user_id, user_priorities)
        # Crear una carpeta si no existeix
        os.makedirs("dades_usuaris", exist_ok=True)

        # Nom de fitxer amb usuari i timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dades_usuaris/cistell_{st.session_state.user_id}_{timestamp}.xlsx"

        # Guardar el fitxer
        df_cart.to_excel(filename, index=False)
        output_cart = BytesIO()
        with pd.ExcelWriter(output_cart, engine='xlsxwriter') as writer:
            df_cart.to_excel(writer, index=False, sheet_name='Cistell')
    st.download_button(
        label="📄 Download all recommendations in Excel",
        data=excel_data,
        file_name="recomanacions.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
