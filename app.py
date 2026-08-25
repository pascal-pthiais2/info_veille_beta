import streamlit as st
from groq import Groq

# 1. Configuration de la page
st.set_page_config(page_title="JuriPulse Studio", page_icon="⚡", layout="centered")

# 2. Clé Groq (Pensez à remettre votre vraie clé gsk_)
MA_CLE_GROQ = "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" 
client = Groq(api_key=MA_CLE_GROQ)

# 3. Le Design System (Désactivation forcée de l'espace blanc du haut)
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc !important; color: #0f172a !important; font-family: "Inter", sans-serif !important; }
    header, footer, [data-testid="stHeader"] { visibility: hidden !important; height: 0px !important; }
    
    /* ANCHOR : Cette règle force l'application à démarrer tout en haut sans marge blanche */
    .block-container { 
        max-width: 760px !important; 
        padding-top: 0px !important; 
        padding-bottom: 40px !important; 
        margin-top: 0px !important;
    }
    
    /* Élimination de TOUS les blocs vides ou espaces générés par st.write ou st.empty */
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stVerticalBlock"],
    div[data-testid="element-container"],
    .stMarkdownContainer {
        border: none !important; 
        background: transparent !important; 
        box-shadow: none !important;
    }
    
    /* Masquage forcé des textes ou paragraphes vides de Streamlit */
    p:empty, div:empty, span:empty { display: none !important; height: 0px !important; margin: 0 !important; padding: 0 !important; }

    /* Barre de Navigation fine */
    .navbar { display: flex; align-items: center; justify-content: space-between; height: 56px; background-color: #ffffff; border-bottom: 1px solid #e2e8f0; margin-bottom: 24px; padding: 0 16px; border-radius: 0 0 8px 8px; }
    .nav-logo-container { display: flex; align-items: center; gap: 8px; }
    .nav-icon { background: linear-gradient(135deg, #635bff 0%, #00d4b6 100%); width: 16px; height: 16px; border-radius: 4px; }
    .nav-logo-text { font-size: 14px !important; font-weight: 600 !important; color: #0a2540; }
    .nav-links { display: flex; gap: 20px; font-size: 12px; color: #64748b; font-weight: 500; }
    
    /* Panneau d'atelier unique */
    .app-workspace { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 12px !important; padding: 32px !important; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05) !important; }
    
    /* Zone de texte */
    textarea { background-color: #f8fafc !important; border: 1px solid #e2e8f0 !important; border-radius: 6px !important; color: #0f172a !important; padding: 14px !important; font-size: 14px !important; }
    
    /* Bouton d'action */
    .stButton > button { background-color: #635bff !important; color: #ffffff !important; border: none !important; border-radius: 6px !important; padding: 12px 24px !important; font-weight: 500 !important; font-size: 14px !important; width: 100% !important; box-shadow: 0 2px 4px rgba(99, 91, 255, 0.15) !important; }
    .stButton > button:hover { background-color: #0a2540 !important; }
    
    /* Boîte de résultat */
    .result-box { background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-top: 25px; }
    .label-caps { font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
    .value-text { font-size: 14px; color: #1e293b; line-height: 1.5; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# 4. Affichage de la Barre de Navigation
st.markdown("""
    <div class="navbar">
        <div class="nav-logo-container"><div class="nav-icon"></div><div class="nav-logo-text">JuriPulse</div></div>
        <div class="nav-links"><div>Dashboard</div><div>Veille Automatique</div><div>Documentation</div></div>
        <div style="font-size: 12px; color: #635bff; font-weight:600; cursor:pointer;">Mon Espace →</div>
    </div>
""", unsafe_allow_html=True)

# 5. L'espace de travail central propre
st.markdown('<div class="app-workspace">', unsafe_allow_html=True)
st.markdown("<h4 style='margin:0 0 4px 0; color:#0a2540; font-size:18px;'>📥 Analyse de document</h4>", unsafe_allow_html=True)
st.markdown("<p style='margin:0 0 20px 0; color:#64748b; font-size:14px;'>Collez un décret, une loi ou un arrêt brut pour en extraire instantanément la structure.</p>", unsafe_allow_html=True)

# Zone de saisie sans aucun titre
texte_utilisateur = st.text_area(
    label="",
    placeholder="Ex: Décret modifiant la taxe foncière des locaux commerciaux...",
    height=140,
    label_visibility="collapsed"
)

lancer_analyse = st.button("🚀 Exécuter l'analyse sémantique")

if lancer_analyse and texte_utilisateur:
    consigne = f"Tu es un robot juriste français ultra-précis. Analyse ce texte de loi et extrait CATEGORIE, RESUME et DATE : {texte_utilisateur}"
    with st.spinner("⏳ Calcul en cours..."):
        reponse = client.chat.completions.create(
            messages=[{"role": "user", "content": consigne}],
            model="openai/gpt-oss-20b",
        )
        resultat_ia = reponse.choices[0].message.content
    
    st.markdown(f"""
    <div class="result-box">
        <div class="label-caps">📋 Métadonnées juridiques extraites</div>
        <div class="value-text" style="white-space: pre-wrap;">{resultat_ia}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
