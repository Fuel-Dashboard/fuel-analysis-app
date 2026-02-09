# ============================================
# ENHANCED ENERGY PERFORMANCE DASHBOARD - UPDATED
# ============================================


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import warnings
import numpy as np
warnings.filterwarnings('ignore')

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
        # Page headers
        "title": "📊 Tableau de Bord Clarke Energy- Gestion de la consommation du carburant ",
        "subtitle": "Analyse détaillée de la consommation du carburant",
        "dashboard_header": " Tableau de Bord",
        "comparison_header": "Comparaisons de Performance",
        "details_header": "📋 Tableaux de Performance",
        "optimization_header": "⚡ Optimisation Énergétique",
        "reporting_header": "📥 Rapports",
        "validation_header": "🚨 Validation des Données",
        
        # Metrics
        "total_km": "Kilométrage Total",
        "total_consumption": "Consommation Totale",
        "total_cost": "Coût Total Carburant",
        "total_co2": "Émissions CO2",
        "km_driver": "Kilométrage Conducteur",
        "cons_driver": "Consommation Conducteur",
        "cost_driver": "Coût Conducteur",
        "avg_driver": "Moyenne/100km",
        "potential_savings": "Économie Potentielle",
        "savings_cost": "Économie en DT",
        "co2_savings": "Économie CO2",
        
        # Table headers
        "driver_perf": "Performance par Conducteur",
        "vehicle_perf": "Performance par Véhicule",
        "transactions": "Détails des Transactions",
        
        # Buttons and filters
        "upload_file": "📤 Upload votre fichier de données",
        "upload_help": "Format attendu: .csv ou .xlsx avec colonnes en français",
        "analysis_filters": "🔍 Filtres d'Analyse",
        "select_driver": "Sélectionner un Conducteur",
        "driver_help": "Choisir un conducteur pour voir ses détails",
        "filter_vehicles": "Filtrer par Véhicule(s)",
        "select_period": "Période d'analyse",
        "alert_thresholds": "⚡ Seuils d'Alerte",
        "consumption_threshold": "Seuil consommation/100km (L)",
        "threshold_help": "Définir le seuil pour mettre en évidence les conducteurs",
        "settings": "⚙️ Paramètres",
        "fuel_price_ssp": "Prix du SSP (DT/L)",
        "fuel_price_go": "Prix du GO (DT/L)",
        "fuel_price_goss": "Prix du GOSS (DT/L)",
        "fuel_price_help": "Prix par litre en Dinars Tunisiens",
        "co2_factors": "🌍 Facteurs d'Émission CO2",
        "co2_ssp": "Facteur CO2 SSP (kg/L)",
        "co2_go": "Facteur CO2 GO (kg/L)",
        "co2_goss": "Facteur CO2 GOSS (kg/L)",
        "co2_help": "Facteur d'émission par type de carburant",
        
        # Anomaly settings
        "anomaly_settings": "🚨 Paramètres Détection Anomalies",
        "lower_limit": "Limite inférieure consommation (L/100km)",
        "upper_limit": "Limite supérieure consommation (L/100km)",
        "anomaly_help": "Transactions en dehors de cette plage seront exclues des calculs",
        
        # Driver analysis
        "driver_analysis": "👤 Analyse par Conducteur",
        
        # Charts
        "top_drivers": "Top Conducteurs par Consommation totale",
        "consumption_trend": "Évolution de la Consommation Journalière",
        "efficiency_scatter": "Efficacité Énergétique: Consommation vs Distance",
        "distribution_chart": "Répartition de la Consommation par Conducteur et Véhicule",
        
        # Export
        "processed_data": "📄 Données Traitées (CSV)",
        "driver_perf_csv": "👤 Performance Conducteurs",
        "vehicle_perf_csv": "🚗 Performance Véhicules",
        "summary_report": "📋 Rapport Sommaire",
        
        # Messages
        "welcome":  "Bienvenue sur votre Dashboard",
        "welcome_sub": "Commencez par télécharger votre fichier de données dans la barre latérale",
        "data_loaded": "✅ Données chargées",
        "anomalies_excluded": "anomalies détectées et exclues des calculs KPIs",
        "valid_transactions": "transactions valides analysées",
        "no_anomalies": "Aucune anomalie de consommation détectée",
        "high_consumption_warning": "conducteur(s) dépassent le seuil",
        "anomalies_detected": "Anomalies détectées dans les données:",
        "no_major_anomalies": "✅ Aucune anomalie majeure détectée",
        "missing_data_detected": "🚨 Données manquantes détectées par conducteur",
        "missing_data_table": "Tableau des données manquantes par conducteur",
        "missing_vehicle": "Véhicule manquant",
        "missing_km_before": "Km avant manquant ou 0",
        "missing_km_after": "Km après manquant ou 0",
        "missing_product": "Produit manquant",
        "total_missing": "Total manquantes",
        "driver": "Chauffeur",
        "times": "fois",
        
        # Features
        "new_features": "🎯  Fonctionnalités",
        "features_list": """
        • Analyse par conducteur et véhicule
        • KPIs de performance énergétique
        • Détection d'anomalies automatisée
        • Visualisations interactives
        • Rapports d'optimisation""",
        
        "metrics_calculated": "⛽ KPIs Calculées",
        "metrics_list": """• Kilométrage parcouru
        • Consommation/100km
        • Coût au kilomètre (DT/km)
        • Émissions CO2 (SSP & Diesel)
        • Écart vs moyenne
        • Potentiel d'économie""",
        
        "how_to_use": "🔧 Comment Utiliser",
        "usage_list": """1. Téléchargez vos données
        2. Appliquez les filtres
        3. Analysez les KPIs
        4. Exportez les rapports
        5. Optimisez la performance""",
        
        "data_format": "📋 Format de Données Requis (Cliquez pour développer)",
        "required_columns": "Votre fichier doit contenir ces colonnes (noms en français):",
        "efficiency_target": "Objectif d'efficacité (L/100km)",
        
        # Footer
        "footer": "📊 Dashboard Clarke Energy v1.0 | © 2026 "
    },
    "en": {
        # Page headers
        "title": "📊 Clarke Energy Fuel Consumption Monitoring Dashboard",
        "subtitle": "Detailed fuel consumption analysis",
        "dashboard_header": " Performance Dashboard",
        "comparison_header": "Performance Comparisons",
        "details_header": "📋 Detailed Performance Tables",
        "optimization_header": "⚡ Energy Optimization",
        "reporting_header": "📥 Reports & Export",
        "validation_header": "🚨 Data Validation",
        
        # Metrics
        "total_km": "Total Distance",
        "total_consumption": "Total Consumption",
        "total_cost": "Total Fuel Cost",
        "total_co2": "CO2 Emissions",
        "km_driver": "Driver Distance",
        "cons_driver": "Driver Consumption",
        "cost_driver": "Driver Cost",
        "avg_driver": "Average/100km",
        "potential_savings": "Potential Savings",
        "savings_cost": "Savings in DT",
        "co2_savings": "CO2 Savings",
        
        # Table headers
        "driver_perf": "Performance by Driver",
        "vehicle_perf": "Performance by Vehicle",
        "transactions": "Transaction Details",
        
        # Buttons and filters
        "upload_file": "📤 Upload your data file",
        "upload_help": "Expected format: .csv or .xlsx with French columns",
        "analysis_filters": "🔍 Analysis Filters",
        "select_driver": "Select a Driver",
        "driver_help": "Choose a driver to see details",
        "filter_vehicles": "Filter by Vehicle(s)",
        "select_period": "Analysis Period",
        "alert_thresholds": "⚡ Alert Thresholds",
        "consumption_threshold": "Consumption/100km threshold (L)",
        "threshold_help": "Set threshold to highlight drivers",
        "settings": "⚙️ Settings",
        "fuel_price_ssp": "SSP Price (DT/L)",
        "fuel_price_go": "GO Price (DT/L)",
        "fuel_price_goss": "GOSS Price (DT/L)",
        "fuel_price_help": "Price per liter in Tunisian Dinars",
        "co2_factors": "🌍 CO2 Emission Factors",
        "co2_ssp": "CO2 Factor SSP (kg/L)",
        "co2_go": "CO2 Factor GO (kg/L)",
        "co2_goss": "CO2 Factor GOSS (kg/L)",
        "co2_help": "Emission factor by fuel type",
        
        # Anomaly settings
        "anomaly_settings": "🚨 Anomaly Detection Settings",
        "lower_limit": "Lower consumption limit (L/100km)",
        "upper_limit": "Upper consumption limit (L/100km)",
        "anomaly_help": "Transactions outside this range will be excluded from calculations",
        
        # Driver analysis
        "driver_analysis": "👤 Driver Analysis",
        
        # Charts
        "top_drivers": "Top Drivers by Total Consumption",
        "consumption_trend": "Daily Consumption Evolution",
        "efficiency_scatter": "Energy Efficiency: Consumption vs Distance",
        "distribution_chart": "Consumption Distribution by Driver and Vehicle",
        
        # Export
        "processed_data": "📄 Processed Data (CSV)",
        "driver_perf_csv": "👤 Driver Performance",
        "vehicle_perf_csv": "🚗 Vehicle Performance",
        "summary_report": "📋 Summary Report",
        
        # Messages
        "welcome": "Welcome to your Dashboard",
        "welcome_sub": "Start by uploading your data file in the sidebar",
        "data_loaded": "✅ Data loaded",
        "anomalies_excluded": "anomalies detected and excluded from KPI calculations",
        "valid_transactions": "valid transactions analyzed",
        "no_anomalies": "No consumption anomalies detected",
        "high_consumption_warning": "driver(s) exceed threshold",
        "anomalies_detected": "Anomalies detected in data:",
        "no_major_anomalies": "✅ No major anomalies detected",
        "missing_data_detected": "🚨 Missing data detected by driver",
        "missing_data_table": "Missing data table by driver",
        "missing_vehicle": "Missing vehicle",
        "missing_km_before": "Missing or zero km before",
        "missing_km_after": "Missing or zero km after",
        "missing_product": "Missing product",
        "total_missing": "Total missing",
        "driver": "Driver",
        "times": "times",
        
        # Features
        "new_features": "🎯 Features",
        "features_list": """• Driver and vehicle analysis
        • Energy performance KPIs
        • Automated anomaly detection
        • Interactive visualizations
        • Optimization reports""",
        
        "metrics_calculated": "⛽ Calculated Metrics",
        "metrics_list": """• Distance traveled
        • Consumption/100km
        • Cost per kilometer (DT/km)
        • CO2 emissions (SSP & Diesel)
        • Deviation vs average
        • Savings potential""",
        
        "how_to_use": "🔧 How to Use",
        "usage_list": """1. Upload your data
        2. Apply filters
        3. Analyze KPIs
        4. Export reports
        5. Optimize performance""",
        
        "data_format": "📋 Required Data Format (Click to expand)",
        "required_columns": "Your file must contain these columns (French names):",
        "efficiency_target": "Efficiency target (L/100km)",
        
        # Footer
        "footer": "📊 Clarke Energy Dashboard v1.0 | © 2026"
    }
}

# ============================================
# LANGUAGE HELPER FUNCTION
# ============================================
def tr(key):
    """Translate key based on selected language"""
    lang = st.session_state.get('language', 'fr')
    return TEXTS[lang].get(key, key)

# ============================================
# CUSTOM STYLING
# ============================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(90deg, #4F1111, #A82C14);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .section-header {
        color: #A82C14;
        border-bottom: 3px solid #A82C14;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #A82C14;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #FCD2D2 0%, #FAB4B4 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #A82C14;
    }
    
    .success-card {
        background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #10B981;
    }
    
    .highlight-row {
        background-color: #FCD2D2 !important;
        font-weight: bold !important;
    }
    
    .dataframe tbody tr:hover {
        background-color: #EFF6FF !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATA PROCESSING FUNCTIONS
# ============================================
def preprocess_data(df):
    """
    Clean and preprocess the data
    """
    df_clean = df.copy()
    
    # Clean column names
    df_clean.columns = df_clean.columns.str.strip()
    
    # Fill Chauffeur column with Carte libelle if empty
    if 'Chauffeur' in df_clean.columns and 'Carte libelle' in df_clean.columns:
        mask = (df_clean['Chauffeur'].isna()) | (df_clean['Chauffeur'] == '')
        df_clean.loc[mask, 'Chauffeur'] = df_clean.loc[mask, 'Carte libelle']
    
    # Convert date columns
    if 'Date' in df_clean.columns:
        df_clean['Date'] = pd.to_datetime(df_clean['Date'], dayfirst=True, errors='coerce')
        df_clean['Month'] = df_clean['Date'].dt.strftime('%Y-%m')
        df_clean['Week'] = df_clean['Date'].dt.isocalendar().week
    
    # Calculate distance traveled
    if all(col in df_clean.columns for col in ['Km avant', 'KM après']):
        df_clean['Kilométrage parcouru'] = df_clean['KM après'] - df_clean['Km avant']
    
    # Calculate consumption per 100km
    if all(col in df_clean.columns for col in ['Quantité', 'Kilométrage parcouru']):
        # Avoid division by zero
        mask = df_clean['Kilométrage parcouru'] > 0
        df_clean.loc[mask, 'Consommation/100km'] = (df_clean.loc[mask, 'Quantité'] / df_clean.loc[mask, 'Kilométrage parcouru']) * 100
        df_clean.loc[~mask, 'Consommation/100km'] = np.nan
    
    return df_clean

def create_missing_data_table(df):
    """
    Create a table of missing data by driver
    Returns a DataFrame with columns: Chauffeur, Véhicule manquant, 
    Km avant manquant ou 0, Km après manquant ou 0, Produit manquant, Total manquantes
    """
    if 'Chauffeur' not in df.columns:
        return pd.DataFrame()
    
    # Get unique drivers
    drivers = df['Chauffeur'].unique()
    missing_data = []
    
    for driver in drivers:
        if pd.isna(driver):
            continue
            
        driver_data = df[df['Chauffeur'] == driver]
        
        # Count missing data for each column
        missing_vehicle = 0
        missing_km_before = 0
        missing_km_after = 0
        missing_product = 0
        
        # Check for missing vehicle
        if 'Véhicule' in df.columns:
            # Check for NaN and empty strings (including multiple spaces)
            missing_vehicle = (
                driver_data['Véhicule'].isna().sum() + 
                (driver_data['Véhicule'].astype(str).str.strip() == '').sum()
            )
        
        # Check for missing or zero km avant
        if 'Km avant' in df.columns:
            # First convert to numeric, handling errors
            km_avant_numeric = pd.to_numeric(driver_data['Km avant'], errors='coerce')
            missing_km_before = (
                km_avant_numeric.isna().sum() + 
                (km_avant_numeric == 0).sum()
            )
        
        # Check for missing or zero km après
        if 'KM après' in df.columns:
            # First convert to numeric, handling errors
            km_apres_numeric = pd.to_numeric(driver_data['KM après'], errors='coerce')
            missing_km_after = (
                km_apres_numeric.isna().sum() + 
                (km_apres_numeric == 0).sum()
            )
        
        # Check for missing product
        if 'Produit' in df.columns:
            # Check for NaN and empty strings (including multiple spaces)
            missing_product = (
                driver_data['Produit'].isna().sum() + 
                (driver_data['Produit'].astype(str).str.strip() == '').sum()
            )
        
        # Calculate total missing for this driver
        total_missing = missing_vehicle + missing_km_before + missing_km_after + missing_product
        
        # Only add to table if there's at least one missing value
        if total_missing > 0:
            missing_data.append({
                tr('driver'): driver,
                tr('missing_vehicle'): int(missing_vehicle),
                tr('missing_km_before'): int(missing_km_before),
                tr('missing_km_after'): int(missing_km_after),
                tr('missing_product'): int(missing_product),
                tr('total_missing'): int(total_missing)
            })
    
    if missing_data:
        missing_df = pd.DataFrame(missing_data)
        # Sort by total missing descending
        missing_df = missing_df.sort_values(tr('total_missing'), ascending=False)
        return missing_df
    else:
        return pd.DataFrame()

def check_missing_data(df):
    """
    Check for missing data in key columns and return a summary by driver
    """
    missing_summary = {}
    
    if 'Chauffeur' not in df.columns:
        return missing_summary
    
    # Group by driver
    for driver in df['Chauffeur'].unique():
        if pd.isna(driver):
            continue
            
        driver_data = df[df['Chauffeur'] == driver]
        
        # Check each condition
        missing_counts = {}
        
        # Check for missing vehicle
        if 'Véhicule' in df.columns:
            missing_vehicle = driver_data['Véhicule'].isna().sum() + (driver_data['Véhicule'].astype(str).str.strip() == '').sum()
            if missing_vehicle > 0:
                missing_counts['vehicle'] = missing_vehicle
        
        # Check for missing or zero km avant
        if 'Km avant' in df.columns:
            km_avant_numeric = pd.to_numeric(driver_data['Km avant'], errors='coerce')
            missing_km_before = (
                km_avant_numeric.isna().sum() + 
                (km_avant_numeric == 0).sum()
            )
            if missing_km_before > 0:
                missing_counts['km_before'] = missing_km_before
        
        # Check for missing or zero km après
        if 'KM après' in df.columns:
            km_apres_numeric = pd.to_numeric(driver_data['KM après'], errors='coerce')
            missing_km_after = (
                km_apres_numeric.isna().sum() + 
                (km_apres_numeric == 0).sum()
            )
            if missing_km_after > 0:
                missing_counts['km_after'] = missing_km_after
        
        # Check for missing product
        if 'Produit' in df.columns:
            missing_product = driver_data['Produit'].isna().sum() + (driver_data['Produit'].astype(str).str.strip() == '').sum()
            if missing_product > 0:
                missing_counts['product'] = missing_product
        
        if missing_counts:
            missing_summary[driver] = missing_counts
    
    return missing_summary

def remove_rows_with_missing_data(df):
    """
    Remove rows with missing data in key columns but keep the driver in analysis
    Returns cleaned dataframe and summary of removed rows
    """
    df_clean = df.copy()
    
    # Create masks for missing data
    masks_to_remove = []
    
    if 'Véhicule' in df_clean.columns:
        mask_vehicle = df_clean['Véhicule'].isna() | (df_clean['Véhicule'].astype(str).str.strip() == '')
        masks_to_remove.append(mask_vehicle)
    
    if 'Km avant' in df_clean.columns:
        km_avant_numeric = pd.to_numeric(df_clean['Km avant'], errors='coerce')
        mask_km_before = km_avant_numeric.isna() | (km_avant_numeric == 0)
        masks_to_remove.append(mask_km_before)
    
    if 'KM après' in df_clean.columns:
        km_apres_numeric = pd.to_numeric(df_clean['KM après'], errors='coerce')
        mask_km_after = km_apres_numeric.isna() | (km_apres_numeric == 0)
        masks_to_remove.append(mask_km_after)
    
    if 'Produit' in df_clean.columns:
        mask_product = df_clean['Produit'].isna() | (df_clean['Produit'].astype(str).str.strip() == '')
        masks_to_remove.append(mask_product)
    
    # Combine all masks
    if masks_to_remove:
        combined_mask = masks_to_remove[0]
        for mask in masks_to_remove[1:]:
            combined_mask = combined_mask | mask
        
        # Store removed rows for reporting
        removed_rows = df_clean[combined_mask].copy()
        
        # Remove rows with missing data
        df_clean = df_clean[~combined_mask]
    else:
        removed_rows = pd.DataFrame()
    
    return df_clean, removed_rows

def calculate_driver_metrics(df_clean, df_original, lang='fr'):
    """
    Calculate metrics per driver
    """
    if 'Chauffeur' not in df_clean.columns:
        return pd.DataFrame()
    
    # Calculate metrics from CLEANED data (without anomalies and missing data)
    metrics_clean = df_clean.groupby('Chauffeur').agg({
        'Kilométrage parcouru': 'sum',
        'Quantité': 'sum',
        'Montant': 'sum',
        'Consommation/100km': 'mean'
    }).round(2)
    
    metrics_clean.columns = ['Kilométrage total', 'Consommation totale', 'Dépense totale',
                          'Consommation moyenne/100km']
    
    # Calculate percentage from overall average
    if 'Consommation/100km' in df_clean.columns:
        overall_avg = df_clean['Consommation/100km'].mean()
        metrics_clean['Écart vs moyenne'] = ((metrics_clean['Consommation moyenne/100km'] - overall_avg) / overall_avg * 100).round(1)
    
    # Calculate number of transactions from ORIGINAL data (including anomalies and removed rows)
    if 'Chauffeur' in df_original.columns:
        transaction_counts = df_original.groupby('Chauffeur')['Ticket'].count()
        transaction_counts.name = 'Nombre de transactions'
        
        # Merge transaction counts with metrics
        metrics = pd.concat([metrics_clean, transaction_counts], axis=1)
        
        # Fill NaN values for drivers who only have anomalies (no valid transactions)
        metrics['Nombre de transactions'] = metrics['Nombre de transactions'].fillna(0).astype(int)
        metrics['Kilométrage total'] = metrics['Kilométrage total'].fillna(0)
        metrics['Consommation totale'] = metrics['Consommation totale'].fillna(0)
        metrics['Dépense totale'] = metrics['Dépense totale'].fillna(0)
        metrics['Consommation moyenne/100km'] = metrics['Consommation moyenne/100km'].fillna(0)
        metrics['Écart vs moyenne'] = metrics['Écart vs moyenne'].fillna(0)
    else:
        metrics = metrics_clean
        metrics['Nombre de transactions'] = df_clean.groupby('Chauffeur')['Ticket'].count()
    
    # Sort by total consumption
    metrics = metrics.sort_values('Consommation totale', ascending=False)
    
    # Translate column names if language is English
    if lang == 'en':
        metrics.columns = ['Total Distance', 'Total Consumption', 'Total Cost',
                          'Average Consumption/100km', 'Deviation vs Average',
                          'Number of Transactions']
    
    return metrics

def calculate_vehicle_metrics(df, lang='fr'):
    """
    Calculate metrics per vehicle
    """
    if 'Véhicule' not in df.columns:
        return pd.DataFrame()
    
    metrics = df.groupby('Véhicule').agg({
        'Kilométrage parcouru': 'sum',
        'Quantité': 'sum',
        'Montant': 'sum',
        'Consommation/100km': 'mean'
    }).round(2)
    
    if lang == 'fr':
        metrics.columns = ['Kilométrage total', 'Consommation totale', 'Dépense totale',
                          'Consommation moyenne/100km']
    else:
        metrics.columns = ['Total Distance', 'Total Consumption', 'Total Cost',
                          'Average Consumption/100km']
    
    return metrics.sort_values('Consommation totale' if lang == 'fr' else 'Total Consumption', ascending=False)

# ============================================
# VISUALIZATION FUNCTIONS
# ============================================
def create_driver_comparison_chart(df, metric='Consommation totale', top_n=15, lang='fr'):
    """
    Create bar chart comparing drivers by selected metric
    """
    if 'Chauffeur' not in df.columns:
        return None
    
    if lang == 'fr':
        driver_metrics = calculate_driver_metrics(df, df, lang='fr')
        title = f"Top {top_n} Conducteurs par {metric}"
        x_label = 'Conducteur'
    else:
        driver_metrics = calculate_driver_metrics(df, df, lang='en')
        metric_map = {
            'Consommation totale': 'Total Consumption',
            'Dépense totale': 'Total Cost',
            'Kilométrage total': 'Total Distance'
        }
        metric = metric_map.get(metric, metric)
        title = f"Top {top_n} Drivers by {metric}"
        x_label = 'Driver'
    
    if driver_metrics.empty:
        return None
    
    # Get top N drivers
    top_drivers = driver_metrics.nlargest(top_n, metric)
    
    fig = px.bar(
        top_drivers,
        x=top_drivers.index,
        y=metric,
        title=title,
        labels={'x': x_label, metric: metric},
        color=metric,
        color_continuous_scale=[
        "#792e26",
        "#7e7c76",
        "#000703",  
        
    ]
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=400
    )
    
    return fig

def create_consumption_trend_chart(df, lang='fr'):
    """
    Create line chart of consumption over time
    """
    if 'Date' not in df.columns or 'Quantité' not in df.columns:
        return None
    
    daily_consumption = df.groupby(df['Date'].dt.date).agg({
        'Quantité': 'sum',
        'Montant': 'sum',
        'Chauffeur': 'nunique'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_consumption['Date'],
        y=daily_consumption['Quantité'],
        mode='lines+markers',
        name='Consommation (L)' if lang == 'fr' else 'Consumption (L)',
        line=dict(color="#9B2525", width=2),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    ))
    
    title = tr("consumption_trend")
    y_label = 'Consommation (L)' if lang == 'fr' else 'Consumption (L)'
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title=y_label,
        hovermode='x unified',
        height=400
    )
    
    return fig

def create_efficiency_scatter_plot(df, lang='fr'):
    """
    Create scatter plot: Consumption vs Distance
    """
    if not all(col in df.columns for col in ['Kilométrage parcouru', 'Consommation/100km']):
        return None
    
    x_col = 'Kilométrage parcouru'
    y_col = 'Consommation/100km'
    
    if lang == 'fr':
        x_label = 'Distance parcourue (km)'
        y_label = 'Consommation (L/100km)'
        title = "Efficacité Énergétique: Consommation vs Distance"
    else:
        x_label = 'Distance traveled (km)'
        y_label = 'Consumption (L/100km)'
        title = "Energy Efficiency: Consumption vs Distance"
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color='Chauffeur' if 'Chauffeur' in df.columns else None,
        size='Quantité',
        title=title,
        labels={x_col: x_label, y_col: y_label},
        hover_data=['Chauffeur', 'Véhicule'] if all(col in df.columns for col in ['Chauffeur', 'Véhicule']) else None
    )
    
    # Add average lines
    avg_consumption = df['Consommation/100km'].mean()
    avg_distance = df['Kilométrage parcouru'].mean()
    
    if lang == 'fr':
        avg_consumption_text = f"Moyenne: {avg_consumption:.1f} L/100km"
        avg_distance_text = f"Moyenne: {avg_distance:.0f} km"
    else:
        avg_consumption_text = f"Average: {avg_consumption:.1f} L/100km"
        avg_distance_text = f"Average: {avg_distance:.0f} km"
    
    fig.add_hline(y=avg_consumption, line_dash="dash", line_color="red",
                 annotation_text=avg_consumption_text)
    fig.add_vline(x=avg_distance, line_dash="dash", line_color="green",
                 annotation_text=avg_distance_text)
    
    fig.update_layout(height=500)
    
    return fig

def create_combined_distribution_chart(df, lang='fr'):
    """
    Create SINGLE pie chart showing consumption by vehicle AND driver combined
    """
    if 'Véhicule' not in df.columns or 'Chauffeur' not in df.columns:
        return None
    
    # Create a combined column for driver + vehicle
    df_combined = df.copy()
    df_combined['Chauffeur_Véhicule'] = df_combined['Chauffeur'] + ' (' + df_combined['Véhicule'] + ')'
    
    # Get top 15 combinations
    combined_dist = df_combined.groupby('Chauffeur_Véhicule')['Quantité'].sum().nlargest(15)
    
    if combined_dist.empty:
        return None
    
    title = tr("distribution_chart")
    
    fig = px.pie(
        combined_dist,
        values=combined_dist.values,
        names=combined_dist.index,
        title=title,
        hole=0.4
    )
    
    if lang == 'fr':
        hovertemplate = "<b>%{label}</b><br>Consommation: %{value:.1f} L<br>Pourcentage: %{percent}"
    else:
        hovertemplate = "<b>%{label}</b><br>Consumption: %{value:.1f} L<br>Percentage: %{percent}"
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate=hovertemplate
    )
    
    fig.update_layout(
        height=400,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.05
        )
    )
    
    return fig

# ============================================
# SIDEBAR - User Controls
# ============================================
with st.sidebar:
    st.image("logo_Clarke-removebg-preview.png", width=250)
    st.title("Dashboard Controls")
    
    # Language selector
    if 'language' not in st.session_state:
        st.session_state.language = 'fr'
    
    language = st.selectbox(
        "🌐 Language / Langue",
        ["Français (fr)", "English (en)"],
        index=0 if st.session_state.language == 'fr' else 1,
        key='language_selector'
    )
    
    # Update session state with language code
    if "Français" in language:
        st.session_state.language = 'fr'
    else:
        st.session_state.language = 'en'
    
    current_lang = st.session_state.language
    
    # File uploader
    uploaded_file = st.file_uploader(
        tr("upload_file"),
        type=['csv', 'xlsx', 'xls'],
        help=tr("upload_help")
    )
    
    st.divider()
    
    if uploaded_file:
        # Load data
        try:
            if uploaded_file.name.endswith('.csv'):
                df_raw = pd.read_csv(uploaded_file, delimiter=';')
            else:
                df_raw = pd.read_excel(uploaded_file)
            
            # Store the original raw data for missing data checking (BEFORE filtering wash)
            df_original_raw = df_raw.copy()
            
            # Preprocess data
            df = preprocess_data(df_raw)
            
            # Calculate default fuel prices from P.U column for each product type
            default_prix_ssp = 2.500  # Default value
            default_prix_go = 1.800   # Default value for GO
            default_prix_goss = 1.900 # Default value for GOSS
            
            if 'P.U' in df.columns and 'Produit' in df.columns:
                # Calculate average P.U for each product type
                for produit_type, default_value in [('SSP', default_prix_ssp), 
                                                   ('GO', default_prix_go), 
                                                   ('GOSS', default_prix_goss)]:
                    # Filter for product type (case insensitive)
                    mask = df['Produit'].astype(str).str.upper().str.contains(produit_type, na=False)
                    pu_values = pd.to_numeric(df.loc[mask, 'P.U'], errors='coerce')
                    if not pu_values.empty and pu_values.notna().any():
                        if produit_type == 'SSP':
                            default_prix_ssp = pu_values.mean()
                        elif produit_type == 'GO':
                            default_prix_go = pu_values.mean()
                        elif produit_type == 'GOSS':
                            default_prix_goss = pu_values.mean()
            
            # Performance Analysis Filters
            st.subheader(tr("analysis_filters"))
            
            # Driver filter
            if 'Chauffeur' in df.columns:
                drivers = ['Tous' if current_lang == 'fr' else 'All'] + sorted(df['Chauffeur'].dropna().unique().tolist())
                selected_driver = st.selectbox(
                    tr("select_driver"),
                    drivers,
                    help=tr("driver_help")
                )
            
            # Vehicle filter - FIXED: Set default to empty list (all vehicles selected)
            if 'Véhicule' in df.columns:
                vehicles = df['Véhicule'].dropna().unique().tolist()
                if vehicles:
                    # Set default to empty list to select ALL vehicles by default
                    selected_vehicles = st.multiselect(
                        tr("filter_vehicles"),
                        vehicles,
                        default=[]  # Empty list means all vehicles are selected
                    )
                else:
                    st.info("Aucune donnée de véhicule disponible" if current_lang == 'fr' else "No vehicle data available")
                    selected_vehicles = []
            
            # Date range filter
            if 'Date' in df.columns:
                min_date = df['Date'].min().date()
                max_date = df['Date'].max().date()
                
                date_range = st.date_input(
                    tr("select_period"),
                    [min_date, max_date],
                    min_value=min_date,
                    max_value=max_date
                )
            
            # Threshold for highlighting
            st.subheader(tr("alert_thresholds"))
            consumption_threshold = st.slider(
                tr("consumption_threshold"),
                min_value=5.0,
                max_value=20.0,
                value=10.0,
                step=0.5,
                help=tr("threshold_help")
            )
            
            # ANOMALY DETECTION SETTINGS
            st.subheader(tr("anomaly_settings"))
            
            col_an1, col_an2 = st.columns(2)
            
            with col_an1:
                anomaly_lower_limit = st.number_input(
                    tr("lower_limit"),
                    value=2.0,
                    min_value=0.0,
                    max_value=10.0,
                    step=0.1,
                    help=tr("anomaly_help")
                )
            
            with col_an2:
                anomaly_upper_limit = st.number_input(
                    tr("upper_limit"),
                    value=30.0,
                    min_value=10.0,
                    max_value=100.0,
                    step=1.0,
                    help=tr("anomaly_help")
                )
            
        except Exception as e:
            error_msg = f"Erreur lors du chargement: {str(e)}" if current_lang == 'fr' else f"Loading error: {str(e)}"
            st.error(error_msg)
            df = None
            df_original_raw = None
    else:
        df = None
        df_original_raw = None
        default_prix_ssp = 2.500
        default_prix_go = 1.800
        default_prix_goss = 1.900
        # Set default anomaly limits even when no file is uploaded
        anomaly_lower_limit = 2.0
        anomaly_upper_limit = 30.0
    
    st.divider()
    
    # Settings - Fuel Prices
    st.subheader("⚙️ " + tr("settings"))
    
    # Fuel prices in Tunisian Dinars for three products
    col_price1, col_price2, col_price3 = st.columns(3)
    
    with col_price1:
        prix_ssp = st.number_input(
            tr("fuel_price_ssp"),
            value=float(default_prix_ssp),
            min_value=0.01,
            max_value=10.0,
            step=0.001,
            format="%.3f",
            help=f"{tr('fuel_price_help')}. Valeur par défaut: {default_prix_ssp:.3f} DT/L" if current_lang == 'fr' else f"{tr('fuel_price_help')}. Default: {default_prix_ssp:.3f} DT/L"
        )
    
    with col_price2:
        prix_go = st.number_input(
            tr("fuel_price_go"),
            value=float(default_prix_go),
            min_value=0.01,
            max_value=10.0,
            step=0.001,
            format="%.3f",
            help=f"{tr('fuel_price_help')}. Valeur par défaut: {default_prix_go:.3f} DT/L" if current_lang == 'fr' else f"{tr('fuel_price_help')}. Default: {default_prix_go:.3f} DT/L"
        )
    
    with col_price3:
        prix_goss = st.number_input(
            tr("fuel_price_goss"),
            value=float(default_prix_goss),
            min_value=0.01,
            max_value=10.0,
            step=0.001,
            format="%.3f",
            help=f"{tr('fuel_price_help')}. Valeur par défaut: {default_prix_goss:.3f} DT/L" if current_lang == 'fr' else f"{tr('fuel_price_help')}. Default: {default_prix_goss:.3f} DT/L"
        )
    
    # CO2 factors for three products
    st.subheader(tr("co2_factors"))
    
    col_co1, col_co2, col_co3 = st.columns(3)
    
    with col_co1:
        co2_factor_ssp = st.number_input(
            tr("co2_ssp"),
            value=2.31,
            min_value=0.01,
            step=0.01,
            help=tr("co2_help")
        )
    
    with col_co2:
        co2_factor_go = st.number_input(
            tr("co2_go"),
            value=2.68,
            min_value=0.01,
            step=0.01,
            help=tr("co2_help")
        )
    
    with col_co3:
        co2_factor_goss = st.number_input(
            tr("co2_goss"),
            value=2.68,
            min_value=0.01,
            step=0.01,
            help=tr("co2_help")
        )

# ============================================
# MAIN PAGE - Header
# ============================================
st.markdown(f'<h1 class="main-header">{tr("title")}</h1>', unsafe_allow_html=True)
st.markdown(f"### {tr('subtitle')}")

# ============================================
# MAIN APP LOGIC
# ============================================
if uploaded_file and df is not None and df_original_raw is not None:
    # Store the original data BEFORE any filtering (for missing data table)
    df_original_for_missing_check = preprocess_data(df_original_raw.copy())
    
    # Apply date filter if date_range exists
    if 'date_range' in locals() and len(date_range) == 2:
        df_filtered = df[
            (df['Date'].dt.date >= date_range[0]) &
            (df['Date'].dt.date <= date_range[1])
        ].copy()
    else:
        df_filtered = df.copy()
    
    # Apply vehicle filter if selected
    # FIXED: When selected_vehicles is empty (default), it means ALL vehicles are selected
    if 'selected_vehicles' in locals():
        # If vehicles are selected in the multiselect, filter by them
        # If no vehicles are selected (empty list), it means ALL vehicles are selected
        if selected_vehicles:  # Only filter if user has specifically selected vehicles
            df_filtered = df_filtered[df_filtered['Véhicule'].isin(selected_vehicles)]
        # If selected_vehicles is empty, don't filter - include ALL vehicles
    
    # Apply driver filter if selected
    if 'selected_driver' in locals() and selected_driver != ('Tous' if current_lang == 'fr' else 'All'):
        df_filtered = df_filtered[df_filtered['Chauffeur'] == selected_driver]
    
    # ============================================
    # CREATE MISSING DATA TABLE (using ORIGINAL data BEFORE filtering)
    # ============================================
    
    # Create missing data table from ORIGINAL data (before any filtering or wash removal)
    missing_data_table = create_missing_data_table(df_original_for_missing_check)
    
    # Store the original filtered data (for transaction counts)
    df_filtered_original = df_filtered.copy()
    
    # ============================================
    # REMOVE ROWS WITH MISSING DATA
    # ============================================
    
    # Remove rows with missing data in key columns
    df_after_missing_removal, removed_rows = remove_rows_with_missing_data(df_filtered_original)
    
    # ============================================
    # EXCLUDE WASH PRODUCTS (AFTER checking for missing data)
    # ============================================
    
    # Now filter out wash products
    if 'Produit' in df_after_missing_removal.columns:
        df_no_wash = df_after_missing_removal.copy()
        # Convert to lowercase for comparison
        df_no_wash['Produit_lower'] = df_no_wash['Produit'].astype(str).str.lower()
        # Exclude wash products
        df_no_wash = df_no_wash[~df_no_wash['Produit_lower'].str.contains('wash', na=False)]
        # Drop the helper column
        df_no_wash = df_no_wash.drop('Produit_lower', axis=1, errors='ignore')
        df_after_missing_removal = df_no_wash
    
    # ============================================
    # ENHANCED ANOMALY DETECTION AND REMOVAL
    # ============================================
    
    # Detect anomalies in consommation moyenne using CONFIGURABLE limits
    if 'Consommation/100km' in df_after_missing_removal.columns:
        # Identify anomalous rows using configurable limits
        consommation_anomalies_mask = (
            (df_after_missing_removal['Consommation/100km'] < anomaly_lower_limit) | 
            (df_after_missing_removal['Consommation/100km'] > anomaly_upper_limit)
        )
        df_anomalies = df_after_missing_removal[consommation_anomalies_mask].copy()
        df_clean = df_after_missing_removal[~consommation_anomalies_mask].copy()
        
        # Count anomalies
        num_missing_rows = len(removed_rows)
        num_cons_anomalies = len(df_anomalies)
        num_clean = len(df_clean)
        
        # Show success message with anomaly information
        if num_missing_rows > 0 or num_cons_anomalies > 0:
            if current_lang == 'fr':
                st.markdown(f'<div class="warning-card">⚠️ {num_missing_rows} lignes avec données manquantes et {num_cons_anomalies} anomalies de consommation exclues. {num_clean} {tr("valid_transactions")}.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="warning-card">⚠️ {num_missing_rows} rows with missing data and {num_cons_anomalies} consumption anomalies excluded. {num_clean} {tr("valid_transactions")}.</div>', unsafe_allow_html=True)
        else:
            if current_lang == 'fr':
                st.markdown(f'<div class="success-card">✅ {tr("data_loaded")}: {len(df_filtered)} transactions (wash exclus). {tr("no_anomalies")}.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="success-card">✅ {tr("data_loaded")}: {len(df_filtered)} transactions (wash excluded). {tr("no_anomalies")}.</div>', unsafe_allow_html=True)
    else:
        df_clean = df_after_missing_removal.copy()
        num_missing_rows = len(removed_rows)
        num_cons_anomalies = 0
        if current_lang == 'fr':
            st.markdown(f'<div class="success-card">✅ {tr("data_loaded")}: {len(df_filtered)} transactions (wash exclus)</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-card">✅ {tr("data_loaded")}: {len(df_filtered)} transactions (wash excluded)</div>', unsafe_allow_html=True)
    
    # Use df_clean for all KPI calculations and visualizations
    df_for_analysis = df_clean.copy()
    
    # ============================================
    # DATA PREVIEW & VALIDATION
    # ============================================
    preview_label = "📋 Aperçu des Données Brutes" if current_lang == 'fr' else "📋 Raw Data Preview"
    with st.expander(preview_label, expanded=False):
        st.dataframe(df_filtered_original.head(50), use_container_width=True)
        if current_lang == 'fr':
            st.caption(f"Total: {len(df_filtered_original)} lignes | {len(df_filtered_original.columns)} colonnes")
        else:
            st.caption(f"Total: {len(df_filtered_original)} rows | {len(df_filtered_original.columns)} columns")
    
    # ============================================
    # CALCULATE CONSUMPTION FOR SSP, GO, AND GOSS
    # ============================================
    if 'Produit' in df_for_analysis.columns:
        # Calculate consumption by product type
        ssp_mask = df_for_analysis['Produit'].astype(str).str.upper().str.contains('SSP|ESSENCE', na=False)
        go_mask = df_for_analysis['Produit'].astype(str).str.upper().str.contains('GO|GAZOLE', na=False) & ~df_for_analysis['Produit'].astype(str).str.upper().str.contains('GOSS', na=False)
        goss_mask = df_for_analysis['Produit'].astype(str).str.upper().str.contains('GOSS|GAZOLE SANS SOUFRE', na=False)
        
        ssp_consumption = df_for_analysis.loc[ssp_mask, 'Quantité'].sum() if ssp_mask.any() else 0
        go_consumption = df_for_analysis.loc[go_mask, 'Quantité'].sum() if go_mask.any() else 0
        goss_consumption = df_for_analysis.loc[goss_mask, 'Quantité'].sum() if goss_mask.any() else 0
        
        # Calculate total CO2 emissions with three factors
        total_co2 = (
            ssp_consumption * co2_factor_ssp + 
            go_consumption * co2_factor_go + 
            goss_consumption * co2_factor_goss
        )
    else:
        ssp_consumption = 0
        go_consumption = 0
        goss_consumption = 0
        total_co2 = 0
    
    # ============================================
    # PERFORMANCE METRICS DASHBOARD
    # ============================================
    st.markdown(f'<h2 class="section-header">{tr("dashboard_header")}</h2>', unsafe_allow_html=True)
    
    # Calculate overall metrics using CLEANED DATA
    total_km = df_for_analysis['Kilométrage parcouru'].sum() if 'Kilométrage parcouru' in df_for_analysis.columns else 0
    total_consumption = df_for_analysis['Quantité'].sum() if 'Quantité' in df_for_analysis.columns else 0
    total_cost = df_for_analysis['Montant'].sum() if 'Montant' in df_for_analysis.columns else 0
    avg_consumption_100km = (total_consumption / total_km * 100) if total_km > 0 else 0
    
    # Create metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        delta_km = f"{total_km/len(df_for_analysis):.0f} km/moy" if len(df_for_analysis) > 0 else ""
        if current_lang == 'en':
            delta_km = f"{total_km/len(df_for_analysis):.0f} km/avg" if len(df_for_analysis) > 0 else ""
        st.metric(
            tr("total_km"),
            f"{total_km:,.0f} km",
            delta=delta_km
        )
    
    with col2:
        delta_cons = f"{avg_consumption_100km:.1f} L/100km"
        st.metric(
            tr("total_consumption"),
            f"{total_consumption:,.0f} L",
            delta=delta_cons
        )
    
    with col3:
        delta_cost = f"{total_cost/total_km:.3f} DT/km" if total_km > 0 else ""
        if current_lang == 'en':
            delta_cost = f"{total_cost/total_km:.3f} DT/km" if total_km > 0 else ""
        st.metric(
            tr("total_cost"),
            f"{total_cost:,.0f} DT",
            delta=delta_cost
        )
    
    with col4:
        co2_delta = f"SSP:{co2_factor_ssp}, GO:{co2_factor_go}, GOSS:{co2_factor_goss} kg/L"
        st.metric(
            tr("total_co2"),
            f"{total_co2:,.0f} kg",
            delta=co2_delta
        )
    
    # ============================================
    # DRIVER DETAILS SECTION (if driver selected)
    # ============================================
    if 'selected_driver' in locals() and selected_driver != ('Tous' if current_lang == 'fr' else 'All'):
        st.markdown(f'<h2 class="section-header">{tr("driver_analysis")}</h2>', unsafe_allow_html=True)
        
        # Use CLEANED data for driver analysis
        driver_data = df_for_analysis[df_for_analysis['Chauffeur'] == selected_driver]
        
        if not driver_data.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                driver_km = driver_data['Kilométrage parcouru'].sum()
                delta_km_pct = f"{(driver_km/total_km*100):.1f}%" if total_km > 0 else ""
                st.metric(
                    tr("km_driver"),
                    f"{driver_km:,.0f} km",
                    delta=delta_km_pct
                )
            
            with col2:
                driver_cons = driver_data['Quantité'].sum()
                delta_cons_pct = f"{(driver_cons/total_consumption*100):.1f}%" if total_consumption > 0 else ""
                st.metric(
                    tr("cons_driver"),
                    f"{driver_cons:,.0f} L",
                    delta=delta_cons_pct
                )
            
            with col3:
                driver_cost = driver_data['Montant'].sum()
                delta_cost_pct = f"{(driver_cost/total_cost*100):.1f}%" if total_cost > 0 else ""
                st.metric(
                    tr("cost_driver"),
                    f"{driver_cost:,.0f} DT",
                    delta=delta_cost_pct
                )
            
            with col4:
                driver_avg = (driver_cons / driver_km * 100) if driver_km > 0 else 0
                deviation = ((driver_avg - avg_consumption_100km) / avg_consumption_100km * 100) if avg_consumption_100km > 0 else 0
                delta_deviation = f"{deviation:.1f}% vs moyenne" if current_lang == 'fr' else f"{deviation:.1f}% vs average"
                st.metric(
                    tr("avg_driver"),
                    f"{driver_avg:.1f} L",
                    delta=delta_deviation
                )
            
            # Driver details table
            st.subheader(tr("transactions"))
            driver_summary = driver_data[[
                'Date', 'Véhicule', 'Nom Station', 'Kilométrage parcouru',
                'Quantité', 'Montant', 'Consommation/100km', 'Produit'
            ]].sort_values('Date', ascending=False)
            
            st.dataframe(driver_summary, use_container_width=True)
    
    # ============================================
    # PERFORMANCE COMPARISON CHARTS (using CLEANED data)
    # ============================================
    st.markdown(f'<h2 class="section-header">{tr("comparison_header")}</h2>', unsafe_allow_html=True)
    
    # Row 1: Consumption chart and Trend chart
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cons = create_driver_comparison_chart(df_for_analysis, 'Consommation totale', 10, current_lang)
        if fig_cons:
            st.plotly_chart(fig_cons, use_container_width=True)
    
    with col2:
        fig_trend = create_consumption_trend_chart(df_for_analysis, current_lang)
        if fig_trend:
            st.plotly_chart(fig_trend, use_container_width=True)
    
    # Row 2: Efficiency scatter plot and SINGLE combined distribution chart
    col3, col4 = st.columns(2)
    
    with col3:
        fig_scatter = create_efficiency_scatter_plot(df_for_analysis, current_lang)
        if fig_scatter:
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col4:
        fig_combined = create_combined_distribution_chart(df_for_analysis, current_lang)
        if fig_combined:
            st.plotly_chart(fig_combined, use_container_width=True)
    
    # ============================================
    # DETAILED PERFORMANCE TABLES (using CLEANED data)
    # ============================================
    st.markdown(f'<h2 class="section-header">{tr("details_header")}</h2>', unsafe_allow_html=True)
    
    # Driver performance table - USING UPDATED FUNCTION with ORIGINAL data for transaction count
    st.subheader(tr("driver_perf"))
    driver_metrics = calculate_driver_metrics(df_for_analysis, df_filtered_original, current_lang)
    
    if not driver_metrics.empty:
        # Highlight drivers above average consumption
        def highlight_high_consumption(row):
            if current_lang == 'fr':
                threshold_col = 'Consommation moyenne/100km'
            else:
                threshold_col = 'Average Consumption/100km'
            
            if row[threshold_col] > consumption_threshold:
                return ['background-color: #FEF3C7; font-weight: bold'] * len(row)
            return [''] * len(row)
        
        styled_driver_table = driver_metrics.style.apply(
            highlight_high_consumption, axis=1
        )
        
        # Format based on language
        if current_lang == 'fr':
            styled_driver_table = styled_driver_table.format({
                'Kilométrage total': '{:,.0f}',
                'Consommation totale': '{:,.1f}',
                'Dépense totale': '{:,.0f} DT',
                'Consommation moyenne/100km': '{:.1f}',
                'Écart vs moyenne': '{:.1f}%',
                'Nombre de transactions': '{:,.0f}'
            })
        else:
            styled_driver_table = styled_driver_table.format({
                'Total Distance': '{:,.0f}',
                'Total Consumption': '{:,.1f}',
                'Total Cost': '{:,.0f} DT',
                'Average Consumption/100km': '{:.1f}',
                'Deviation vs Average': '{:.1f}%',
                'Number of Transactions': '{:,.0f}'
            })
        
        st.dataframe(styled_driver_table, use_container_width=True)
        
        # Display warnings for high consumers
        if current_lang == 'fr':
            threshold_col = 'Consommation moyenne/100km'
        else:
            threshold_col = 'Average Consumption/100km'
        
        high_consumers = driver_metrics[driver_metrics[threshold_col] > consumption_threshold]
        if not high_consumers.empty:
            st.markdown('<div class="warning-card">', unsafe_allow_html=True)
            warning_msg = f"🚨 {len(high_consumers)} {tr('high_consumption_warning')} de {consumption_threshold} L/100km"
            if current_lang == 'en':
                warning_msg = f"🚨 {len(high_consumers)} {tr('high_consumption_warning')} of {consumption_threshold} L/100km"
            st.warning(warning_msg)
            
            for driver, row in high_consumers.iterrows():
                if current_lang == 'fr':
                    st.write(f"• **{driver}**: {row['Consommation moyenne/100km']:.1f} L/100km (+{row['Écart vs moyenne']:.1f}% vs moyenne)")
                else:
                    st.write(f"• **{driver}**: {row['Average Consumption/100km']:.1f} L/100km (+{row['Deviation vs Average']:.1f}% vs average)")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Vehicle performance table
    if 'Véhicule' in df_for_analysis.columns:
        st.subheader(tr("vehicle_perf"))
        vehicle_metrics = calculate_vehicle_metrics(df_for_analysis, current_lang)
        
        if not vehicle_metrics.empty:
            if current_lang == 'fr':
                st.dataframe(
                    vehicle_metrics.style.format({
                        'Kilométrage total': '{:,.0f}',
                        'Consommation totale': '{:,.1f}',
                        'Dépense totale': '{:,.0f} DT',
                        'Consommation moyenne/100km': '{:.1f}'
                    }),
                    use_container_width=True
                )
            else:
                st.dataframe(
                    vehicle_metrics.style.format({
                        'Total Distance': '{:,.0f}',
                        'Total Consumption': '{:,.1f}',
                        'Total Cost': '{:,.0f} DT',
                        'Average Consumption/100km': '{:.1f}'
                    }),
                    use_container_width=True
                )
    
    # ============================================
    # ADDITIONAL ENERGY PERFORMANCE FEATURES (using CLEANED data)
    # ============================================
    st.markdown(f'<h2 class="section-header">{tr("optimization_header")}</h2>', unsafe_allow_html=True)
    
    # Energy efficiency analysis
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Calculate potential savings
        avg_efficiency = df_for_analysis['Consommation/100km'].mean() if 'Consommation/100km' in df_for_analysis.columns else 0
        target_efficiency = st.number_input(
            tr("efficiency_target"),
            min_value=1.0,
            max_value=20.0,
            value=max(5.0, avg_efficiency * 0.9) if avg_efficiency > 0 else 7.0,
            step=0.1
        )
    
    with col2:
        # Calculate potential fuel savings
        potential_savings = 0
        savings_cost = 0
        if avg_efficiency > 0 and total_km > 0:
            current_consumption = (avg_efficiency * total_km) / 100
            target_consumption = (target_efficiency * total_km) / 100
            potential_savings = current_consumption - target_consumption
            savings_percent = ((avg_efficiency - target_efficiency) / avg_efficiency * 100) if avg_efficiency > 0 else 0
            
            st.metric(
                tr("potential_savings"),
                f"{potential_savings:,.0f} L",
                delta=f"{savings_percent:.1f}%"
            )
        else:
            st.metric(tr("potential_savings"), "0 L")
    
    with col3:
        if avg_efficiency > 0 and total_km > 0:
            # Calculate weighted average fuel price based on consumption mix
            total_cons = ssp_consumption + go_consumption + goss_consumption
            if total_cons > 0:
                avg_fuel_price = (
                    (ssp_consumption/total_cons * prix_ssp) +
                    (go_consumption/total_cons * prix_go) +
                    (goss_consumption/total_cons * prix_goss)
                )
                savings_cost = potential_savings * avg_fuel_price
                monthly_savings = f"{savings_cost/12:,.0f} DT/mois" if current_lang == 'fr' else f"{savings_cost/12:,.0f} DT/month"
                st.metric(
                    tr("savings_cost"),
                    f"{savings_cost:,.0f} DT",
                    delta=monthly_savings
                )
            else:
                st.metric(tr("savings_cost"), "0 DT")
        else:
            st.metric(tr("savings_cost"), "0 DT")
    
    with col4:
        # Calculate CO2 savings
        co2_savings = 0
        if avg_efficiency > 0 and total_km > 0 and total_consumption > 0:
            # Calculate weighted average CO2 factor based on fuel mix
            ssp_ratio = ssp_consumption / total_consumption if total_consumption > 0 else 0
            go_ratio = go_consumption / total_consumption if total_consumption > 0 else 0
            goss_ratio = goss_consumption / total_consumption if total_consumption > 0 else 0
            
            # Calculate average CO2 factor based on fuel mix
            avg_co2_factor = (
                ssp_ratio * co2_factor_ssp + 
                go_ratio * co2_factor_go + 
                goss_ratio * co2_factor_goss
            )
            co2_savings = potential_savings * avg_co2_factor
            
            co2_pct = f"{(co2_savings/total_co2*100):.1f}%" if total_co2 > 0 else ""
            st.metric(
                tr("co2_savings"),
                f"{co2_savings:,.0f} kg",
                delta=co2_pct
            )
        else:
            st.metric(tr("co2_savings"), "0 kg")
    
    # ============================================
    # EXPORT AND REPORTING (using CLEANED data)
    # ============================================
    st.markdown(f'<h2 class="section-header">{tr("reporting_header")}</h2>', unsafe_allow_html=True)
    
    # Create export options
    col_exp1, col_exp2, col_exp3, col_exp4 = st.columns(4)
    
    with col_exp1:
        # Export processed data (CLEANED data without anomalies)
        csv_data = df_for_analysis.to_csv(index=False, sep=';').encode('utf-8-sig')
        st.download_button(
            label=tr("processed_data"),
            data=csv_data,
            file_name="donnees_traitees.csv" if current_lang == 'fr' else "processed_data.csv",
            mime="text/csv"
        )
    
    with col_exp2:
        # Export driver performance
        if not driver_metrics.empty:
            driver_csv = driver_metrics.to_csv(sep=';').encode('utf-8-sig')
            st.download_button(
                label=tr("driver_perf_csv"),
                data=driver_csv,
                file_name="performance_conducteurs.csv" if current_lang == 'fr' else "driver_performance.csv",
                mime="text/csv"
            )
    
    with col_exp3:
        # Export vehicle performance
        if 'vehicle_metrics' in locals() and not vehicle_metrics.empty:
            vehicle_csv = vehicle_metrics.to_csv(sep=';').encode('utf-8-sig')
            st.download_button(
                label=tr("vehicle_perf_csv"),
                data=vehicle_csv,
                file_name="performance_vehicules.csv" if current_lang == 'fr' else "vehicle_performance.csv",
                mime="text/csv"
            )
    
    with col_exp4:
        # Generate summary report
        if current_lang == 'fr':
            report_text = f"""
            RAPPORT PERFORMANCE ÉNERGÉTIQUE
            ================================
            Période: {df_for_analysis['Date'].min().date() if 'Date' in df_for_analysis.columns and not df_for_analysis.empty else 'N/A'} au {df_for_analysis['Date'].max().date() if 'Date' in df_for_analysis.columns and not df_for_analysis.empty else 'N/A'}
            Nombre de transactions initiales: {len(df_filtered_original)}
            Lignes avec données manquantes exclues: {num_missing_rows}
            Anomalies de consommation exclues: {num_cons_anomalies} (limites: {anomaly_lower_limit}-{anomaly_upper_limit} L/100km)
            Transactions analysées: {len(df_for_analysis)}
            Kilométrage total: {total_km:,.0f} km
            Consommation totale: {total_consumption:,.0f} L
            Consommation par produit: SSP={ssp_consumption:,.0f} L, GO={go_consumption:,.0f} L, GOSS={goss_consumption:,.0f} L
            Coût total: {total_cost:,.0f} DT
            Prix des carburants: SSP={prix_ssp:.3f} DT/L, GO={prix_go:.3f} DT/L, GOSS={prix_goss:.3f} DT/L
            Consommation moyenne: {avg_consumption_100km:.1f} L/100km
            Émissions CO2 totales: {total_co2:,.0f} kg
            Facteurs CO2: SSP={co2_factor_ssp} kg/L, GO={co2_factor_go} kg/L, GOSS={co2_factor_goss} kg/L
            Conducteurs analysés: {len(driver_metrics) if not driver_metrics.empty else 0}
            Conducteurs au-dessus du seuil ({consumption_threshold} L/100km): {len(high_consumers) if 'high_consumers' in locals() else 0}
            Économie potentielle: {potential_savings:,.0f} L ({savings_cost:,.0f} DT)
            Économie CO2 potentielle: {co2_savings:,.0f} kg
            """
        else:
            report_text = f"""
            ENERGY PERFORMANCE REPORT
            =========================
            Period: {df_for_analysis['Date'].min().date() if 'Date' in df_for_analysis.columns and not df_for_analysis.empty else 'N/A'} to {df_for_analysis['Date'].max().date() if 'Date' in df_for_analysis.columns and not df_for_analysis.empty else 'N/A'}
            Initial transactions: {len(df_filtered_original)}
            Rows with missing data excluded: {num_missing_rows}
            Consumption anomalies excluded: {num_cons_anomalies} (limits: {anomaly_lower_limit}-{anomaly_upper_limit} L/100km)
            Transactions analyzed: {len(df_for_analysis)}
            Total distance: {total_km:,.0f} km
            Total consumption: {total_consumption:,.0f} L
            Consumption by product: SSP={ssp_consumption:,.0f} L, GO={go_consumption:,.0f} L, GOSS={goss_consumption:,.0f} L
            Total cost: {total_cost:,.0f} DT
            Fuel prices: SSP={prix_ssp:.3f} DT/L, GO={prix_go:.3f} DT/L, GOSS={prix_goss:.3f} DT/L
            Average consumption: {avg_consumption_100km:.1f} L/100km
            Total CO2 emissions: {total_co2:,.0f} kg
            CO2 factors: SSP={co2_factor_ssp} kg/L, GO={co2_factor_go} kg/L, GOSS={co2_factor_goss} kg/L
            Drivers analyzed: {len(driver_metrics) if not driver_metrics.empty else 0}
            Drivers above threshold ({consumption_threshold} L/100km): {len(high_consumers) if 'high_consumers' in locals() else 0}
            Potential savings: {potential_savings:,.0f} L ({savings_cost:,.0f} DT)
            Potential CO2 savings: {co2_savings:,.0f} kg
            """
        
        st.download_button(
            label=tr("summary_report"),
            data=report_text.encode('utf-8'),
            file_name="rapport_performance.txt" if current_lang == 'fr' else "performance_report.txt",
            mime="text/plain"
        )
    
    # ============================================
    # ENHANCED DATA VALIDATION AND ANOMALIES
    # ============================================
    st.markdown(f'<h2 class="section-header">{tr("validation_header")}</h2>', unsafe_allow_html=True)
    
    # Check for anomalies in ORIGINAL data (before cleaning)
    anomalies_found = []
    
    # Show missing data table
    if not missing_data_table.empty:
        st.markdown('<div class="warning-card">', unsafe_allow_html=True)
        st.warning(tr("missing_data_detected"))
        
        # Display the missing data table
        st.subheader(tr("missing_data_table"))
        
        # Format the table for better display
        styled_missing_table = missing_data_table.style.format({
            tr('missing_vehicle'): '{:,.0f}',
            tr('missing_km_before'): '{:,.0f}',
            tr('missing_km_after'): '{:,.0f}',
            tr('missing_product'): '{:,.0f}',
            tr('total_missing'): '{:,.0f}'
        })
        
        # Highlight rows with high missing counts
        def highlight_missing_rows(row):
            if row[tr('total_missing')] >= 5:
                return ['background-color: #FEF3C7; font-weight: bold'] * len(row)
            return [''] * len(row)
        
        styled_missing_table = styled_missing_table.apply(highlight_missing_rows, axis=1)
        
        st.dataframe(styled_missing_table, use_container_width=True)
        
        # Summary statistics
        total_missing_entries = missing_data_table[tr('total_missing')].sum()
        total_drivers_with_missing = len(missing_data_table)
        
        if current_lang == 'fr':
            st.write(f"**Résumé:** {total_drivers_with_missing} conducteur(s) avec données manquantes, totalisant {total_missing_entries} entrées manquantes.")
            st.write(f"**Note:** Ces {num_missing_rows} lignes ont été exclues des analyses mais les conducteurs restent dans les calculs de performance avec leurs données valides.")
        else:
            st.write(f"**Summary:** {total_drivers_with_missing} driver(s) with missing data, totaling {total_missing_entries} missing entries.")
            st.write(f"**Note:** These {num_missing_rows} rows have been excluded from analyses but drivers remain in performance calculations with their valid data.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Check for consommation moyenne anomalies using CONFIGURABLE limits
    if 'Consommation/100km' in df_filtered_original.columns:
        # Calculate anomalies for consommation moyenne using configurable limits
        low_cons_anomalies = df_filtered_original[df_filtered_original['Consommation/100km'] < anomaly_lower_limit]
        high_cons_anomalies = df_filtered_original[df_filtered_original['Consommation/100km'] > anomaly_upper_limit]
        total_cons_anomalies = len(low_cons_anomalies) + len(high_cons_anomalies)
        
        if total_cons_anomalies > 0:
            anomalies_found.append(f"{total_cons_anomalies} anomalies de consommation (<{anomaly_lower_limit} L/100km: {len(low_cons_anomalies)}, >{anomaly_upper_limit} L/100km: {len(high_cons_anomalies)})")
            
            # Create expandable section to show detailed anomaly transactions
            expander_label = "📋 Voir les transactions avec anomalies de consommation" if current_lang == 'fr' else "📋 View transactions with consumption anomalies"
            with st.expander(expander_label, expanded=False):
                if not low_cons_anomalies.empty:
                    low_title = f"Consommation trop faible (<{anomaly_lower_limit} L/100km): {len(low_cons_anomalies)} transactions" if current_lang == 'fr' else f"Too low consumption (<{anomaly_lower_limit} L/100km): {len(low_cons_anomalies)} transactions"
                    st.subheader(low_title)
                    st.dataframe(low_cons_anomalies[['Ticket', 'Chauffeur', 'Véhicule', 'Km avant', 'KM après', 
                                                    'Kilométrage parcouru', 'Quantité', 'Consommation/100km', 'Date']].sort_values('Consommation/100km'), 
                               use_container_width=True)
                
                if not high_cons_anomalies.empty:
                    high_title = f"Consommation trop élevée (>{anomaly_upper_limit} L/100km): {len(high_cons_anomalies)} transactions" if current_lang == 'fr' else f"Too high consumption (>{anomaly_upper_limit} L/100km): {len(high_cons_anomalies)} transactions"
                    st.subheader(high_title)
                    st.dataframe(high_cons_anomalies[['Ticket', 'Chauffeur', 'Véhicule', 'Km avant', 'KM après',
                                                     'Kilométrage parcouru', 'Quantité', 'Consommation/100km', 'Date']].sort_values('Consommation/100km', ascending=False), 
                               use_container_width=True)
                
                # Summary of anomalies removed from KPI calculations
                if current_lang == 'fr':
                    st.info(f"""
                    **Impact sur les analyses:**
                    - Ces {total_cons_anomalies} transactions ont été exclues des calculs KPIs
                    - Tous les indicateurs (consommation totale, coût, émissions CO2) sont calculés sans ces anomalies
                    - Les graphiques et tableaux de performance utilisent uniquement les données valides
                    - Les anomalies sont toujours comptées dans le nombre total de transactions par conducteur
                    """)
                else:
                    st.info(f"""
                    **Impact on analyses:**
                    - These {total_cons_anomalies} transactions have been excluded from KPI calculations
                    - All indicators (total consumption, cost, CO2 emissions) are calculated without these anomalies
                    - Charts and performance tables use only valid data
                    - Anomalies are still counted in the total number of transactions per driver
                    """)
    
    # Display all anomalies found
    if anomalies_found and missing_data_table.empty:
        st.markdown('<div class="warning-card">', unsafe_allow_html=True)
        st.warning(tr("anomalies_detected"))
        for anomaly in anomalies_found:
            st.write(f"• {anomaly}")
        
        # Add information about anomaly removal
        if num_cons_anomalies > 0:
            st.write("")
            if current_lang == 'fr':
                st.write(f"**Note:** Les anomalies de consommation (<{anomaly_lower_limit} ou >{anomaly_upper_limit} L/100km) ont été automatiquement exclues des calculs KPIs.")
                st.write(f"Les analyses ci-dessus sont basées sur {len(df_for_analysis)} transactions valides.")
                st.write(f"Le nombre de transactions par conducteur inclut toutes les transactions (anomalies incluses).")
            else:
                st.write(f"**Note:** Consumption anomalies (<{anomaly_lower_limit} or >{anomaly_upper_limit} L/100km) have been automatically excluded from KPI calculations.")
                st.write(f"The above analyses are based on {len(df_for_analysis)} valid transactions.")
                st.write(f"The number of transactions per driver includes all transactions (including anomalies).")
        
        st.markdown('</div>', unsafe_allow_html=True)
    elif not anomalies_found and missing_data_table.empty:
        st.markdown(f'<div class="success-card">{tr("no_major_anomalies")}</div>', unsafe_allow_html=True)

else:
    # ============================================
    # WELCOME SCREEN (when no file uploaded)
    # ============================================
    current_lang = st.session_state.get('language', 'fr')
    
    if current_lang == 'fr':
        welcome_html = f"""
        <div style='text-align: center; padding: 4rem; background: linear-gradient(135deg, #EDEBEB 0%, #EDEBEB 100%); border-radius: 15px;'>
            <h2 style='color: #A82C14;'>{tr("welcome")}</h2>
            <p style='font-size: 1.3rem; color: #4B5563;'>{tr("welcome_sub")}</p>
        </div>
        """
    else:
        welcome_html = f"""
        <div style='text-align: center; padding: 4rem; background: linear-gradient(135deg, #EDEBEB 0%, #EDEBEB 100%); border-radius: 15px;'>
            <h2 style='color: #A82C14;'>{tr("welcome")}</h2>
            <p style='font-size: 1.3rem; color: #4B5563;'>{tr("welcome_sub")}</p>
        </div>
        """
    
    st.markdown(welcome_html, unsafe_allow_html=True)
    
    st.divider()
    
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        st.markdown(f"### {tr('new_features')}")
        st.markdown(tr("features_list"))
    
    with col_info2:
        st.markdown(f"### {tr('metrics_calculated')}")
        st.markdown(tr("metrics_list"))
    
    with col_info3:
        st.markdown(f"### {tr('how_to_use')}")
        st.markdown(tr("usage_list"))
    
    # Sample data format
    expander_label = tr("data_format")
    with st.expander(expander_label):
        if current_lang == 'fr':
            st.markdown("""
            Votre fichier doit contenir ces colonnes (noms en français):
            
            | Colonne | Description | Exemple |
            |---------|-------------|---------|
            | **Ticket** | Numéro de ticket | 12345 |
            | **Chauffeur** | Nom du conducteur | "DUPONT Jean" |
            | **Carte libelle** | Libellé de la carte | "DUPONT J" |
            | **Km avant** | Kilométrage avant plein | 15000 |
            | **KM après** | Kilométrage après plein | 15250 |
            | **Quantité** | Litres consommés | 45.5 |
            | **Montant** | Coût du plein | 113.75 |
            | **P.U** | Prix unitaire | 2.500 |
            | **Produit** | Type de produit | "SSP", "GO" ou "GOSS" |
            | **Date** | Date de la transaction | 2024-01-15 |
            | **Heure** | Heure de la transaction | 14:30 |
            | **Véhicule** | Immatriculation | "AB-123-CD" |
            | **Nom Station** | Station-service | "TOTAL Tunis" |
            
            **Notes**:
            1. Les lignes avec Produit="wash" sont automatiquement exclues
            2. Les prix par défaut sont calculés à partir de la colonne P.U par type de produit
            3. DT = Dinar Tunisien
            4. Si "Chauffeur" est vide, il est rempli avec "Carte libelle"
            5. Les lignes sans véhicule, sans kilométrage (avant/après = 0), ou sans produit sont exclues des analyses mais les conducteurs restent dans les calculs
            6. Les limites d'anomalies de consommation sont configurables dans la barre latérale
            7. Les anomalies sont exclues des calculs KPIs mais incluses dans le nombre de transactions par conducteur
            """)
        else:
            st.markdown("""
            Your file must contain these columns (French names):
            
            | Column | Description | Example |
            |--------|-------------|---------|
            | **Ticket** | Ticket number | 12345 |
            | **Chauffeur** | Driver name | "DUPONT Jean" |
            | **Carte libelle** | Card label | "DUPONT J" |
            | **Km avant** | Odometer before | 15000 |
            | **KM après** | Odometer after | 15250 |
            | **Quantité** | Liters consumed | 45.5 |
            | **Montant** | Cost of fill-up | 113.75 |
            | **P.U** | Unit price | 2.500 |
            | **Produit** | Product type | "SSP", "GO" or "GOSS" |
            | **Date** | Transaction date | 2024-01-15 |
            | **Heure** | Transaction time | 14:30 |
            | **Véhicule** | License plate | "AB-123-CD" |
            | **Nom Station** | Gas station | "TOTAL Tunis" |
            
            **Notes**:
            1. Rows with Produit="wash" are automatically excluded
            2. Default prices are calculated from P.U column by product type
            3. DT = Tunisian Dinar 
            4. If "Chauffeur" is empty, it's filled with "Carte libelle"
            5. Rows without vehicle, without odometer (before/after = 0), or without product are excluded from analyses but drivers remain in calculations
            6. Consumption anomaly limits are configurable in the sidebar
            7. Anomalies are excluded from KPI calculations but included in transaction count per driver
            """)

# ============================================
# FOOTER
# ============================================
st.divider()
st.caption(tr("footer"))

# ============================================
# END OF UPDATED APP WITH ALL MODIFICATIONS
# ============================================