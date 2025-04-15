import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="Revolution Tech Fund Website", layout="wide",initial_sidebar_state="collapsed")

#----------------------ARRIERE PLAN---------------------------------------------------------------------

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
image_path = "Arriere_Plan_Page_Accueil.png"  # 
set_background(image_path)

#Ajouter texte + traits 
st.markdown(
    """
    <style>
    .texte {
        position: fixed;
        top: 65%;
        left: 0.5%;
        color: white;
        font-size: 400%;
        font-family: 'Nunito', sans-serif;
        font-weight: bold;
        font-style: italic;
        background-color: transparent;
        padding: 10px 15px;
        border-radius: 8px;
        z-index: 0;
        line-height: 0.9;
    }
    .texte2 {
        position: fixed;
        top: 10%;
        right : 0.5%;
        color: rgba(255, 255, 255, 0.8);
        font-size: 100%;
        font-family: 'Nunito', sans-serif;
        font-style: italic;
        background-color: transparent;
        padding: 10px 15px;
        border-radius: 8px;
        z-index: 0;
        line-height: 0.9;
    }
 
    .trait1 {
    position : fixed;
    top: 95%;
    left:0%;
    width:45%;
    height:1px;
    background-color: white;
    }

    .trait2 {
    position : fixed;
    top: 45%;
    left:0%;
    width:25%;
    height:1px;
    background-color: white;
    }

    .trait3 {
    position : fixed;
    top: 35%;
    left:0%;
    width:15%;
    height:1px;
    background-color: white;
    } 

    .trait4 {
    position : fixed;
    top: 28%;
    left:15%;
    width:7%;
    height:0.5px;
    background-color: white;
    } 

    .trait5 {
    position : fixed;
    top: 20%;
    left:3%;
    width:10%;
    height:0.5px;
    background-color: white;
    } 

    </style>

    <div class="texte">
        REVOLUTION <br>
        TECHFUND
    </div>
    
    <div class="texte2">
        PROGRAM THE <br>
        FUTURE
    </div>

    <div class="trait1"></div>
    <div class="trait2"></div>
    <div class="trait3"></div>
    <div class="trait4"></div>
    <div class="trait5"></div>

    """,
    unsafe_allow_html=True
)


# CSS pour les colonnes et le texte

st.markdown("""
    <style>
        html, body {
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
        }

        .grid-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            grid-template-rows: 1fr 1fr;
            width: 100vw;
            height: 100vh;
        }

        .cell {
            position: relative;
            border: 1px solid transparent;
            background-color: transparent;
        }
        .wide-hover-text {
            grid-column: 2 / 5; 
            grid-row: 2 / 3;
            position: relative;
        }

        .wide-hover-text .hover-text {
            position: absolute;
            bottom: 60px;
            left: 50%;
            transform: translateX(-50%);
            width: 55%;
            text-align: center;
            color: white;
            font-weight: bold;
            font-size: 20px;
            opacity: 0;
            transition: opacity 0.3s ease-in-out;
            background-color: rgba(0, 0, 0, 0.6);
            padding: 10px;
            border-radius: 8px;
        }

        /* Affichage du texte si hover sur colonne 1, ligne 1 */
        .cell[data-col="1"][data-row="1"]:hover ~ .wide-hover-text .hover-text {
            opacity: 1;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { transform: translateX(-50%) scale(1); }
            50% { transform: translateX(-50%) scale(1.1); }
            100% { transform: translateX(-50%) scale(1); }
        }
    </style>

    <div class="grid-container">
        <!-- Ligne 1 -->
        <div class="cell" data-col="1" data-row="1"></div>
        <div class="cell" data-col="2" data-row="1"></div>
        <div class="cell" data-col="3" data-row="1"></div>
        <div class="cell" data-col="4" data-row="1"></div>
        <div class="cell" data-col="5" data-row="1"></div>
        <!-- Ligne 2 -->
        <div class="cell" data-col="1" data-row="2"></div>
        <div class="wide-hover-text">
            <div class="hover-text">
                <span style="color:#00ff88;font-size : 20px;transform: scaleX(-1);display: inline-block;">⬎</span> Découvrez notre fond <span style="color:#00ff88;font-size : 20px;">⬎</span>
            </div>
        </div>
        <div class="cell" data-col="5" data-row="2"></div>
    </div>
""", unsafe_allow_html=True)


#----------------------------------------------------------------SECTIONS-----------------------------------

# --- Style CSS global ---
st.markdown(f"""
    <style>
    .block-container {{
        padding: 0 !important;
        width : 100%;
        box-sizing: border-box;
    }}

    html, body {{
        margin: 0;
        padding: 0;
        overflow-x: hidden;
    }}

    .section {{
        width: 100%;
        padding: 0;
        margin : 0;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    .transparent-content {{
        background-color: rgba(0, 0, 0, 0.3);
        padding: 40px;
        border-radius: 20px;
        color: white;
        font-size: 24px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- SECTION 1 : Accueil : fond transparent ---



#---SECTION 2 : Nos engagement ; critères...

#2 colonnes côte à côte
st.markdown("""
    <style>
    .modern-columns {
        display: flex;
        gap: 0px;
        justify-content: justify;
        align-items: stretch;
        margin-top: 40px;
        flex-wrap: wrap;
    }

    .column-1 {
        flex: 1;
        min-width: 300px;
        background-color: #0F1C2E;
        backdrop-filter: blur(7px);
      
        color: white;
        padding: 30px;
        border-radius: 0px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .column-2 {
        flex: 1;
        min-width: 300px;
        background-color: #1E2E40;
        backdrop-filter: blur(7px);
      
        color: white;
        padding: 30px;
        border-radius: 0px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .column-1:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.6);
        background-color: #4A6B8F;
    }
    
    .column-2:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.6);
        background-color: #4A6B8F;
    }

    .column h3 {
        font-size: 24px;
        margin-bottom: 15px;
    }

    .column p {
        font-size: 16px;
        line-height: 1.6;
        color: #ddd;
    }
    </style>

    <div class="modern-columns">
        <div class="column-1">
            <h3>Nos engagements</h3>
            <p>Dans un monde en pleine transition environnementale et numérique, notre fonds se positionne à l’intersection de ces deux dynamiques, en investissant exclusivement dans des entreprises du secteur des logiciels et services informatiques, tout en intégrant une démarche durable exigeante. <br>
            Notre approche repose sur une analyse ESG (Environnement, Social, Gouvernance) complète, permettant d’évaluer la performance extra-financière des entreprises en portefeuille. 
            Mais au-delà de cette évaluation standard, nous choisissons de mettre un accent particulier 
            sur les critères environnementaux, afin de favoriser une réelle transition vers un modèle bas carbone et responsable.
            </p>
        </div>
        <div class="column-2">
            <h4>Pourquoi ? </h4>
            <p>
            Contrairement aux idées reçues, le numérique a un impact environnemental croissant, 
            notamment à travers la consommation énergétique des infrastructures IT, 
            les chaînes de valeur globalisées et l’utilisation intensive de ressources. 
            C’est pourquoi nous accordons une attention particulière à la traçabilité carbone et 
            aux pratiques durables de ce secteur.
             </p>
        </div>
    </div>
""", unsafe_allow_html=True)

bg_image_base64 = get_base64_image("Arriere_Plan_Slogan.png")
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Dancing+Script&display=swap');
    .black-section-4 {{
        background-image: url("data:image/png;base64,{bg_image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        padding: 50px 20px;
        border-radius: 0px;
        margin-top: 0px;
        font-family: 'Dancing Script', sans-serif;
    }}
    .black-section-4:hover {{
        background-color: rgba(60, 100, 150, 0.9);
    }}
    .label {{
        font-size: 13.5px;
        line-height: 1.5;
        margin-top: 12px;
        color: #dddddd;
    }}   
    .titre {{
    text-align: center;  
    color: white;      
    font-size: 40px;   
    font-weight: bold;   
    margin-top: 20px;    
    }}
    </style>
    <div class="black-section-4">
        <div class="titre">"Programmons le futur en misant sur des acteurs responsables"</div>
    </div>
""", unsafe_allow_html=True)

# notre vision : en misant sur des acteurs responsables, nous programmons le monde de demain
st.markdown("""
<style>
.black-section {
    background: #102A43;
    backdrop-filter: blur(10px);
    padding: 60px 30px 100px;
    border-radius: 0px;
    font-family: 'Roboto', sans-serif;
    color: white;
    margin: 0;
    box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    transition: transform 0.3s ease;
}
.black-section:hover {
    background-color: #4A6B8F;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 40px;
    color: #ffffff;
    letter-spacing: 1px;
}

.circles {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 50px;
}

.item {
    width: 300px;
    text-align: center;
}

.main-circle {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1e4732, #38a169);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 14px;
    font-weight: 600;
    margin: auto;
    color: #fff;
    box-shadow: inset 0 0 10px rgba(255,255,255,0.05), 0 6px 15px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
    padding: 18px;
    line-height: 1.4;
}
.main-circle:hover {
    transform: scale(1.06);
    box-shadow: 0 10px 25px rgba(255,255,255,0.1);
}

.small-wrapper {
    margin-top: 25px;
    display: flex;
    justify-content: center;
    gap: 14px;
    flex-wrap: wrap;
}

.small {
    width: 85px;
    height: 85px;
    background: linear-gradient(135deg, #1e3d2f, #2c6b48);
    border-radius: 50%;
    color: white;
    font-size: 9px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    position: relative;
    box-shadow: 0 4px 10px rgba(0,0,0,0.25);
    transition: all 0.3s ease;
    text-align: center;
    padding: 8px;
}
.small:hover {
    background: #555;
    transform: scale(1.05);
    box-shadow: 0 6px 15px rgba(255,255,255,0.1);
}

.tooltip {
    visibility: hidden;
    opacity: 0;
    background: rgba(20, 20, 20, 0.95);
    color: #fff;
    text-align: left;
    border-radius: 8px;
    padding: 12px;
    position: absolute;
    bottom: -80px;
    left: 50%;
    transform: translateX(-50%);
    transition: opacity 0.3s ease, transform 0.3s ease;
    width: 200px;
    font-size: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    z-index: 1000;
}
.small:hover .tooltip {
    visibility: visible;
    opacity: 1;
    transform: translateX(-50%) translateY(5px);
}
</style>

<div class="black-section">
    <div class="title">Nos critères</div>
    <div class="circles">
        <!-- 1 -->
        <div class="item">
            <div class="main-circle">1<br>Impact climatique direct</div>
            <div class="small-wrapper">
                <div class="small">Emissions
                    <div class="tooltip">Évalue les émissions de gaz à effet de serre (GES) générées par l’entreprise, notamment le CO₂. </div>
                </div>
                <div class="small">Politique Energitique Efficace
                    <div class="tooltip">Mesure l'existence et la qualité des politiques internes sur l'efficacité énergétique.</div>
                </div>
                <div class="small">Usage d'énergies renouvelables 
                    <div class="tooltip">Indique la part de l’énergie totale consommée qui provient de sources renouvelables (éolien, solaire, etc.).</div>
                </div>
            </div>
        </div>
        <!-- 2 -->
        <div class="item">
            <div class="main-circle">2<br>Impact climatique indirect</div>
            <div class="small-wrapper">
                <div class="small">Gestion environnementale de la chaîne d'approvisionnement
                    <div class="tooltip">Évalue si l’entreprise pousse ses fournisseurs à adopter des pratiques écologiques.</div>
                </div>
                <div class="small">Suivi environnemental
                    <div class="tooltip">Mesure les actions mises en place pour surveiller régulièrement les impacts environnementaux (pollution, déchets, etc.).</div>
                </div>
                <div class="small">Réduction de l'impact des produits
                    <div class="tooltip">Évalue les efforts pour concevoir des produits durables, recyclables ou à faible impact écologique.</div>
                </div>
            </div>
        </div>
        <!-- 3 -->
        <div class="item">
            <div class="main-circle">3<br>Risque non climatique</div>
            <div class="small-wrapper">
                <div class="small">Utilisation des ressources
                    <div class="tooltip">Mesure la gestion responsable des ressources naturelles (matières premières, énergie, etc.).</div>
                </div>
                <div class="small">Politiques d'efficacité de gestion de l'eau
                    <div class="tooltip">Évalue les mesures prises pour économiser l’eau ou limiter sa pollution.</div>
                </div>
                <div class="small">Réduction des déchets électroniques
                    <div class="tooltip">Mesure les initiatives pour recycler ou réduire les déchets issus des équipements électroniques.</div>
                </div>
            </div>
        </div>
        <!-- 4 -->
        <div class="item">
            <div class="main-circle">4<br>Innovation</div>
            <div class="small-wrapper">
                <div class="small">Innovation Environnementale
                    <div class="tooltip">Évalue la capacité de l’entreprise à innover pour réduire son impact écologique (nouvelles technologies, procédés propres, etc.).</div>
                </div>
            </div>
        </div>
        <!-- 5 -->
        <div class="item">
            <div class="main-circle">5<br>ESG Global</div>
            <div class="small-wrapper">
                <div class="small">ESG
                    <div class="tooltip">Représente la performance globale de l’entreprise sur les critères Environnement (E), Social (S), et Gouvernance (G).</div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)



#---SECTION 3 : NOS ACTIFS ?? (mettre le code et un read csv)

st.markdown("""
    <style>
    .black-section-3 {
        background-color: #1A334D;
        backdrop-filter: blur(7px);
        padding: 50px 20px;
        border-radius: 0px;
        margin-top: 0px;
        font-family: 'Segoe UI', sans-serif;
    }
    .black-section-3:hover {
        background-color: #4C6A8E;
    }
    .label {
        font-size: 13.5px;
        line-height: 1.5;
        margin-top: 12px;
        color: #dddddd;
    }   
    .titre {
    text-align: center;  
    color: white;      
    font-size: 30px;   
    font-weight: bold;   
    margin-top: 20px;    
    }
    </style>
    <div class="black-section-3">
        <div class="titre">Nos Actifs</div>
    </div>
""", unsafe_allow_html=True)


#Rajouter le tableau à mettre après avoir lancer la fonction indice_fonds





#Section 4 : Prêt à essayer ? (simulation de portefeuille)

st.markdown(
    """
    <style>
    .modern-section {
        background: #224C57;
        backdrop-filter: blur(7px);
        padding: 60px 30px;
        border-radius: 0px;
        color: #fff;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
    .modern-section h2 {
        font-size: 2.5rem;
        margin-bottom: 20px;
    }
    .modern-section p {
        font-size: 1.2rem;
        line-height: 1.6;
        margin-bottom: 40px;
    }
    .modern-section:hover {
        background-color: #2D5E6A;
    }
    .modern-button {
        background-color:#50c878;
        color: white;
        padding: 15px 40px;
        border: none;
        border-radius: 50px;
        font-size: 1rem;
        font-weight: 600;
        text-decoration: none;
        margin: 10px;
        transition: background-color 0.3s, transform 0.3s;
    }
    .modern-button:hover {
        background-color: #45b26a;
        transform: translateY(-5px);
    }
    </style>
    <div class="modern-section">
        <h2>Prêt à essayer ?</h2>
        <p>Testez notre simulation de portefeuille et découvrez comment optimiser votre stratégie d'investissement en quelques clics.</p>
        <a href="/page_1" class="modern-button">Simuler maintenant</a>
    </div>
    """, 
    unsafe_allow_html=True
)

