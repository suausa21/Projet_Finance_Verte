#Page sur les stratégies
import streamlit as st
import base64
from Utilities.Data_Collector_final import data_collector
from Utilities.Strategie_final import strategies
from Utilities.Indice_final import indice_user


from datetime import datetime
from dateutil.relativedelta import relativedelta

# Configuration de la page 1
st.set_page_config(page_title="Your portfolio", layout="centered",initial_sidebar_state="collapsed")


#------------------------------------Arrière plan-------------------------------------------------------------
# Fonction pour convertir une image locale en base64
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Fonction pour appliquer l'image en arrière-plan
def set_background(image_path):
    encoded_image = get_base64_image(image_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .main > div {{
            background-color: rgba(255, 255, 255, 0.75); 
            padding: 2rem;
            border-radius: 10px; 
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
# --------- IMAGE EN FOND --------- 
image_path = "Arriere_Plan_Page_1.png"  # 
set_background(image_path)


#-------------------------------ELEMENTS PAGE-------------------------------------------------
# Titre centré
st.markdown("<h1 style='text-align: center; color: white;'>Votre Portefeuille</h1>", unsafe_allow_html=True)

#----------------------------------------------------------------------------Boutons menu principal--------------------------------------------------


#Récupérer les pays de la base de données 
country_map = {
    'US': 'États-Unis',
    'FR': 'France',
    'DE': 'Allemagne',
    'JP': 'Japon',
    'IN': 'Inde',
    'CN': 'Chine',
    'KR': 'Corée du Sud',
    'GB': 'Royaume-Uni',
    'CA': 'Canada',
    'AU': 'Australie',
    'SE': 'Suède',
    'IT': 'Italie',
    'BR': 'Brésil',
    'ES': 'Espagne',
    'FI': 'Finlande',
    'NL': 'Pays-Bas',
    'SG': 'Singapour',
    'ZA': 'Afrique du Sud',
    'LU': 'Luxembourg',
    'IE': 'Irlande',
    'NO': 'Norvège',
    'PL': 'Pologne',
    'MY': 'Malaisie',
    'CH': 'Suisse',
    'TR': 'Turquie',
    'HK': 'Hong Kong',
    'NZ': 'Nouvelle-Zélande',
    'DK': 'Danemark',
    'QA': 'Qatar',
    'BE': 'Belgique',
    'AE': 'Émirats Arabes Unis',
    'IL': 'Israël',
    'SA': 'Arabie Saoudite',
    'CL': 'Chili',
    'ID': 'Indonésie',
    'GR': 'Grèce',
    'MT': 'Malte',
    'UY': 'Uruguay',
    'BG': 'Bulgarie',
    'LT': 'Lituanie',
    'CY': 'Chypre',
    'TW': 'Taïwan',
    'AT': 'Autriche',
    'MA': 'Maroc',
    'TH': 'Thaïlande',
}

#Récupérer les données de la Page Home
if 'score_df' in st.session_state and 'pays_df' in st.session_state:
    score = st.session_state['score_df']
    pays = st.session_state['pays_df']
    st.success("✅ Données récupérées avec succès depuis la mémoire de session.")
    pays['Pays'] = pays['HQ'].map(country_map)
    pays_uniques = sorted(pays['Pays'].dropna().unique())

else:
    st.warning("⚠️ Aucune donnée en mémoire. Veuillez d'abord lancer le calcul sur la page précédente.")
    pays_uniques = [""]


# --- Sidebar : Choix utilisateur ---

st.markdown("""
    <style>
        /* ---- Style global ---- */
        html, body, .main {
            background-color: #f4f6f8;
            font-family: 'Segoe UI', Roboto, sans-serif;
        }

        .section-container {
            background-color: #ffffff;
            border-radius: 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            padding: 30px;
            margin-bottom: 40px;
            color: #1f2937;
        }

        .section-title {
            text-align: center;
            font-size: 26px;
            font-weight: 700;
            color: white;
            margin-bottom: 25px;
        }

        .metric-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 12px;
            color: white;
        }

        .stButton > button {
            width: 100%;
            border-radius: 12px;
            padding: 12px;
            font-size: 16px;
            font-weight: 600;
            background: linear-gradient(90deg, #3b82f6, #2563eb);
            color: white;
            border: none;
            transition: 0.3s ease;
        }

        .stButton > button:hover {
            background: linear-gradient(90deg, #2563eb, #1d4ed8);
            transform: scale(1.02);
        }

        /* Selectboxes et Inputs */
        .stSelectbox, .stNumberInput, .stTextInput {
            background-color: #f9fafb;
            border-radius: 12px; 
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)


#-------------------STYLE 2-----------------------------

st.markdown("""
    <style>
        .section-container-2 {
            background: linear-gradient(135deg, #1e4732, #38a169);
            border-radius: 15px;
            padding: 5px;
            margin-bottom: 30px;
            color: white;
        }
        .section-title {
            text-align: center;
            font-size: 25px; 
            font-weight: 600;
            margin-bottom: 5px;
            font-family: 'Helvetica Neue', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

#---------------------------------BOUTONS-----------------------------------------

with st.container():
    
    st.markdown("""
        <div class="section-container-2">
            <div class="section-title"> 📊 Votre Indice</div>
        </div>
    """, unsafe_allow_html=True)

poids = []
with st.container():
    #Sélectionner le profil 
    profil = st.selectbox("Votre Profil", ["Expert", "Normal"])
    pondérations_valides = True 

    # Ligne 1
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="metric-title">🏭 Impact climatique direct de la chaîne de valeur</div>', unsafe_allow_html=True)
        if profil == "Expert":
            poids_b = st.number_input("Emissions CO2 (%)", min_value=5, max_value=100, value=11, step=1)
            poids_c = st.number_input("Mise en oeuvre de politique énergitique efficace (%)", min_value=5, max_value=100, value=11, step=1)
            poids_d = st.number_input("Usage d'énergies renouvelables (%)", min_value=5, max_value=100, value=11)

            
        else:
            poids_b = st.number_input("Impact direct de l'activité (%)", min_value=10, max_value=100, value=30, step=1)


    with col2:
        st.markdown('<div class="metric-title">🔁 Impact climatique indirect de la chaîne de valeur</div>', unsafe_allow_html=True)
        if profil == "Expert":
            poids_e = st.number_input("Gestion environnementale de la chaîne d'approvisionnement (%)", min_value=5, max_value=100, value=11)
            poids_f = st.number_input("Suivi environnemental (%)", min_value=5, max_value=100, value=11)
            poids_fz = st.number_input("Minimisation impact produit (%)", min_value=5, max_value=100, value=11)
        else:
            poids_c = st.number_input("Réduction de l'impact des produits (%)", min_value=10, max_value=100, value=30, step=1)
    # Espace entre les lignes
    st.markdown("<br>", unsafe_allow_html=True)

    # Ligne 2
    col3, col4 = st.columns(2)
    with col3:
        #Option ESG (Expert + Normal)
        st.markdown('<div class="metric-title">🌍 ESG Global </div>', unsafe_allow_html=True)
        poids_a = st.number_input("ESG (%)", min_value=10, max_value=100, value=12)
        st.markdown('<div class="metric-title"> Innovation <br> </div>', unsafe_allow_html=True)
        poids_innov = st.number_input("Innovation Environnementale (%)", min_value=10, max_value=100, value=11)
    with col4:
        st.markdown('<div class="metric-title">🌱 Risque non climatique <br> </div>', unsafe_allow_html=True)
        if profil == "Expert":
            poids_g = st.number_input("Utilisation des ressources (%)", min_value=5, max_value=100, value=11)
            poids_h = st.number_input("Politiques d'efficacité de gestion de l'eau (%)", min_value=5, max_value=100, value=11)
            poids_i = st.number_input("Réduction des déchets électroniques (%)", min_value=5, max_value=100, value=11)
            total = poids_a+poids_b+poids_c+poids_d+poids_e+poids_f+poids_g+poids_h+poids_i+poids_innov+poids_fz
            poids.extend([poids_a,poids_innov, poids_b,poids_c,poids_d,poids_e,poids_f,poids_fz, poids_g,poids_h,poids_i])
        else:
            poids_d = st.number_input("Risque non climatique (%)", min_value=10, max_value=100, value=28, step=1)
            total = poids_a+poids_b+poids_c + poids_d+poids_innov
            poids.extend([ poids_a,poids_innov,poids_b,poids_c , poids_d])
    
    st.markdown('<div class="metric-title">🌍 Pays des actions </div>', unsafe_allow_html=True)
    st.markdown(
    '<p style="color: white; font-size: 16px;">Choisis un ou plusieurs pays :</p>',
    unsafe_allow_html=True
    )
    pays_choisis = st.multiselect("Choisis un ou plusieurs pays :", options=pays_uniques)






    # Ajout du style CSS pour la zone blanche
# Style général pour les messages
st.markdown("""
    <style>
        .result-box {
            background-color: #ffffff; /* fond blanc */
            border-left: 6px solid;
            border-radius: 12px;
            padding: 16px 22px;
            margin: 20px 0;
            font-weight: 600;
            font-size: 16px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        }

        .success {
            border-color: #22c55e; /* vert */
            color: #166534;
        }

        .error {
            border-color: #ef4444; /* rouge */
            color: #991b1b;
        }

        .icon {
            font-size: 18px;
            margin-right: 8px;
        }
    </style>
""", unsafe_allow_html=True)


if total != 100:
    st.markdown(f"""
        <div class="result-box error">
            <span class="icon">❌</span> Le total est {total}%. Il doit être égal à 100%.
        </div>
    """, unsafe_allow_html=True)
    pondérations_valides = False
else:
    st.markdown(f"""
        <div class="result-box success">
            <span class="icon">✅</span> Pondération correcte ({total}%)
        </div>
    """, unsafe_allow_html=True)
  


with st.container():
    st.markdown("""
        <div class="section-container-2">
            <div class="section-title"> 💰 Votre Stratégie des Gestion de Portefeuille</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(
    """
    <div style="color: white; font-size:14px;">
        Les stratégies proposées dans notre outil de simulation sont présentées à titre d’exemple.<br>
        Elles reflètent certaines des approches les plus appréciées par nos clients.<br>
        N’hésitez pas à contacter nos conseillers pour construire une stratégie adaptée à vos objectifs et à votre profil.
        <br>
    </div>
    """, 
    unsafe_allow_html=True)
    #Entrer les dates : dates pour backtester et dates ou la stratégie sera appliquée
    nb_annees = st.number_input(
        "⏳ Sur combien d'années souhaitez-vous backtester la stratégie ?",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )
    #Mettre une explication de la stratégie testée
    indice_cible = st.selectbox("Indice cible", ["Rendement moyen annualisé", "Volatilité annualisée", "Sharpe Ratio", "Skewness"], key="indice_cible_unique")


bouton_ok = st.button("Calculer mon portefeuille")

if pays_uniques == "":
    st.button("Calculer mon portefeuille", disabled=True)
else:

    if bouton_ok:
        if total != 100 :
            st.error("La pondération doit être égale à 100% pour lancer les calculs.")
        else:
            st.markdown("""
        <div class="section-container-2">
            <div class="section-title"> 🔍 Vos résultats</div>
        </div>
            """, unsafe_allow_html=True)
        
            st.markdown(
            """
            <div style="color: white; font-size:14px;">
            Résultats en dessous de vos attentes ?<br>
            Pas d'inquiétude ! Contactez l'un de nos conseillers : il sera à votre écoute pour vous accompagner et construire un portefeuille sur-mesure, adapté à votre profil et à vos objectifs.
            <br>
            </div>
            """, 
            unsafe_allow_html=True)

#DATA COLLECTOR
            #Avoir les initiales pour la fonction data collector
            reverse_country_map = {v: k for k, v in country_map.items()}
            initiales = [reverse_country_map[p] for p in pays_choisis if p in reverse_country_map]

        #INDICE 
        
        #Calcul du score
        #Calcul de l'indice utilisateur
            user = indice_user(score, poids)
            score_utilisateur, actifs_selectionnes = user.scoring()
            st.markdown("<h2 style='color: white;'>Résultats du Score Utilisateur</h2>", unsafe_allow_html=True)
            st.dataframe(score_utilisateur)
            st.markdown("<h2 style='color: white;'>Actifs sélectionnés par ordre décroissant de score</h2>", unsafe_allow_html=True)
            st.write(actifs_selectionnes)

        # Appel à la fonction data_collector avec le DataFrame score et la période choisie.
        # Ici, nous supposons que 'score' contient la liste des actifs (par exemple issus de indice_score.actifs)
        
            end_date = datetime.strptime("31/12/2024", "%d/%m/%Y")
            start_date = new_date = end_date - relativedelta(years=int(nb_annees))

            df_rendements = data_collector(
                df_data=score, 
                start=start_date.strftime('%Y-%m-%d'), 
                end=end_date.strftime('%Y-%m-%d')
            )

            #Calcul du portefeuille
         
            # Extraire les noms d'actifs à partir du DataFrame score ESG (par exemple, l'index)
            actifs_user = score.index.tolist()
        
        # Définir les entrants pour la stratégie (l'objectif choisi par l'utilisateur)
            entrants = indice_cible
        # Pour simplifier, on utilise df_rendements pour déterminer à la fois les pondérations et la performance réelle
            df_test = df_rendements.copy()
            df_strat = df_rendements.copy()
 
        # Créer une instance de la classe strategies
            strategie_obj = strategies(
                actifs=actifs_user,
                entrants=entrants,
                df_test=df_test,
                df_strat=df_strat
            )
 
        # Calculer les résultats de la stratégie
            strategie, performance, portfolio_plot = strategie_obj.calcul_resultat()
        
        # Afficher les résultats
            st.markdown("<h2 style='color: white;'>Stratégie Calculée</h2>", unsafe_allow_html=True)
            st.dataframe(strategie)
            st.markdown("<h2 style='color: white;'>Performance du Portefeuille</h2>", unsafe_allow_html=True)
            st.dataframe(performance)
            st.markdown("<h2 style='color: white;'>Graphique: Portefeuille vs Benchmark</h2>", unsafe_allow_html=True)
            st.pyplot(portfolio_plot)
