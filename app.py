# ============================================
# ENHANCED ENERGY PERFORMANCE DASHBOARD
# ============================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import numpy as np
import base64
warnings.filterwarnings('ignore')

def img_to_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

# ============================================
# PAGE SETUP
# ============================================
st.set_page_config(
    page_title="Clarke Energy Fuel Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LANGUAGE DICTIONARIES
# ============================================
TEXTS = {
    "fr": {
        "title": "Tableau de Bord Clarke Energy",
        "subtitle": "Gestion & Analyse de la Consommation du Carburant",
        "dashboard_header": "Indicateurs de Performance",
        "comparison_header": "Comparaisons de Performance",
        "details_header": "Tableaux de Performance Détaillés",
        "optimization_header": "Optimisation Énergétique",
        "reporting_header": "Rapports & Export",
        "validation_header": "Validation des Données",
        "total_km": "Kilométrage Total",
        "total_consumption": "Consommation Totale",
        "total_cost": "Coût Total Carburant",
        "total_co2": "Émissions CO₂",
        "km_driver": "Kilométrage Conducteur",
        "cons_driver": "Consommation Conducteur",
        "cost_driver": "Coût Conducteur",
        "avg_driver": "Moyenne/100km",
        "potential_savings": "Économie Potentielle",
        "savings_cost": "Économie en DT",
        "co2_savings": "Économie CO₂",
        "driver_perf": "Performance par Conducteur",
        "vehicle_perf": "Performance par Véhicule",
        "transactions": "Détails des Transactions",
        "upload_file": "📤 Importer le fichier de données",
        "upload_help": "Format attendu : .csv ou .xlsx",
        "analysis_filters": "Filtres d'Analyse",
        "select_driver": "Conducteur",
        "driver_help": "Choisir un conducteur pour voir ses détails",
        "filter_vehicles": "Véhicule(s)",
        "select_period": "Période d'analyse",
        "alert_thresholds": "Seuils d'Alerte",
        "consumption_threshold": "Seuil conso/100km (L)",
        "threshold_help": "Seuil pour mettre en évidence les conducteurs",
        "settings": "Paramètres",
        "fuel_price_ssp": "SSP (DT/L)",
        "fuel_price_go": "GO (DT/L)",
        "fuel_price_goss": "GOSS (DT/L)",
        "fuel_price_help": "Prix par litre en Dinars Tunisiens",
        "co2_factors": "Facteurs d'Émission CO₂",
        "co2_ssp": "SSP (kg/L)",
        "co2_go": "GO (kg/L)",
        "co2_goss": "GOSS (kg/L)",
        "co2_help": "Facteur d'émission par type de carburant",
        "anomaly_settings": "Détection des Anomalies",
        "lower_limit": "Limite inf. (L/100km)",
        "upper_limit": "Limite sup. (L/100km)",
        "anomaly_help": "Transactions hors plage exclues des calculs",
        "driver_analysis": "Analyse par Conducteur",
        "top_drivers": "Top Conducteurs par Consommation totale",
        "consumption_trend": "Évolution Mensuelle de la Consommation",
        "efficiency_scatter": "Efficacité Énergétique : Consommation vs Distance",
        "distribution_chart": "Répartition de la Consommation par Conducteur & Véhicule",
        "processed_data": "Données Traitées (CSV)",
        "driver_perf_csv": "Performance Conducteurs",
        "vehicle_perf_csv": "Performance Véhicules",
        "summary_report": "Rapport Sommaire",
        "welcome": "Bienvenue sur votre Dashboard Clarke Energy",
        "welcome_sub": "Commencez par télécharger votre fichier de données dans la barre latérale",
        "data_loaded": "Données chargées",
        "anomalies_excluded": "anomalies détectées et exclues des calculs KPIs",
        "valid_transactions": "transactions valides analysées",
        "no_anomalies": "Aucune anomalie de consommation détectée",
        "high_consumption_warning": "conducteur(s) dépassent le seuil",
        "anomalies_detected": "Anomalies détectées dans les données :",
        "no_major_anomalies": "Aucune anomalie majeure détectée",
        "missing_data_detected": "Données manquantes détectées par conducteur",
        "missing_data_table": "Tableau des données manquantes par conducteur",
        "missing_vehicle": "Véhicule manquant",
        "missing_km_before": "Km avant manquant/0",
        "missing_km_after": "Km après manquant/0",
        "missing_product": "Produit manquant",
        "total_missing": "Total manquantes",
        "driver": "Chauffeur",
        "times": "fois",
        "new_features": "Fonctionnalités",
        "features_list": """• Analyse par conducteur et véhicule\n• KPIs de performance énergétique\n• Détection d'anomalies automatisée\n• Visualisations interactives\n• Rapports d'optimisation""",
        "metrics_calculated": "KPIs Calculées",
        "metrics_list": """• Kilométrage parcouru\n• Consommation/100km\n• Coût au kilomètre (DT/km)\n• Émissions CO₂ (SSP & Diesel)\n• Écart vs moyenne\n• Potentiel d'économie""",
        "how_to_use": "Comment Utiliser",
        "usage_list": """1. Téléchargez vos données\n2. Appliquez les filtres\n3. Analysez les KPIs\n4. Exportez les rapports\n5. Optimisez la performance""",
        "data_format": "Format de Données Requis",
        "required_columns": "Votre fichier doit contenir ces colonnes :",
        "efficiency_target": "Objectif d'efficacité (L/100km)",
        "footer": "Clarke Energy Dashboard v1.0  ·  © 2026  ·  Tous droits réservés"
    },
    "en": {
        "title": "Clarke Energy Fuel Dashboard",
        "subtitle": "Fuel Consumption Management & Analysis",
        "dashboard_header": "Performance Indicators",
        "comparison_header": "Performance Comparisons",
        "details_header": "Detailed Performance Tables",
        "optimization_header": "Energy Optimization",
        "reporting_header": "Reports & Export",
        "validation_header": "Data Validation",
        "total_km": "Total Distance",
        "total_consumption": "Total Consumption",
        "total_cost": "Total Fuel Cost",
        "total_co2": "CO₂ Emissions",
        "km_driver": "Driver Distance",
        "cons_driver": "Driver Consumption",
        "cost_driver": "Driver Cost",
        "avg_driver": "Average/100km",
        "potential_savings": "Potential Savings",
        "savings_cost": "Savings in DT",
        "co2_savings": "CO₂ Savings",
        "driver_perf": "Performance by Driver",
        "vehicle_perf": "Performance by Vehicle",
        "transactions": "Transaction Details",
        "upload_file": "📤 Upload your data file",
        "upload_help": "Expected format: .csv or .xlsx",
        "analysis_filters": "Analysis Filters",
        "select_driver": "Driver",
        "driver_help": "Choose a driver to see details",
        "filter_vehicles": "Vehicle(s)",
        "select_period": "Analysis Period",
        "alert_thresholds": "Alert Thresholds",
        "consumption_threshold": "Consumption/100km threshold (L)",
        "threshold_help": "Set threshold to highlight drivers",
        "settings": "Settings",
        "fuel_price_ssp": "SSP (DT/L)",
        "fuel_price_go": "GO (DT/L)",
        "fuel_price_goss": "GOSS (DT/L)",
        "fuel_price_help": "Price per liter in Tunisian Dinars",
        "co2_factors": "CO₂ Emission Factors",
        "co2_ssp": "SSP (kg/L)",
        "co2_go": "GO (kg/L)",
        "co2_goss": "GOSS (kg/L)",
        "co2_help": "Emission factor by fuel type",
        "anomaly_settings": "Anomaly Detection",
        "lower_limit": "Lower limit (L/100km)",
        "upper_limit": "Upper limit (L/100km)",
        "anomaly_help": "Transactions outside this range will be excluded",
        "driver_analysis": "Driver Analysis",
        "top_drivers": "Top Drivers by Total Consumption",
        "consumption_trend": "Monthly Consumption Evolution",
        "efficiency_scatter": "Energy Efficiency: Consumption vs Distance",
        "distribution_chart": "Consumption Distribution by Driver & Vehicle",
        "processed_data": "Processed Data (CSV)",
        "driver_perf_csv": "Driver Performance",
        "vehicle_perf_csv": "Vehicle Performance",
        "summary_report": "Summary Report",
        "welcome": "Welcome to Clarke Energy Dashboard",
        "welcome_sub": "Start by uploading your data file in the sidebar",
        "data_loaded": "Data loaded",
        "anomalies_excluded": "anomalies detected and excluded from KPI calculations",
        "valid_transactions": "valid transactions analyzed",
        "no_anomalies": "No consumption anomalies detected",
        "high_consumption_warning": "driver(s) exceed threshold",
        "anomalies_detected": "Anomalies detected in data:",
        "no_major_anomalies": "No major anomalies detected",
        "missing_data_detected": "Missing data detected by driver",
        "missing_data_table": "Missing data table by driver",
        "missing_vehicle": "Missing vehicle",
        "missing_km_before": "Missing/zero km before",
        "missing_km_after": "Missing/zero km after",
        "missing_product": "Missing product",
        "total_missing": "Total missing",
        "driver": "Driver",
        "times": "times",
        "new_features": "Features",
        "features_list": """• Driver and vehicle analysis\n• Energy performance KPIs\n• Automated anomaly detection\n• Interactive visualizations\n• Optimization reports""",
        "metrics_calculated": "Calculated Metrics",
        "metrics_list": """• Distance traveled\n• Consumption/100km\n• Cost per kilometer (DT/km)\n• CO₂ emissions (SSP & Diesel)\n• Deviation vs average\n• Savings potential""",
        "how_to_use": "How to Use",
        "usage_list": """1. Upload your data\n2. Apply filters\n3. Analyze KPIs\n4. Export reports\n5. Optimize performance""",
        "data_format": "Required Data Format",
        "required_columns": "Your file must contain these columns:",
        "efficiency_target": "Efficiency target (L/100km)",
        "footer": "Clarke Energy Dashboard v1.0  ·  © 2026  ·  All rights reserved"
    }
}

def tr(key):
    lang = st.session_state.get('language', 'fr')
    return TEXTS[lang].get(key, key)

# ============================================
# CUSTOM STYLING — POLISHED UI
# ============================================
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=DM+Serif+Display&display=swap');

/* ── Design tokens ── */
:root {
    --brand:        #A82C14;
    --brand-deep:   #4F1111;
    --brand-hover:  #8B2410;
    --brand-pale:   #FDF1EF;
    --brand-tint:   #FCD2D2;
    --success:      #0F9B6B;
    --success-bg:   #ECFDF5;
    --warning:      #B45309;
    --warning-bg:   #FFFBEB;
    --gray-50:      #F9FAFB;
    --gray-100:     #F3F4F6;
    --gray-200:     #E5E7EB;
    --gray-400:     #9CA3AF;
    --gray-600:     #4B5563;
    --gray-800:     #1F2937;
    --radius:       10px;
    --radius-lg:    14px;
    --shadow:       0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md:    0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
}

/* ── Base typography ── */
html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif;
    color: var(--gray-800);
}

/* ── Top accent line ── */
.stApp::before {
    content: '';
    display: block;
    height: 3px;
    background: linear-gradient(90deg, var(--brand-deep), var(--brand), #E05C3A);
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 9999;
}

/* ── Main header ── */
.main-header {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    background: linear-gradient(135deg, var(--brand-deep) 0%, var(--brand) 60%, #D44A2A 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin-bottom: 0.25rem;
    padding-top: 0.5rem;
}

.page-subtitle {
    text-align: center;
    color: var(--gray-600);
    font-size: 0.95rem;
    font-weight: 400;
    letter-spacing: 0.3px;
    margin-bottom: 1.5rem;
}

/* ── Section headers ── */
.section-header {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--brand);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    border-bottom: 2px solid var(--brand-tint);
    padding-bottom: 0.5rem;
    margin-top: 2.5rem;
    margin-bottom: 1rem;
}

/* ── Status cards ── */
.warning-card {
    background: var(--warning-bg);
    border: 1px solid #FDE68A;
    border-left: 4px solid #F59E0B;
    padding: 0.9rem 1.1rem;
    border-radius: var(--radius);
    font-size: 0.9rem;
    color: var(--warning);
    margin: 0.5rem 0;
}

.success-card {
    background: var(--success-bg);
    border: 1px solid #A7F3D0;
    border-left: 4px solid var(--success);
    padding: 0.9rem 1.1rem;
    border-radius: var(--radius);
    font-size: 0.9rem;
    color: var(--success);
    margin: 0.5rem 0;
}

.alert-card {
    background: var(--brand-pale);
    border: 1px solid var(--brand-tint);
    border-left: 4px solid var(--brand);
    padding: 0.9rem 1.1rem;
    border-radius: var(--radius);
    font-size: 0.9rem;
    color: var(--brand-deep);
    margin: 0.5rem 0;
}

/* ── Metric cards (st.metric override) ── */
[data-testid="stMetric"] {
    background: #fff;
    border: 1px solid var(--gray-200);
    border-top: 3px solid var(--brand);
    border-radius: var(--radius-lg);
    padding: 1.1rem 1.2rem 0.9rem !important;
    box-shadow: var(--shadow);
    transition: box-shadow 0.2s ease;
}
[data-testid="stMetric"]:hover {
    box-shadow: var(--shadow-md);
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.6px !important;
    color: var(--gray-600) !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: var(--gray-800) !important;
    letter-spacing: -0.5px !important;
    line-height: 1.2 !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
}

/* ── Estimation box ── */
.estimation-box {
    background: var(--gray-50);
    border: 1px solid var(--gray-200);
    border-left: 3px solid var(--brand);
    padding: 0.6rem 0.8rem;
    border-radius: var(--radius);
    margin-top: 0.5rem;
    font-size: 0.82rem;
    color: var(--gray-600);
    line-height: 1.5;
}
.estimation-box p { margin: 0; }
.estimation-highlight {
    font-weight: 600;
    color: var(--brand);
}

/* ── Download buttons ── */
.stDownloadButton > button {
    background: #fff !important;
    color: var(--brand) !important;
    border: 1.5px solid var(--brand) !important;
    border-radius: var(--radius) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 0.8rem !important;
    transition: all 0.15s ease !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    background: var(--brand) !important;
    color: #fff !important;
    border-color: var(--brand) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #FAFAFA !important;
    border-right: 1px solid var(--gray-200) !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label {
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--gray-600) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.4px !important;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    color: var(--brand) !important;
    background: var(--brand-pale) !important;
    padding: 0.4rem 0.6rem !important;
    border-radius: 6px !important;
    margin-bottom: 0.6rem !important;
    margin-top: 0.8rem !important;
}

/* ── Expanders ── */
[data-testid="stExpander"] {
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius) !important;
    background: #fff !important;
    box-shadow: var(--shadow) !important;
    margin-bottom: 0.4rem !important;
}
[data-testid="stExpander"] summary {
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    color: var(--gray-800) !important;
    padding: 0.7rem 1rem !important;
}
[data-testid="stExpander"] summary:hover {
    color: var(--brand) !important;
}

/* ── DataFrames ── */
.stDataFrame {
    border: 1px solid var(--gray-200) !important;
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow) !important;
}
.stDataFrame thead th {
    background: var(--gray-50) !important;
    color: var(--gray-800) !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.4px !important;
    border-bottom: 2px solid var(--gray-200) !important;
}
.stDataFrame tbody tr:hover td {
    background: var(--brand-pale) !important;
}

/* ── Select / Multiselect / Input focus ── */
[data-baseweb="select"] > div:focus-within,
[data-baseweb="input"] > div:focus-within {
    border-color: var(--brand) !important;
    box-shadow: 0 0 0 2px rgba(168,44,20,0.12) !important;
}

/* ── Tabs (if used) ── */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: 2px solid var(--gray-200) !important;
    gap: 0.25rem !important;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: var(--gray-600) !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 0.5rem 1rem !important;
}
.stTabs [aria-selected="true"] {
    color: var(--brand) !important;
    border-bottom: 2px solid var(--brand) !important;
}

/* ── Slider accent ── */
[data-testid="stSlider"] .stSlider > div > div > div > div {
    background: var(--brand) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--gray-200) !important;
    margin: 1.5rem 0 !important;
}

/* ── Compact input ── */
.compact-input {
    font-size: 0.85rem;
}

/* ── Footer ── */
.page-footer {
    text-align: center;
    font-size: 0.75rem;
    color: var(--gray-400);
    letter-spacing: 0.3px;
    padding: 1rem 0 0.5rem;
}
.page-footer span {
    color: var(--brand);
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# PLOTLY CHART THEME HELPER
# ============================================
BRAND_COLORS = ["#A82C14", "#7e7c76", "#C84B30", "#4F1111", "#D97B60", "#2D1818", "#E8A090"]

def style_chart(fig, height=400):
    """Apply consistent brand styling to any Plotly figure."""
    fig.update_layout(
        height=height,
        font=dict(family="DM Sans, sans-serif", size=12, color="#374151"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=48, b=32, l=8, r=8),
        title_font=dict(size=13, color="#1F2937", family="DM Sans, sans-serif"),
        title_x=0.0,
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#E5E7EB",
            borderwidth=1,
            font=dict(size=11),
        ),
        xaxis=dict(
            gridcolor="#F3F4F6",
            linecolor="#E5E7EB",
            tickfont=dict(size=11),
            showgrid=False,
        ),
        yaxis=dict(
            gridcolor="#F3F4F6",
            linecolor="rgba(0,0,0,0)",
            tickfont=dict(size=11),
        ),
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="#E5E7EB",
            font=dict(size=12, family="DM Sans, sans-serif"),
        ),
    )
    return fig

# ============================================
# DATA PROCESSING FUNCTIONS
# ============================================
def rename_columns_by_position(df):
    column_mapping = {
        0: 'Ticket', 1: 'Carte N°', 2: 'Carte libelle', 3: 'Carte type',
        4: 'Carte format', 5: 'N° Client', 6: 'Nom Client', 7: 'Nom Station',
        8: 'Chauffeur', 9: 'Solde avant', 10: 'Solde après', 11: 'Km avant',
        12: 'KM après', 13: 'Véhicule', 14: 'Code Chauffeur',
        15: 'Type Transaction', 16: 'Mode Payement', 17: 'Produit',
        18: 'Quantité', 19: 'Montant', 20: 'P.U', 21: 'Consommation moyenne',
        22: 'Hors ligne', 23: 'Date', 24: 'Heure'
    }
    new_names = [column_mapping.get(i, df.columns[i]) for i in range(len(df.columns))]
    df.columns = new_names
    return df

def preprocess_data(df):
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.strip()

    # Convert all numeric columns upfront — prevents ArrowStringArray errors on
    # Streamlit Cloud where pandas uses PyArrow-backed dtypes by default
    numeric_cols = ['Km avant', 'KM après', 'Quantité', 'Montant', 'P.U',
                    'Solde avant', 'Solde après', 'Consommation moyenne']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    if 'Chauffeur' in df_clean.columns and 'Carte libelle' in df_clean.columns:
        mask = (df_clean['Chauffeur'].isna()) | (df_clean['Chauffeur'] == '')
        df_clean.loc[mask, 'Chauffeur'] = df_clean.loc[mask, 'Carte libelle']

    if 'Date' in df_clean.columns:
        df_clean['Date'] = pd.to_datetime(df_clean['Date'], dayfirst=True, errors='coerce')
        df_clean['Month'] = df_clean['Date'].dt.strftime('%Y-%m')
        df_clean['Week'] = df_clean['Date'].dt.isocalendar().week

    if all(col in df_clean.columns for col in ['Km avant', 'KM après']):
        df_clean['Kilométrage parcouru'] = df_clean['KM après'] - df_clean['Km avant']

    if all(col in df_clean.columns for col in ['Quantité', 'Kilométrage parcouru']):
        mask = df_clean['Kilométrage parcouru'] > 0
        df_clean.loc[mask, 'Consommation/100km'] = (
            df_clean.loc[mask, 'Quantité'] / df_clean.loc[mask, 'Kilométrage parcouru']
        ) * 100
        df_clean.loc[~mask, 'Consommation/100km'] = np.nan

    return df_clean

def create_missing_data_table(df):
    if 'Chauffeur' not in df.columns:
        return pd.DataFrame()

    missing_data = []
    for driver in df['Chauffeur'].unique():
        if pd.isna(driver):
            continue
        dd = df[df['Chauffeur'] == driver]
        mv = mk_b = mk_a = mp = 0

        if 'Véhicule' in df.columns:
            mv = dd['Véhicule'].isna().sum() + (dd['Véhicule'].astype(str).str.strip() == '').sum()
        if 'Km avant' in df.columns:
            n = pd.to_numeric(dd['Km avant'], errors='coerce')
            mk_b = n.isna().sum() + (n == 0).sum()
        if 'KM après' in df.columns:
            n = pd.to_numeric(dd['KM après'], errors='coerce')
            mk_a = n.isna().sum() + (n == 0).sum()
        if 'Produit' in df.columns:
            mp = dd['Produit'].isna().sum() + (dd['Produit'].astype(str).str.strip() == '').sum()

        total = mv + mk_b + mk_a + mp
        if total > 0:
            missing_data.append({
                tr('driver'): driver,
                tr('missing_vehicle'): int(mv),
                tr('missing_km_before'): int(mk_b),
                tr('missing_km_after'): int(mk_a),
                tr('missing_product'): int(mp),
                tr('total_missing'): int(total)
            })

    if missing_data:
        return pd.DataFrame(missing_data).sort_values(tr('total_missing'), ascending=False)
    return pd.DataFrame()

def check_missing_data(df):
    missing_summary = {}
    if 'Chauffeur' not in df.columns:
        return missing_summary
    for driver in df['Chauffeur'].unique():
        if pd.isna(driver):
            continue
        dd = df[df['Chauffeur'] == driver]
        missing_counts = {}
        if 'Véhicule' in df.columns:
            v = dd['Véhicule'].isna().sum() + (dd['Véhicule'].astype(str).str.strip() == '').sum()
            if v > 0: missing_counts['vehicle'] = v
        if 'Km avant' in df.columns:
            n = pd.to_numeric(dd['Km avant'], errors='coerce')
            c = n.isna().sum() + (n == 0).sum()
            if c > 0: missing_counts['km_before'] = c
        if 'KM après' in df.columns:
            n = pd.to_numeric(dd['KM après'], errors='coerce')
            c = n.isna().sum() + (n == 0).sum()
            if c > 0: missing_counts['km_after'] = c
        if 'Produit' in df.columns:
            p = dd['Produit'].isna().sum() + (dd['Produit'].astype(str).str.strip() == '').sum()
            if p > 0: missing_counts['product'] = p
        if missing_counts:
            missing_summary[driver] = missing_counts
    return missing_summary

def remove_rows_with_missing_data(df):
    df_clean = df.copy()
    masks = []

    if 'Véhicule' in df_clean.columns:
        masks.append(df_clean['Véhicule'].isna() | (df_clean['Véhicule'].astype(str).str.strip() == ''))
    if 'Km avant' in df_clean.columns:
        n = pd.to_numeric(df_clean['Km avant'], errors='coerce')
        masks.append(n.isna() | (n == 0))
    if 'KM après' in df_clean.columns:
        n = pd.to_numeric(df_clean['KM après'], errors='coerce')
        masks.append(n.isna() | (n == 0))
    if 'Produit' in df_clean.columns:
        masks.append(df_clean['Produit'].isna() | (df_clean['Produit'].astype(str).str.strip() == ''))

    if masks:
        combined = masks[0]
        for m in masks[1:]:
            combined = combined | m
        removed = df_clean[combined].copy()
        df_clean = df_clean[~combined]
    else:
        removed = pd.DataFrame()

    return df_clean, removed

def calculate_driver_metrics(df_clean, df_original, lang='fr'):
    if 'Chauffeur' not in df_clean.columns:
        return pd.DataFrame()

    metrics_clean = df_clean.groupby('Chauffeur').agg({
        'Kilométrage parcouru': 'sum',
        'Quantité': 'sum',
        'Montant': 'sum',
        'Consommation/100km': 'mean'
    }).round(2)
    metrics_clean.columns = ['Kilométrage total', 'Consommation totale', 'Dépense totale',
                              'Consommation moyenne/100km']

    if 'Consommation/100km' in df_clean.columns:
        overall_avg = df_clean['Consommation/100km'].mean()
        metrics_clean['Écart vs moyenne'] = (
            (metrics_clean['Consommation moyenne/100km'] - overall_avg) / overall_avg * 100
        ).round(1)

    if 'Chauffeur' in df_original.columns:
        tx_counts = df_original.groupby('Chauffeur')['Ticket'].count()
        tx_counts.name = 'Nombre de transactions'
        metrics = pd.concat([metrics_clean, tx_counts], axis=1)
        for col in ['Nombre de transactions', 'Kilométrage total', 'Consommation totale',
                    'Dépense totale', 'Consommation moyenne/100km', 'Écart vs moyenne']:
            if col in metrics.columns:
                metrics[col] = metrics[col].fillna(0)
        metrics['Nombre de transactions'] = metrics['Nombre de transactions'].astype(int)
    else:
        metrics = metrics_clean
        metrics['Nombre de transactions'] = df_clean.groupby('Chauffeur')['Ticket'].count()

    metrics = metrics.sort_values('Consommation totale', ascending=False)

    if lang == 'en':
        metrics.columns = ['Total Distance', 'Total Consumption', 'Total Cost',
                           'Average Consumption/100km', 'Deviation vs Average',
                           'Number of Transactions']
    return metrics

def calculate_vehicle_metrics(df, lang='fr'):
    if 'Véhicule' not in df.columns:
        return pd.DataFrame()

    if 'Produit' in df.columns:
        vehicle_products = df.groupby('Véhicule')['Produit'].agg(
            lambda x: ', '.join(sorted(x.unique()))
        ).rename('Énergie' if lang == 'fr' else 'Fuel')
    else:
        vehicle_products = pd.Series(index=df['Véhicule'].unique(), data='N/A')
        vehicle_products.name = 'Énergie' if lang == 'fr' else 'Fuel'

    metrics = df.groupby('Véhicule').agg({
        'Kilométrage parcouru': 'sum',
        'Quantité': 'sum',
        'Montant': 'sum',
        'Consommation/100km': 'mean'
    }).round(2)
    metrics = metrics.join(vehicle_products)

    if lang == 'fr':
        metrics.columns = ['Kilométrage total', 'Consommation totale', 'Dépense totale',
                           'Consommation moyenne/100km', 'Énergie']
    else:
        metrics.columns = ['Total Distance', 'Total Consumption', 'Total Cost',
                           'Average Consumption/100km', 'Fuel']

    sort_col = 'Consommation totale' if lang == 'fr' else 'Total Consumption'
    return metrics.sort_values(sort_col, ascending=False)

# ============================================
# VISUALIZATION FUNCTIONS
# ============================================
def create_driver_comparison_chart(df, metric='Consommation totale', top_n=15, lang='fr'):
    if 'Chauffeur' not in df.columns:
        return None

    if lang == 'fr':
        driver_metrics = calculate_driver_metrics(df, df, lang='fr')
        title = f"Top {top_n} Conducteurs — {metric}"
        x_label = 'Conducteur'
    else:
        driver_metrics = calculate_driver_metrics(df, df, lang='en')
        metric_map = {
            'Consommation totale': 'Total Consumption',
            'Dépense totale': 'Total Cost',
            'Kilométrage total': 'Total Distance'
        }
        metric = metric_map.get(metric, metric)
        title = f"Top {top_n} Drivers — {metric}"
        x_label = 'Driver'

    if driver_metrics.empty:
        return None

    top_drivers = driver_metrics.nlargest(top_n, metric)

    fig = px.bar(
        top_drivers,
        x=top_drivers.index,
        y=metric,
        title=title,
        labels={'x': x_label, metric: metric},
        color=metric,
        color_continuous_scale=["#FFDDD8", "#C84B30", "#4F1111"],
    )
    fig.update_traces(
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>" + metric + ": %{y:,.1f}<extra></extra>"
    )
    fig.update_layout(
        xaxis_tickangle=-40,
        showlegend=False,
        coloraxis_showscale=False,
    )
    return style_chart(fig, height=380)


def create_monthly_consumption_chart(df, year, lang='fr'):
    if 'Date' not in df.columns or 'Quantité' not in df.columns:
        return None

    df_year = df[df['Date'].dt.year == year].copy()
    if df_year.empty:
        fig = go.Figure()
        fig.add_annotation(
            text=("Aucune donnée pour l'année sélectionnée" if lang == 'fr' else "No data for selected year"),
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color="#9CA3AF")
        )
        return style_chart(fig, height=380)

    df_year['Month'] = df_year['Date'].dt.to_period('M')
    monthly = df_year.groupby('Month').agg({'Quantité': 'sum', 'Montant': 'sum'}).reset_index()
    monthly['Month_dt'] = monthly['Month'].dt.start_time
    monthly = monthly.sort_values('Month_dt')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly['Month_dt'],
        y=monthly['Quantité'],
        mode='lines+markers',
        name=('Consommation (L)' if lang == 'fr' else 'Consumption (L)'),
        line=dict(color="#A82C14", width=2.5),
        marker=dict(size=6, color="#A82C14", line=dict(color="white", width=1.5)),
        fill='tozeroy',
        fillcolor='rgba(168,44,20,0.07)',
        yaxis='y',
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:,.0f} L<extra></extra>"
    ))
    fig.add_trace(go.Bar(
        x=monthly['Month_dt'],
        y=monthly['Montant'],
        name=('Coût (DT)' if lang == 'fr' else 'Cost (DT)'),
        marker=dict(color='rgba(0,0,0,0)'),
        yaxis='y2',
        hovertemplate="<b>%{x|%b %Y}</b><br>%{y:,.0f} DT<extra></extra>"
    ))

    title = tr("consumption_trend") + f" · {year}"
    y1_label = 'Consommation (L)' if lang == 'fr' else 'Consumption (L)'
    y2_label = 'Coût (DT)' if lang == 'fr' else 'Cost (DT)'

    fig.update_layout(
        title=title,
        xaxis=dict(title='', tickformat="%b %Y"),
        yaxis=dict(
            title=dict(text=y1_label, font=dict(size=11)),
            color='#A82C14',
        ),
        yaxis2=dict(
            title=dict(text=y2_label, font=dict(size=11)),
            color='#A82C14',
            overlaying='y', side='right', showgrid=False,
        ),
        hovermode='x unified',
        showlegend=False,
    )
    return style_chart(fig, height=380)


def create_efficiency_scatter_plot(df, lang='fr'):
    if not all(col in df.columns for col in ['Kilométrage parcouru', 'Consommation/100km']):
        return None

    x_col, y_col = 'Kilométrage parcouru', 'Consommation/100km'
    if lang == 'fr':
        x_label, y_label = 'Distance parcourue (km)', 'Consommation (L/100km)'
        title = "Efficacité Énergétique · Consommation vs Distance"
    else:
        x_label, y_label = 'Distance traveled (km)', 'Consumption (L/100km)'
        title = "Energy Efficiency · Consumption vs Distance"

    hover_cols = ['Chauffeur', 'Véhicule'] if all(c in df.columns for c in ['Chauffeur', 'Véhicule']) else None

    fig = px.scatter(
        df, x=x_col, y=y_col,
        color='Chauffeur' if 'Chauffeur' in df.columns else None,
        size='Quantité',
        title=title,
        labels={x_col: x_label, y_col: y_label},
        hover_data=hover_cols,
        color_discrete_sequence=BRAND_COLORS,
        opacity=0.75,
    )
    avg_c = df['Consommation/100km'].mean()
    avg_d = df['Kilométrage parcouru'].mean()
    avg_c_lbl = f"{'Moyenne' if lang=='fr' else 'Avg'}: {avg_c:.1f} L/100km"
    avg_d_lbl = f"{'Moyenne' if lang=='fr' else 'Avg'}: {avg_d:.0f} km"

    fig.add_hline(y=avg_c, line_dash="dot", line_color="#A82C14", line_width=1.5,
                  annotation_text=avg_c_lbl, annotation_font_size=11)
    fig.add_vline(x=avg_d, line_dash="dot", line_color="#4F1111", line_width=1.5,
                  annotation_text=avg_d_lbl, annotation_font_size=11)
    return style_chart(fig, height=420)


def create_combined_distribution_chart(df, lang='fr'):
    if 'Véhicule' not in df.columns or 'Chauffeur' not in df.columns:
        return None

    df_c = df.copy()
    df_c['Chauffeur_Véhicule'] = df_c['Chauffeur'] + ' (' + df_c['Véhicule'] + ')'
    combined_dist = df_c.groupby('Chauffeur_Véhicule')['Quantité'].sum().nlargest(15)

    if combined_dist.empty:
        return None

    fig = px.pie(
        combined_dist, values=combined_dist.values, names=combined_dist.index,
        title=tr("distribution_chart"),
        hole=0.42,
        color_discrete_sequence=BRAND_COLORS + ["#7e7c76", "#C0BDB7", "#8B7B7B",
                                                  "#D4B8B8", "#E8D5D5", "#B85C3C"],
    )
    htmpl = ("<b>%{label}</b><br>Consommation: %{value:.0f} L<br>%{percent}"
             if lang == 'fr' else
             "<b>%{label}</b><br>Consumption: %{value:.0f} L<br>%{percent}")
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        hovertemplate=htmpl,
        marker=dict(line=dict(color='white', width=1.5))
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5,
                    xanchor="left", x=1.02, font=dict(size=10))
    )
    return style_chart(fig, height=420)


# ============================================
# YEARLY BREAKDOWN HELPER
# ============================================
def get_yearly_breakdown(df, co2_factors, current_lang):
    if 'Date' not in df.columns or df.empty:
        return pd.DataFrame()

    df_y = df.copy()
    df_y['Year'] = df_y['Date'].dt.year

    yearly = df_y.groupby('Year').agg(
        {'Kilométrage parcouru': 'sum', 'Quantité': 'sum', 'Montant': 'sum'}
    ).rename(columns={'Kilométrage parcouru': 'km', 'Quantité': 'cons', 'Montant': 'cost'})

    if 'Produit' in df.columns:
        py = df_y.groupby(['Year', 'Produit'])['Quantité'].sum().reset_index()
        py['co2_factor'] = py['Produit'].apply(
            lambda p: co2_factors.get(p.upper(), 0) if pd.notna(p) else 0
        )
        py['co2'] = py['Quantité'] * py['co2_factor']
        yearly['co2'] = py.groupby('Year')['co2'].sum()
    else:
        yearly['co2'] = 0

    yearly = yearly.round(0).astype(int).reset_index()
    if current_lang == 'fr':
        yearly.columns = ['Année', 'km', 'cons (L)', 'coût (DT)', 'CO2 (kg)']
    else:
        yearly.columns = ['Year', 'km', 'cons (L)', 'cost (DT)', 'CO2 (kg)']
    return yearly


# ============================================
# HELPERS
# ============================================
def safe_scalar(value, default=0.0):
    """Always return a plain Python float, even for Arrow-backed Series/arrays."""
    try:
        if hasattr(value, 'item'):      # numpy scalar
            return float(value.item())
        if hasattr(value, 'iloc'):      # Series / DataFrame
            value = value.iloc[0]
        return float(value)
    except Exception:
        return float(default)

def _valid_price(v):
    """Return True if v is a plain numeric scalar usable in number_input."""
    try:
        f = float(v)
        return not (f != f)  # reject NaN
    except Exception:
        return False

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    logo_b64 = img_to_b64("logo_Clarke-removebg-preview.png")
    if logo_b64:
        st.markdown(
            f'<a href="/" target="_self" title="Retour à l\'accueil">'
            f'<img src="data:image/png;base64,{logo_b64}" width="220" '
            f'style="cursor:pointer; transition: opacity 0.2s; display:block;" '
            f'onmouseover="this.style.opacity=\'0.75\'" '
            f'onmouseout="this.style.opacity=\'1\'">'
            f'</a>',
            unsafe_allow_html=True
        )
    else:
        st.markdown("## Clarke Energy")

    st.markdown("---")

    if 'language' not in st.session_state:
        st.session_state.language = 'fr'

    language = st.selectbox(
        "🌐 Language / Langue",
        ["Français (fr)", "English (en)"],
        index=0 if st.session_state.language == 'fr' else 1,
        key='language_selector'
    )
    st.session_state.language = 'fr' if "Français" in language else 'en'
    current_lang = st.session_state.language

    st.markdown("---")

    uploaded_file = st.file_uploader(
        tr("upload_file"),
        type=['csv', 'xlsx', 'xls'],
        help=tr("upload_help")
    )

    st.markdown("---")

    # ── Validate & sanitise any fuel prices previously stored in session state ──
    for _key, _default in [('cached_prix_ssp', 2.500),
                            ('cached_prix_go',  1.800),
                            ('cached_prix_goss', 1.900)]:
        if _key in st.session_state and not _valid_price(st.session_state[_key]):
            st.session_state[_key] = _default

    # Always-safe fallback defaults (overridden from file data if available)
    default_prix_ssp = 2.500
    default_prix_go  = 1.800
    default_prix_goss = 1.900
    anomaly_lower_limit = 2.0
    anomaly_upper_limit = 30.0

    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                try:
                    df_raw = pd.read_csv(uploaded_file, delimiter=';', encoding='utf-8')
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    df_raw = pd.read_csv(uploaded_file, delimiter=';', encoding='latin-1')
            else:
                df_raw = pd.read_excel(uploaded_file)

            df_raw = rename_columns_by_position(df_raw)
            df_original_raw = df_raw.copy()
            df = preprocess_data(df_raw)

            if 'P.U' in df.columns and 'Produit' in df.columns:
                for produit_type, attr in [('SSP', 'ssp'), ('GO', 'go'), ('GOSS', 'goss')]:
                    mask = df['Produit'].astype(str).str.upper().str.contains(produit_type, na=False)
                    pu = pd.to_numeric(df.loc[mask, 'P.U'].squeeze(), errors='coerce')
                    if pu.notna().any():
                        mean_val = float(pu.mean())
                        if attr == 'ssp': default_prix_ssp = mean_val
                        elif attr == 'go': default_prix_go = mean_val
                        elif attr == 'goss': default_prix_goss = mean_val

            # ── Filters ──
            st.subheader(tr("analysis_filters"))

            if 'Chauffeur' in df.columns:
                all_opt = 'Tous' if current_lang == 'fr' else 'All'
                drivers = [all_opt] + sorted(df['Chauffeur'].dropna().unique().tolist())
                selected_driver = st.selectbox(tr("select_driver"), drivers, help=tr("driver_help"))

            if 'Véhicule' in df.columns:
                vehicles = df['Véhicule'].dropna().unique().tolist()
                if vehicles:
                    selected_vehicles = st.multiselect(tr("filter_vehicles"), vehicles, default=[])
                else:
                    st.info("Aucun véhicule disponible" if current_lang == 'fr' else "No vehicle data")
                    selected_vehicles = []

            if 'Produit' in df.columns:
                products = [p for p in df['Produit'].dropna().unique().tolist()
                            if 'wash' not in str(p).lower()]
                if products:
                    selected_products = st.multiselect(
                        "Type de Produit" if current_lang == 'fr' else "Product Type",
                        products, default=[])
                else:
                    selected_products = []

            if 'Date' in df.columns:
                min_date = df['Date'].min().date()
                max_date = df['Date'].max().date()
                date_range = st.date_input(
                    tr("select_period"), [min_date, max_date],
                    min_value=min_date, max_value=max_date
                )

            # ── Alert threshold ──
            st.subheader(tr("alert_thresholds"))
            consumption_threshold = st.slider(
                tr("consumption_threshold"),
                min_value=5.0, max_value=20.0, value=10.0, step=0.5,
                help=tr("threshold_help")
            )

            # ── Anomaly detection ──
            st.subheader(tr("anomaly_settings"))
            col_an1, col_an2 = st.columns(2)
            with col_an1:
                anomaly_lower_limit = st.number_input(
                    tr("lower_limit"), value=2.0, min_value=0.0, max_value=10.0, step=0.1)
            with col_an2:
                anomaly_upper_limit = st.number_input(
                    tr("upper_limit"), value=30.0, min_value=10.0, max_value=100.0, step=1.0)

        except Exception as e:
            st.error(f"{'Erreur' if current_lang == 'fr' else 'Error'}: {str(e)}")
            df = None
            df_original_raw = None

    else:
        df = None
        df_original_raw = None

    st.markdown("---")

    # ── Settings ──
    st.subheader(tr("settings"))
    st.markdown(f"**{'Prix carburants' if current_lang=='fr' else 'Fuel prices'}**")
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        try:
            prix_ssp = st.number_input(tr("fuel_price_ssp"), value=safe_scalar(default_prix_ssp, 2.500),
                                       min_value=0.01, max_value=10.0, step=0.001, format="%.3f")
        except Exception:
            prix_ssp = 2.500
    with col_p2:
        try:
            prix_go = st.number_input(tr("fuel_price_go"), value=safe_scalar(default_prix_go, 1.800),
                                      min_value=0.01, max_value=10.0, step=0.001, format="%.3f")
        except Exception:
            prix_go = 1.800
    with col_p3:
        try:
            prix_goss = st.number_input(tr("fuel_price_goss"), value=safe_scalar(default_prix_goss, 1.900),
                                        min_value=0.01, max_value=10.0, step=0.001, format="%.3f")
        except Exception:
            prix_goss = 1.900

    st.markdown(f"**{tr('co2_factors')}**")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        co2_factor_ssp = st.number_input(tr("co2_ssp"), value=2.31, min_value=0.01, step=0.01)
    with col_c2:
        co2_factor_go = st.number_input(tr("co2_go"), value=2.68, min_value=0.01, step=0.01)
    with col_c3:
        co2_factor_goss = st.number_input(tr("co2_goss"), value=2.68, min_value=0.01, step=0.01)

# ============================================
# MAIN — HEADER
# ============================================
st.markdown(f'<h1 class="main-header">{tr("title")}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="page-subtitle">{tr("subtitle")}</p>', unsafe_allow_html=True)

# ============================================
# MAIN APP LOGIC
# ============================================
if uploaded_file and df is not None and df_original_raw is not None:
    df_original_for_missing_check = preprocess_data(df_original_raw.copy())

    # ── Date filter ──
    if 'date_range' in locals() and len(date_range) == 2:
        df_filtered = df[
            (df['Date'].dt.date >= date_range[0]) & (df['Date'].dt.date <= date_range[1])
        ].copy()
    else:
        df_filtered = df.copy()

    # ── Vehicle filter ──
    if 'selected_vehicles' in locals() and selected_vehicles:
        df_filtered = df_filtered[df_filtered['Véhicule'].isin(selected_vehicles)]

    # ── Product filter ──
    if 'selected_products' in locals() and selected_products:
        df_filtered = df_filtered[df_filtered['Produit'].isin(selected_products)]

    # ── Driver filter ──
    if 'selected_driver' in locals() and selected_driver != ('Tous' if current_lang == 'fr' else 'All'):
        df_filtered = df_filtered[df_filtered['Chauffeur'] == selected_driver]

    # ── Missing data table (on raw data) ──
    missing_data_table = create_missing_data_table(df_original_for_missing_check)
    df_filtered_original = df_filtered.copy()

    # ── Remove rows with missing data ──
    df_after_missing_removal, removed_rows = remove_rows_with_missing_data(df_filtered_original)

    # ── Exclude wash ──
    if 'Produit' in df_after_missing_removal.columns:
        mask_wash = df_after_missing_removal['Produit'].astype(str).str.lower().str.contains('wash', na=False)
        df_after_missing_removal = df_after_missing_removal[~mask_wash]

    # ── Anomaly detection ──
    if 'Consommation/100km' in df_after_missing_removal.columns:
        anomaly_mask = (
            (df_after_missing_removal['Consommation/100km'] < anomaly_lower_limit) |
            (df_after_missing_removal['Consommation/100km'] > anomaly_upper_limit)
        )
        df_anomalies = df_after_missing_removal[anomaly_mask].copy()
        df_clean = df_after_missing_removal[~anomaly_mask].copy()
        num_missing_rows = len(removed_rows)
        num_cons_anomalies = len(df_anomalies)
        num_clean = len(df_clean)

        if num_missing_rows > 0 or num_cons_anomalies > 0:
            if current_lang == 'fr':
                msg = (f"⚠️  {num_missing_rows} lignes avec données manquantes et "
                       f"{num_cons_anomalies} anomalies de consommation exclues. "
                       f"**{num_clean} {tr('valid_transactions')}.**")
            else:
                msg = (f"⚠️  {num_missing_rows} rows with missing data and "
                       f"{num_cons_anomalies} consumption anomalies excluded. "
                       f"**{num_clean} {tr('valid_transactions')}.**")
            st.markdown(f'<div class="warning-card">{msg}</div>', unsafe_allow_html=True)
        else:
            tx = len(df_filtered)
            if current_lang == 'fr':
                msg = f"✅  {tr('data_loaded')} : {tx} transactions (wash exclus). {tr('no_anomalies')}."
            else:
                msg = f"✅  {tr('data_loaded')}: {tx} transactions (wash excluded). {tr('no_anomalies')}."
            st.markdown(f'<div class="success-card">{msg}</div>', unsafe_allow_html=True)
    else:
        df_clean = df_after_missing_removal.copy()
        num_missing_rows = len(removed_rows)
        num_cons_anomalies = 0
        tx = len(df_filtered)
        if current_lang == 'fr':
            st.markdown(f'<div class="success-card">✅  {tr("data_loaded")} : {tx} transactions (wash exclus)</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-card">✅  {tr("data_loaded")}: {tx} transactions (wash excluded)</div>', unsafe_allow_html=True)

    df_for_analysis = df_clean.copy()

    # ── All-fuel totals (for estimation) ──
    all_fuel_df = df_filtered_original.copy()
    if 'Produit' in all_fuel_df.columns:
        all_fuel_df = all_fuel_df[
            ~all_fuel_df['Produit'].astype(str).str.lower().str.contains('wash', na=False)
        ]
    estimate_total_cost = all_fuel_df['Montant'].sum() if 'Montant' in all_fuel_df.columns else 0
    total_drivers_est = all_fuel_df['Chauffeur'].nunique() if 'Chauffeur' in all_fuel_df.columns else 0

    # ── Raw data preview ──
    preview_label = "📋 Aperçu des Données Brutes" if current_lang == 'fr' else "📋 Raw Data Preview"
    with st.expander(preview_label, expanded=False):
        st.dataframe(df_filtered_original.head(50), use_container_width=True)
        cap = (f"Total : {len(df_filtered_original)} lignes · {len(df_filtered_original.columns)} colonnes"
               if current_lang == 'fr'
               else f"Total: {len(df_filtered_original)} rows · {len(df_filtered_original.columns)} columns")
        st.caption(cap)

    # ── Product consumption ──
    if 'Produit' in df_for_analysis.columns:
        ssp_mask = df_for_analysis['Produit'].astype(str).str.upper().str.contains('SSP|ESSENCE', na=False)
        go_mask = (df_for_analysis['Produit'].astype(str).str.upper().str.contains('GO|GAZOLE', na=False) &
                   ~df_for_analysis['Produit'].astype(str).str.upper().str.contains('GOSS', na=False))
        goss_mask = df_for_analysis['Produit'].astype(str).str.upper().str.contains('GOSS|GAZOLE SANS SOUFRE', na=False)
        ssp_consumption = df_for_analysis.loc[ssp_mask, 'Quantité'].sum() if ssp_mask.any() else 0
        go_consumption  = df_for_analysis.loc[go_mask,  'Quantité'].sum() if go_mask.any() else 0
        goss_consumption= df_for_analysis.loc[goss_mask,'Quantité'].sum() if goss_mask.any() else 0
        total_co2 = (ssp_consumption * co2_factor_ssp +
                     go_consumption  * co2_factor_go +
                     goss_consumption* co2_factor_goss)
    else:
        ssp_consumption = go_consumption = goss_consumption = total_co2 = 0

    # ============================================================
    # KPI METRICS
    # ============================================================
    st.markdown(f'<h2 class="section-header">📊 {tr("dashboard_header")}</h2>', unsafe_allow_html=True)

    total_km          = df_for_analysis['Kilométrage parcouru'].sum() if 'Kilométrage parcouru' in df_for_analysis.columns else 0
    total_consumption = df_for_analysis['Quantité'].sum() if 'Quantité' in df_for_analysis.columns else 0
    total_cost        = df_for_analysis['Montant'].sum() if 'Montant' in df_for_analysis.columns else 0
    avg_consumption_100km = (total_consumption / total_km * 100) if total_km > 0 else 0
    current_drivers_count = df_for_analysis['Chauffeur'].nunique() if 'Chauffeur' in df_for_analysis.columns else 0
    current_transactions_count = len(df_for_analysis)
    cost_difference   = estimate_total_cost - total_cost
    cost_diff_percent = (cost_difference / total_cost * 100) if total_cost > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        delta_km = (f"{total_km/len(df_for_analysis):.0f} km/" + ("moy" if current_lang=='fr' else "avg")
                    if len(df_for_analysis) > 0 else "")
        st.metric(tr("total_km"), f"{total_km:,.0f} km", delta=delta_km)
        if 'Date' in df_for_analysis.columns:
            yearly = get_yearly_breakdown(df_for_analysis,
                                          {'SSP': co2_factor_ssp, 'GO': co2_factor_go, 'GOSS': co2_factor_goss},
                                          current_lang)
            if not yearly.empty:
                yr_col = 'Année' if current_lang == 'fr' else 'Year'
                with st.expander("Par année" if current_lang == 'fr' else "By year"):
                    st.dataframe(yearly[[yr_col, 'km']].rename(columns={'km': tr("total_km")}),
                                 hide_index=True, use_container_width=True)

    with col2:
        st.metric(tr("total_consumption"), f"{total_consumption:,.0f} L",
                  delta=f"{avg_consumption_100km:.1f} L/100km")
        if 'Date' in df_for_analysis.columns:
            yearly = get_yearly_breakdown(df_for_analysis,
                                          {'SSP': co2_factor_ssp, 'GO': co2_factor_go, 'GOSS': co2_factor_goss},
                                          current_lang)
            if not yearly.empty:
                yr_col = 'Année' if current_lang == 'fr' else 'Year'
                with st.expander("Par année" if current_lang == 'fr' else "By year"):
                    st.dataframe(yearly[[yr_col, 'cons (L)']].rename(columns={'cons (L)': tr("total_consumption")}),
                                 hide_index=True, use_container_width=True)

    with col3:
        delta_cost = f"{total_cost/total_km:.3f} DT/km" if total_km > 0 else ""
        st.metric(tr("total_cost"), f"{total_cost:,.0f} DT", delta=delta_cost)

        if current_lang == 'fr':
            st.markdown(f"""
            <div class="estimation-box">
                <p>Basé sur <span class="estimation-highlight">{current_drivers_count} conducteurs</span>
                   &nbsp;·&nbsp; <span class="estimation-highlight">{current_transactions_count} transactions</span></p>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="estimation-box">
                <p>Based on <span class="estimation-highlight">{current_drivers_count} drivers</span>
                   &nbsp;·&nbsp; <span class="estimation-highlight">{current_transactions_count} transactions</span></p>
            </div>""", unsafe_allow_html=True)

        if total_drivers_est > 0:
            c1, c2 = st.columns([1, 2])
            with c1:
                est_key = 'est_drivers_input' if current_lang == 'fr' else 'est_drivers_input_en'
                if est_key not in st.session_state:
                    st.session_state[est_key] = total_drivers_est
                est_drivers = st.number_input(
                    "Conducteurs" if current_lang == 'fr' else "Drivers",
                    min_value=1, step=1, key=est_key)
            with c2:
                if est_drivers == total_drivers_est:
                    est_cost = estimate_total_cost
                else:
                    avg_cpd = total_cost / current_drivers_count if current_drivers_count > 0 else 0
                    est_cost = avg_cpd * est_drivers
                diff = est_cost - total_cost
                diff_pct = (diff / total_cost * 100) if total_cost != 0 else 0
                st.markdown(f"**{est_cost:,.0f} DT** ({diff:+,.0f}, {diff_pct:+.1f}%)")

        if 'Date' in df_for_analysis.columns:
            yearly = get_yearly_breakdown(df_for_analysis,
                                          {'SSP': co2_factor_ssp, 'GO': co2_factor_go, 'GOSS': co2_factor_goss},
                                          current_lang)
            if not yearly.empty:
                yr_col = 'Année' if current_lang == 'fr' else 'Year'
                cost_col = 'coût (DT)' if current_lang == 'fr' else 'cost (DT)'
                with st.expander("Par année" if current_lang == 'fr' else "By year"):
                    st.dataframe(yearly[[yr_col, cost_col]].rename(columns={cost_col: tr("total_cost")}),
                                 hide_index=True, use_container_width=True)

    with col4:
        co2_delta = f"SSP:{co2_factor_ssp} · GO:{co2_factor_go} · GOSS:{co2_factor_goss} kg/L"
        st.metric(tr("total_co2"), f"{total_co2:,.0f} kg", delta=co2_delta)
        if 'Date' in df_for_analysis.columns:
            yearly = get_yearly_breakdown(df_for_analysis,
                                          {'SSP': co2_factor_ssp, 'GO': co2_factor_go, 'GOSS': co2_factor_goss},
                                          current_lang)
            if not yearly.empty:
                yr_col = 'Année' if current_lang == 'fr' else 'Year'
                with st.expander("Par année" if current_lang == 'fr' else "By year"):
                    st.dataframe(yearly[[yr_col, 'CO2 (kg)']].rename(columns={'CO2 (kg)': tr("total_co2")}),
                                 hide_index=True, use_container_width=True)

    # ============================================================
    # DRIVER DETAILS (if one driver selected)
    # ============================================================
    if 'selected_driver' in locals() and selected_driver != ('Tous' if current_lang == 'fr' else 'All'):
        st.markdown(f'<h2 class="section-header">👤 {tr("driver_analysis")}</h2>', unsafe_allow_html=True)
        driver_data = df_for_analysis[df_for_analysis['Chauffeur'] == selected_driver]

        if not driver_data.empty:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                driver_km = driver_data['Kilométrage parcouru'].sum()
                st.metric(tr("km_driver"), f"{driver_km:,.0f} km",
                          delta=f"{driver_km/total_km*100:.1f}%" if total_km > 0 else "")
            with c2:
                driver_cons = driver_data['Quantité'].sum()
                st.metric(tr("cons_driver"), f"{driver_cons:,.0f} L",
                          delta=f"{driver_cons/total_consumption*100:.1f}%" if total_consumption > 0 else "")
            with c3:
                driver_cost = driver_data['Montant'].sum()
                st.metric(tr("cost_driver"), f"{driver_cost:,.0f} DT",
                          delta=f"{driver_cost/total_cost*100:.1f}%" if total_cost > 0 else "")
            with c4:
                driver_avg = (driver_cons / driver_km * 100) if driver_km > 0 else 0
                deviation = ((driver_avg - avg_consumption_100km) / avg_consumption_100km * 100) if avg_consumption_100km > 0 else 0
                delta_dev = (f"{deviation:.1f}% vs moyenne" if current_lang == 'fr' else f"{deviation:.1f}% vs average")
                st.metric(tr("avg_driver"), f"{driver_avg:.1f} L", delta=delta_dev)

            st.subheader(tr("transactions"))
            driver_summary = driver_data[[
                'Date', 'Véhicule', 'Nom Station', 'Kilométrage parcouru',
                'Quantité', 'Montant', 'Consommation/100km', 'Produit'
            ]].sort_values('Date', ascending=False)
            st.dataframe(driver_summary, use_container_width=True)

    # ============================================================
    # COMPARISON CHARTS
    # ============================================================
    st.markdown(f'<h2 class="section-header">📈 {tr("comparison_header")}</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_cons = create_driver_comparison_chart(df_for_analysis, 'Consommation totale', 10, current_lang)
        if fig_cons:
            st.plotly_chart(fig_cons, use_container_width=True, config={"displayModeBar": False})

    with col2:
        if 'Date' in df_for_analysis.columns:
            years = sorted(df_for_analysis['Date'].dt.year.unique(), reverse=True)
            if years:
                selected_year = st.selectbox(
                    "Année" if current_lang == 'fr' else "Year", years, index=0)
                fig_monthly = create_monthly_consumption_chart(df_for_analysis, selected_year, current_lang)
            else:
                fig_monthly = None
                st.info("Aucune année disponible" if current_lang == 'fr' else "No years available")
        else:
            fig_monthly = None
        if fig_monthly:
            st.plotly_chart(fig_monthly, use_container_width=True, config={"displayModeBar": False})

    col3, col4 = st.columns(2)
    with col3:
        fig_scatter = create_efficiency_scatter_plot(df_for_analysis, current_lang)
        if fig_scatter:
            st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

    with col4:
        fig_combined = create_combined_distribution_chart(df_for_analysis, current_lang)
        if fig_combined:
            st.plotly_chart(fig_combined, use_container_width=True, config={"displayModeBar": False})

    # ============================================================
    # PERFORMANCE TABLES
    # ============================================================
    st.markdown(f'<h2 class="section-header">📋 {tr("details_header")}</h2>', unsafe_allow_html=True)

    st.subheader(tr("driver_perf"))
    driver_metrics = calculate_driver_metrics(df_for_analysis, df_filtered_original, current_lang)

    if not driver_metrics.empty:
        def highlight_high_consumption(row):
            col = 'Consommation moyenne/100km' if current_lang == 'fr' else 'Average Consumption/100km'
            if row[col] > consumption_threshold:
                return ['background-color: #FFF7ED; font-weight: 600'] * len(row)
            return [''] * len(row)

        styled = driver_metrics.style.apply(highlight_high_consumption, axis=1)
        if current_lang == 'fr':
            styled = styled.format({
                'Kilométrage total': '{:,.0f}', 'Consommation totale': '{:,.1f}',
                'Dépense totale': '{:,.0f} DT', 'Consommation moyenne/100km': '{:.1f}',
                'Écart vs moyenne': '{:.1f}%', 'Nombre de transactions': '{:,.0f}'
            })
        else:
            styled = styled.format({
                'Total Distance': '{:,.0f}', 'Total Consumption': '{:,.1f}',
                'Total Cost': '{:,.0f} DT', 'Average Consumption/100km': '{:.1f}',
                'Deviation vs Average': '{:.1f}%', 'Number of Transactions': '{:,.0f}'
            })
        st.dataframe(styled, use_container_width=True)

        threshold_col = 'Consommation moyenne/100km' if current_lang == 'fr' else 'Average Consumption/100km'
        high_consumers = driver_metrics[driver_metrics[threshold_col] > consumption_threshold]

        if not high_consumers.empty:
            st.markdown('<div class="alert-card">', unsafe_allow_html=True)
            warn = (f"🚨 {len(high_consumers)} {tr('high_consumption_warning')} de {consumption_threshold} L/100km"
                    if current_lang == 'fr'
                    else f"🚨 {len(high_consumers)} {tr('high_consumption_warning')} of {consumption_threshold} L/100km")
            st.warning(warn)
            for driver, row in high_consumers.iterrows():
                if current_lang == 'fr':
                    st.write(f"• **{driver}** : {row['Consommation moyenne/100km']:.1f} L/100km  (+{row['Écart vs moyenne']:.1f}% vs moyenne)")
                else:
                    st.write(f"• **{driver}**: {row['Average Consumption/100km']:.1f} L/100km  (+{row['Deviation vs Average']:.1f}% vs average)")
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        high_consumers = pd.DataFrame()

    if 'Véhicule' in df_for_analysis.columns:
        st.subheader(tr("vehicle_perf"))
        vehicle_metrics = calculate_vehicle_metrics(df_for_analysis, current_lang)
        if not vehicle_metrics.empty:
            if current_lang == 'fr':
                st.dataframe(vehicle_metrics.style.format({
                    'Kilométrage total': '{:,.0f}', 'Consommation totale': '{:,.1f}',
                    'Dépense totale': '{:,.0f} DT', 'Consommation moyenne/100km': '{:.1f}',
                    'Énergie': '{}'
                }), use_container_width=True)
            else:
                st.dataframe(vehicle_metrics.style.format({
                    'Total Distance': '{:,.0f}', 'Total Consumption': '{:,.1f}',
                    'Total Cost': '{:,.0f} DT', 'Average Consumption/100km': '{:.1f}',
                    'Fuel': '{}'
                }), use_container_width=True)

    # ============================================================
    # ENERGY OPTIMIZATION
    # ============================================================
    st.markdown(f'<h2 class="section-header">⚡ {tr("optimization_header")}</h2>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_efficiency = df_for_analysis['Consommation/100km'].mean() if 'Consommation/100km' in df_for_analysis.columns else 0
        target_efficiency = st.number_input(
            tr("efficiency_target"),
            min_value=1.0, max_value=20.0,
            value=max(5.0, avg_efficiency * 0.9) if avg_efficiency > 0 else 7.0,
            step=0.1
        )

    potential_savings = savings_cost = co2_savings = 0

    with col2:
        if avg_efficiency > 0 and total_km > 0:
            current_consumption_calc = (avg_efficiency * total_km) / 100
            target_consumption_calc  = (target_efficiency * total_km) / 100
            potential_savings = current_consumption_calc - target_consumption_calc
            savings_pct = ((avg_efficiency - target_efficiency) / avg_efficiency * 100) if avg_efficiency > 0 else 0
            st.metric(tr("potential_savings"), f"{potential_savings:,.0f} L", delta=f"{savings_pct:.1f}%")
        else:
            st.metric(tr("potential_savings"), "0 L")

    with col3:
        if avg_efficiency > 0 and total_km > 0:
            total_cons_mix = ssp_consumption + go_consumption + goss_consumption
            if total_cons_mix > 0:
                avg_fuel_price = (
                    (ssp_consumption / total_cons_mix * prix_ssp) +
                    (go_consumption  / total_cons_mix * prix_go) +
                    (goss_consumption/ total_cons_mix * prix_goss)
                )
                savings_cost = potential_savings * avg_fuel_price
                monthly_savings = (f"{savings_cost/12:,.0f} DT/mois" if current_lang == 'fr'
                                   else f"{savings_cost/12:,.0f} DT/month")
                st.metric(tr("savings_cost"), f"{savings_cost:,.0f} DT", delta=monthly_savings)
            else:
                st.metric(tr("savings_cost"), "0 DT")
        else:
            st.metric(tr("savings_cost"), "0 DT")

    with col4:
        if avg_efficiency > 0 and total_km > 0 and total_consumption > 0:
            ssp_r  = ssp_consumption  / total_consumption if total_consumption > 0 else 0
            go_r   = go_consumption   / total_consumption if total_consumption > 0 else 0
            goss_r = goss_consumption / total_consumption if total_consumption > 0 else 0
            avg_co2 = ssp_r * co2_factor_ssp + go_r * co2_factor_go + goss_r * co2_factor_goss
            co2_savings = potential_savings * avg_co2
            co2_pct = f"{co2_savings/total_co2*100:.1f}%" if total_co2 > 0 else ""
            st.metric(tr("co2_savings"), f"{co2_savings:,.0f} kg", delta=co2_pct)
        else:
            st.metric(tr("co2_savings"), "0 kg")

    # ============================================================
    # EXPORT
    # ============================================================
    st.markdown(f'<h2 class="section-header">📥 {tr("reporting_header")}</h2>', unsafe_allow_html=True)

    col_e1, col_e2, col_e3, col_e4 = st.columns(4)

    with col_e1:
        csv_data = df_for_analysis.to_csv(index=False, sep=';').encode('utf-8-sig')
        st.download_button(
            label="⬇ " + tr("processed_data"),
            data=csv_data,
            file_name="donnees_traitees.csv" if current_lang == 'fr' else "processed_data.csv",
            mime="text/csv"
        )

    with col_e2:
        if not driver_metrics.empty:
            driver_csv = driver_metrics.to_csv(sep=';').encode('utf-8-sig')
            st.download_button(
                label="⬇ " + tr("driver_perf_csv"),
                data=driver_csv,
                file_name="performance_conducteurs.csv" if current_lang == 'fr' else "driver_performance.csv",
                mime="text/csv"
            )

    with col_e3:
        if 'vehicle_metrics' in locals() and not vehicle_metrics.empty:
            vehicle_csv = vehicle_metrics.to_csv(sep=';').encode('utf-8-sig')
            st.download_button(
                label="⬇ " + tr("vehicle_perf_csv"),
                data=vehicle_csv,
                file_name="performance_vehicules.csv" if current_lang == 'fr' else "vehicle_performance.csv",
                mime="text/csv"
            )

    with col_e4:
        period_start = (df_for_analysis['Date'].min().date()
                        if 'Date' in df_for_analysis.columns and not df_for_analysis.empty else 'N/A')
        period_end = (df_for_analysis['Date'].max().date()
                      if 'Date' in df_for_analysis.columns and not df_for_analysis.empty else 'N/A')
        hc_count = len(high_consumers) if 'high_consumers' in locals() else 0
        dm_count = len(driver_metrics) if not driver_metrics.empty else 0

        if current_lang == 'fr':
            report_text = f"""RAPPORT PERFORMANCE ÉNERGÉTIQUE
================================
Période       : {period_start} au {period_end}
Transactions  : {len(df_filtered_original)} initiales · {num_missing_rows} manquantes exclues · {num_cons_anomalies} anomalies exclues
Analysées     : {len(df_for_analysis)}
Kilométrage   : {total_km:,.0f} km
Consommation  : {total_consumption:,.0f} L  (SSP={ssp_consumption:,.0f}, GO={go_consumption:,.0f}, GOSS={goss_consumption:,.0f})
Coût total    : {total_cost:,.0f} DT  (SSP={prix_ssp:.3f}, GO={prix_go:.3f}, GOSS={prix_goss:.3f} DT/L)
Moy./100km    : {avg_consumption_100km:.1f} L
CO2           : {total_co2:,.0f} kg  (SSP={co2_factor_ssp}, GO={co2_factor_go}, GOSS={co2_factor_goss} kg/L)
Conducteurs   : {dm_count} analysés · {hc_count} au-dessus du seuil ({consumption_threshold} L/100km)
Éco. potent.  : {potential_savings:,.0f} L · {savings_cost:,.0f} DT
Éco. CO2      : {co2_savings:,.0f} kg
"""
        else:
            report_text = f"""ENERGY PERFORMANCE REPORT
=========================
Period        : {period_start} to {period_end}
Transactions  : {len(df_filtered_original)} initial · {num_missing_rows} missing excluded · {num_cons_anomalies} anomalies excluded
Analyzed      : {len(df_for_analysis)}
Distance      : {total_km:,.0f} km
Consumption   : {total_consumption:,.0f} L  (SSP={ssp_consumption:,.0f}, GO={go_consumption:,.0f}, GOSS={goss_consumption:,.0f})
Total cost    : {total_cost:,.0f} DT  (SSP={prix_ssp:.3f}, GO={prix_go:.3f}, GOSS={prix_goss:.3f} DT/L)
Avg/100km     : {avg_consumption_100km:.1f} L
CO2           : {total_co2:,.0f} kg  (SSP={co2_factor_ssp}, GO={co2_factor_go}, GOSS={co2_factor_goss} kg/L)
Drivers       : {dm_count} analyzed · {hc_count} above threshold ({consumption_threshold} L/100km)
Pot. savings  : {potential_savings:,.0f} L · {savings_cost:,.0f} DT
CO2 savings   : {co2_savings:,.0f} kg
"""
        st.download_button(
            label="⬇ " + tr("summary_report"),
            data=report_text.encode('utf-8'),
            file_name="rapport_performance.txt" if current_lang == 'fr' else "performance_report.txt",
            mime="text/plain"
        )

    # ============================================================
    # DATA VALIDATION
    # ============================================================
    st.markdown(f'<h2 class="section-header">🔍 {tr("validation_header")}</h2>', unsafe_allow_html=True)

    anomalies_found = []

    # Missing data table
    if not missing_data_table.empty:
        st.markdown(f'<div class="alert-card">🚨 {tr("missing_data_detected")}</div>', unsafe_allow_html=True)
        st.subheader(tr("missing_data_table"))

        def highlight_missing_rows(row):
            if row[tr('total_missing')] >= 5:
                return ['background-color: #FFF7ED; font-weight: 600'] * len(row)
            return [''] * len(row)

        styled_missing = missing_data_table.style.apply(highlight_missing_rows, axis=1).format({
            tr('missing_vehicle'): '{:,.0f}',
            tr('missing_km_before'): '{:,.0f}',
            tr('missing_km_after'): '{:,.0f}',
            tr('missing_product'): '{:,.0f}',
            tr('total_missing'): '{:,.0f}'
        })
        st.dataframe(styled_missing, use_container_width=True)

        total_me = missing_data_table[tr('total_missing')].sum()
        total_dm = len(missing_data_table)
        if current_lang == 'fr':
            st.caption(f"**Résumé :** {total_dm} conducteur(s) concerné(s) · {total_me} entrées manquantes au total. "
                       f"Les {num_missing_rows} lignes exclues, mais les conducteurs restent dans l'analyse avec leurs données valides.")
        else:
            st.caption(f"**Summary:** {total_dm} driver(s) affected · {total_me} total missing entries. "
                       f"The {num_missing_rows} excluded rows, but drivers remain in analysis with valid data.")

    # Consumption anomalies
    if 'Consommation/100km' in df_filtered_original.columns:
        low_a  = df_filtered_original[df_filtered_original['Consommation/100km'] < anomaly_lower_limit]
        high_a = df_filtered_original[df_filtered_original['Consommation/100km'] > anomaly_upper_limit]
        total_ca = len(low_a) + len(high_a)

        if total_ca > 0:
            anomalies_found.append(
                f"{total_ca} anomalies (<{anomaly_lower_limit}: {len(low_a)}, >{anomaly_upper_limit}: {len(high_a)} L/100km)"
            )
            exp_label = ("📋 Voir les transactions avec anomalies" if current_lang == 'fr'
                         else "📋 View transactions with anomalies")
            with st.expander(exp_label, expanded=False):
                if not low_a.empty:
                    st.subheader(f"Trop faible (<{anomaly_lower_limit} L/100km) — {len(low_a)} transactions" if current_lang == 'fr'
                                 else f"Too low (<{anomaly_lower_limit} L/100km) — {len(low_a)} transactions")
                    cols_show = [c for c in ['Ticket', 'Chauffeur', 'Véhicule', 'Km avant', 'KM après',
                                              'Kilométrage parcouru', 'Quantité', 'Consommation/100km', 'Date']
                                 if c in low_a.columns]
                    st.dataframe(low_a[cols_show].sort_values('Consommation/100km'), use_container_width=True)
                if not high_a.empty:
                    st.subheader(f"Trop élevée (>{anomaly_upper_limit} L/100km) — {len(high_a)} transactions" if current_lang == 'fr'
                                 else f"Too high (>{anomaly_upper_limit} L/100km) — {len(high_a)} transactions")
                    cols_show = [c for c in ['Ticket', 'Chauffeur', 'Véhicule', 'Km avant', 'KM après',
                                              'Kilométrage parcouru', 'Quantité', 'Consommation/100km', 'Date']
                                 if c in high_a.columns]
                    st.dataframe(high_a[cols_show].sort_values('Consommation/100km', ascending=False), use_container_width=True)

                if current_lang == 'fr':
                    st.info(f"Ces {total_ca} transactions ont été exclues des calculs KPIs. "
                            f"Les graphiques et tableaux utilisent uniquement les {len(df_for_analysis)} transactions valides. "
                            f"Le nombre de transactions par conducteur inclut toutes les transactions.")
                else:
                    st.info(f"These {total_ca} transactions were excluded from KPI calculations. "
                            f"Charts and tables use only the {len(df_for_analysis)} valid transactions. "
                            f"Transaction count per driver includes all transactions.")

    if anomalies_found and missing_data_table.empty:
        st.markdown('<div class="alert-card">', unsafe_allow_html=True)
        st.warning(tr("anomalies_detected"))
        for a in anomalies_found:
            st.write(f"• {a}")
        st.markdown('</div>', unsafe_allow_html=True)
    elif not anomalies_found and missing_data_table.empty:
        st.markdown(f'<div class="success-card">✅ {tr("no_major_anomalies")}</div>', unsafe_allow_html=True)

# ============================================================
# WELCOME SCREEN
# ============================================================
else:
    current_lang = st.session_state.get('language', 'fr')

    st.markdown(f"""
    <div style='text-align: center; padding: 4rem; background: linear-gradient(135deg, #EDEBEB 0%, #EDEBEB 100%); border-radius: 15px;'>
        <h2 style='color: #A82C14;'>{tr("welcome")}</h2>
        <p style='font-size: 1.3rem; color: #4B5563;'>{tr("welcome_sub")}</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns(3)

    def info_card(icon, title, body):
        st.markdown(f"""
        <div style="
            background: #fff;
            border: 1px solid #E5E7EB;
            border-top: 3px solid #A82C14;
            border-radius: 12px;
            padding: 1.4rem 1.2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            height: 100%;
        ">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase;
                        letter-spacing: 0.6px; color: #A82C14; margin-bottom: 0.6rem;">{title}</div>
            <div style="font-size: 0.85rem; color: #4B5563; line-height: 1.7; white-space: pre-line;">{body}</div>
        </div>""", unsafe_allow_html=True)

    with col1:
        info_card("🎯", tr("new_features"), tr("features_list"))
    with col2:
        info_card("⛽", tr("metrics_calculated"), tr("metrics_list"))
    with col3:
        info_card("🔧", tr("how_to_use"), tr("usage_list"))

    st.divider()

    with st.expander(tr("data_format")):
        if current_lang == 'fr':
            st.markdown("""
| Colonne | Description | Exemple |
|---------|-------------|---------|
| **Ticket** | Numéro de ticket | 12345 |
| **Chauffeur** | Nom du conducteur | DUPONT Jean |
| **Carte libelle** | Libellé carte (fallback) | DUPONT J |
| **Km avant** | Kilométrage avant plein | 15000 |
| **KM après** | Kilométrage après plein | 15250 |
| **Quantité** | Litres consommés | 45.5 |
| **Montant** | Coût du plein | 113.75 |
| **P.U** | Prix unitaire | 2.500 |
| **Produit** | Type de carburant | SSP / GO / GOSS |
| **Date** | Date de la transaction | 2024-01-15 |
| **Véhicule** | Immatriculation | AB-123-CD |
| **Nom Station** | Station-service | TOTAL Tunis |

> **Notes :** lignes `wash` exclues · prix détectés depuis `P.U` · lignes sans véhicule/km/produit exclues · anomalies de consommation configurables
""")
        else:
            st.markdown("""
| Column | Description | Example |
|--------|-------------|---------|
| **Ticket** | Ticket number | 12345 |
| **Chauffeur** | Driver name | DUPONT Jean |
| **Carte libelle** | Card label (fallback) | DUPONT J |
| **Km avant** | Odometer before | 15000 |
| **KM après** | Odometer after | 15250 |
| **Quantité** | Liters consumed | 45.5 |
| **Montant** | Fill-up cost | 113.75 |
| **P.U** | Unit price | 2.500 |
| **Produit** | Fuel type | SSP / GO / GOSS |
| **Date** | Transaction date | 2024-01-15 |
| **Véhicule** | License plate | AB-123-CD |
| **Nom Station** | Gas station | TOTAL Tunis |

> **Notes:** `wash` rows excluded · prices auto-detected from `P.U` · rows missing vehicle/km/product excluded · anomaly limits configurable
""")

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(
    f'<p class="page-footer"><span>Clarke Energy</span> Dashboard v1.0 · © 2026 · All rights reserved</p>',
    unsafe_allow_html=True
)
