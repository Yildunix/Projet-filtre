import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:5000"

st.title("Nettoyage et Filtrage de Données CSV")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Envoyer le fichier à l'API Flask
    files = {'file': uploaded_file}
    response = requests.post(f"{API_URL}/upload", files=files)

    if response.status_code == 200:
        st.success("Fichier uploadé avec succès !")

        # Récupérer le filepath dans la réponse JSON
        uploaded_filepath = response.json()['filepath']
        df = pd.read_csv(uploaded_filepath)  # Utilise le filepath pour lire le fichier

        st.write("Aperçu des données :")
        st.write(df)

        # Sélectionner les colonnes à conserver
        columns = st.multiselect("Sélectionnez les colonnes à conserver :", options=df.columns)

        # Appliquer des filtres sur les colonnes
        filters = {}
        for column in df.columns:
            unique_values = df[column].unique()
            selected_value = st.selectbox(f"Filtrer {column} :", options=[""] + list(unique_values))
            if selected_value:
                filters[column] = selected_value

        if st.button("Appliquer les filtres"):
            filter_payload = {
                'filepath': uploaded_filepath,
                'filters': {
                    'columns_to_keep': columns,
                    'conditions': filters
                }
            }
            filter_response = requests.post(f"{API_URL}/filter", json=filter_payload)

            if filter_response.status_code == 200:
                cleaned_filepath = filter_response.json()['cleaned_filepath']
                st.success("Fichier filtré avec succès !")
                st.download_button(
                    "Télécharger le fichier nettoyé",
                    data=open(cleaned_filepath, 'rb'),
                    file_name="cleaned_data.csv"
                )
            else:
                st.error("Erreur lors de l'application des filtres.")
