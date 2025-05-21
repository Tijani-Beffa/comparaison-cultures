import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Comparateur de cultures agricoles", layout="wide")
st.title("🌾 Tableau de bord : Comparaison des cultures agricoles")

uploaded_file = st.file_uploader("📁 Charger un fichier CSV contenant les données agricoles", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("📋 Aperçu des données")
        st.dataframe(df)

        st.subheader("🔍 Filtrer les cultures")
        if 'Culture' not in df.columns:
            st.error("Le fichier doit contenir une colonne 'Culture'.")
        else:
            cultures = df['Culture'].unique().tolist()
            selected_cultures = st.multiselect("Sélectionnez les cultures à afficher :", cultures, default=cultures)
            filtered_df = df[df['Culture'].isin(selected_cultures)]

            st.subheader("📈 Graphique : Rendement par culture")
            if 'Rendement' in df.columns:
                fig = px.bar(filtered_df, x='Culture', y='Rendement', color='Culture',
                             title="Comparaison des rendements par culture")
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("📊 Analyse comparative")
            if 'Surface' in df.columns and 'Rendement' in df.columns:
                filtered_df['Rendement_ha'] = filtered_df['Rendement'] / filtered_df['Surface']
                st.write("💡 Rendement par hectare :")
                st.dataframe(filtered_df[['Culture', 'Surface', 'Rendement', 'Rendement_ha']])
            else:
                st.warning("Le fichier doit contenir les colonnes 'Surface' et 'Rendement' pour cette analyse.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier : {e}")
else:
    st.info("Veuillez charger un fichier CSV pour commencer.")
