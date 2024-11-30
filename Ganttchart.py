import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(page_title="Diagramme de Gantt", layout="wide")

st.title("Diagramme de Gantt Dynamique")

# Fonction pour définir la couleur en fonction de l'avancement
def get_color(progress):
    if progress < 50:
        return "red"
    elif 50 <= progress < 100:
        return "yellow"
    else:
        return "green"

# Initialisation du DataFrame
if "gantt_data" not in st.session_state:
    st.session_state["gantt_data"] = pd.DataFrame(columns=["Phase", "Début", "Fin", "Avancement (%)"])

# Zone d'entrée pour ajouter des phases
st.sidebar.header("Ajouter une nouvelle phase")
phase_name = st.sidebar.text_input("Nom de la phase")
start_date = st.sidebar.date_input("Date de début", value=datetime.now())
end_date = st.sidebar.date_input("Date de fin", value=datetime.now() + timedelta(days=7))
progress = st.sidebar.slider("Avancement (%)", min_value=0, max_value=100, step=1)

if st.sidebar.button("Ajouter la phase"):
    if start_date > end_date:
        st.sidebar.error("La date de début doit être antérieure à la date de fin.")
    else:
        new_data = {
            "Phase": phase_name,
            "Début": pd.to_datetime(start_date),
            "Fin": pd.to_datetime(end_date),
            "Avancement (%)": progress,
        }
        st.session_state["gantt_data"] = pd.concat(
            [st.session_state["gantt_data"], pd.DataFrame([new_data])], ignore_index=True
        )
        st.sidebar.success(f"La phase '{phase_name}' a été ajoutée.")

# Trier les données par date de début
st.session_state["gantt_data"] = st.session_state["gantt_data"].sort_values(by="Début").reset_index(drop=True)

# Afficher les données ajoutées
st.subheader("Données du Projet")
st.dataframe(st.session_state["gantt_data"])

# Créer le diagramme de Gantt
st.subheader("Diagramme de Gantt")
if not st.session_state["gantt_data"].empty:
    fig, ax = plt.subplots(figsize=(12, 6))

    # Préparation des données
    phases = st.session_state["gantt_data"]["Phase"]
    start_dates = date2num(st.session_state["gantt_data"]["Début"])
    end_dates = date2num(st.session_state["gantt_data"]["Fin"])
    durations = end_dates - start_dates
    colors = [get_color(p) for p in st.session_state["gantt_data"]["Avancement (%)"]]

    # Création des barres
    for i, (phase, start, duration, color) in enumerate(zip(phases, start_dates, durations, colors)):
        ax.barh(i, duration, left=start, color=color, edgecolor="black", height=0.5)

    # Configuration des axes
    ax.set_yticks(range(len(phases)))
    ax.set_yticklabels(phases)
    ax.invert_yaxis()  # Inverser l'axe pour avoir la première phase en haut
    ax.xaxis_date()  # Convertir l'axe des x en dates
    ax.set_xlabel("Dates")
    ax.set_ylabel("Phases")
    ax.set_title("Diagramme de Gantt")

    # Améliorer le format des dates
    fig.autofmt_xdate()

    # Afficher le graphique
    st.pyplot(fig)
else:
    st.info("Ajoutez des phases pour générer le diagramme de Gantt.")
