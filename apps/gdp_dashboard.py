import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

# Configuration de la page avec thème personnalisé
st.set_page_config(
    page_title="Analyse du PIB Mondial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Définition des couleurs personnalisées pour les graphiques
THEME_COLORS = [
    '#d1d5db', '#9ca3af', '#6b7280', '#4b5563',
    '#e5e7eb', '#374151', '#f3f4f6', '#1f2937'
]

BACKGROUND_COLOR = '#0d1117'
PAPER_COLOR = '#161b22'
GRID_COLOR = '#21262d'
TEXT_COLOR = '#f3f4f6'

# Configuration du thème des graphiques
PLOT_TEMPLATE = go.layout.Template()
PLOT_TEMPLATE.layout.plot_bgcolor = BACKGROUND_COLOR
PLOT_TEMPLATE.layout.paper_bgcolor = PAPER_COLOR
PLOT_TEMPLATE.layout.font = dict(color=TEXT_COLOR)
PLOT_TEMPLATE.layout.xaxis = dict(
    gridcolor=GRID_COLOR, 
    zerolinecolor=GRID_COLOR,
    linecolor=GRID_COLOR
)
PLOT_TEMPLATE.layout.yaxis = dict(
    gridcolor=GRID_COLOR, 
    zerolinecolor=GRID_COLOR,
    linecolor=GRID_COLOR
)

# Configuration des légendes des graphiques
LEGEND_STYLE = dict(
    bgcolor='rgba(13, 17, 23, 0.8)',
    bordercolor='rgba(209, 213, 219, 0.3)',
    borderwidth=1,
    font=dict(color=TEXT_COLOR)
)

# Chargement du CSS externe
def load_css(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Charger le fichier CSS
load_css('apps/style/GPDstyle.css')

# En-tête avec style
st.markdown("""🌍<span>Analyse Mondiale des Tendances Économiques</span> </br></br>
            🎯<span>Objectif de l'Analyse</span> </br></br>
            Cette analyse approfondie explore les dynamiques économiques mondiales à travers le temps, 
            mettant en lumière les disparités de développement entre les pays, les impacts des crises majeures, 
            et les tendances de croissance à long terme.
            Notre dashboard interactif vous permet d'explorer les relations complexes entre la taille 
            des économies et leur potentiel de croissance, offrant une perspective unique sur les 
            transformations économiques globales.
""", unsafe_allow_html=True)

# Fonction de chargement des données avec cache
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("./data/gdp_data.csv")
        df['Log PIB'] = np.log10(df['GDP (Current US$)'])
        return df
    except Exception as e:
        print(f"Erreur lors du chargement des données: {str(e)}")
        return None

try:
    df = load_data()
    
    if df is not None:
        # Sidebar stylisée
        with st.sidebar:
            st.markdown("""
                <div class="sidebar-header">
                    <h2>🔍 Paramètres d'Exploration</h2>
                </div>
            """, unsafe_allow_html=True)
            
            # Sélection de l'année avec style
            years = sorted(df['Year'].unique())
            selected_years = st.slider(
                "📅 Horizon Temporel d'Analyse",
                min_value=min(years),
                max_value=max(years),
                value=(min(years), max(years))
            )
            
            # Sélection des pays avec style
            all_countries = sorted(df['Country'].unique())
            default_countries = all_countries[:5] if len(all_countries) >= 5 else all_countries
            selected_countries = st.multiselect(
                "🌐 Économies à Comparer",
                options=all_countries,
                default=default_countries
            )
        
        # Filtrage des données
        filtered_df = df[
            (df['Year'].between(selected_years[0], selected_years[1])) &
            (df['Country'].isin(selected_countries))
        ]
        
        # Layout en colonnes avec nouvelle grille
        st.markdown('<div class="graph-grid">', unsafe_allow_html=True)

        # Première colonne
        st.markdown('<div class="column">', unsafe_allow_html=True)
        st.markdown("""
            <div class="graph-container">
                <h3>📈 Évolution de la Puissance Économique</h3>
                <p class="graph-description">Trajectoire historique du PIB nominal, reflétant l'évolution 
                de la taille des économies et leur positionnement mondial au fil du temps.</p>
            """, unsafe_allow_html=True)

        fig_gdp = px.line(
            filtered_df,
            x='Year',
            y='GDP (Current US$)',
            color='Country',
            title="",
            template=PLOT_TEMPLATE,
            color_discrete_sequence=THEME_COLORS
        )
        fig_gdp.update_layout(
            height=400,
            hovermode='x unified',
            legend=LEGEND_STYLE,
            plot_bgcolor=BACKGROUND_COLOR,
            paper_bgcolor=PAPER_COLOR
        )
        st.plotly_chart(fig_gdp, use_container_width=True)

        st.markdown("""
            <div class="observation-box">
                <h4>Points Clés</h4>
                <ul>
                    <li>Émergence de nouvelles puissances économiques</li>
                    <li>Impact des crises financières sur la trajectoire économique</li>
                    <li>Écarts croissants entre les économies développées et émergentes</li>
                </ul>
            </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Deuxième colonne
        st.markdown('<div class="column">', unsafe_allow_html=True)
        st.markdown("""
            <div class="graph-container">
                <h3>💹 Dynamiques de Croissance</h3>
                <p class="graph-description">Analyse comparative des taux de croissance, mettant en évidence 
                les périodes d'expansion, de récession et les cycles économiques.</p>
            """, unsafe_allow_html=True)

        fig_growth = px.line(
            filtered_df,
            x='Year',
            y='GDP Growth (%)',
            color='Country',
            title="",
            template=PLOT_TEMPLATE,
            color_discrete_sequence=THEME_COLORS
        )
        fig_growth.update_layout(
            height=400,
            hovermode='x unified',
            legend=LEGEND_STYLE,
            plot_bgcolor=BACKGROUND_COLOR,
            paper_bgcolor=PAPER_COLOR
        )
        st.plotly_chart(fig_growth, use_container_width=True)

        st.markdown("""
            <div class="observation-box">
                <h4>🔍 Points Clés:</h4>
                <ul>
                    <li>Cycles de croissance et périodes de volatilité</li>
                    <li>Résilience différenciée face aux chocs économiques</li>
                    <li>Tendances de convergence/divergence entre économies</li>
                </ul>
            </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # Fin de la grille

        # Section Relation PIB vs Croissance
        st.markdown("""
            <div class="graph-container">
                <h3>🔄 Relation Taille-Croissance des Économies</h3>
                <p class="graph-description">Exploration de la corrélation entre la taille d'une économie et 
                son potentiel de croissance, testant l'hypothèse de convergence économique.</p>
            """, unsafe_allow_html=True)
        
        fig_scatter = px.scatter(
            filtered_df,
            x='GDP (Current US$)',
            y='GDP Growth (%)',
            color='Country',
            title="",
            template=PLOT_TEMPLATE,
            color_discrete_sequence=THEME_COLORS,
            hover_data=['Year']
        )
        fig_scatter.update_layout(
            height=500,
            legend=LEGEND_STYLE,
            plot_bgcolor=BACKGROUND_COLOR,
            paper_bgcolor=PAPER_COLOR
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Statistiques descriptives
        st.markdown("""
            <div class="graph-container">
                <h3>📊 Indicateurs de Performance Économique</h3>
                <p class="graph-description">Synthèse comparative des performances économiques moyennes, 
                permettant d'identifier les leaders en termes de taille et de dynamisme.</p>
        """, unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            avg_gdp = filtered_df.groupby('Country')['GDP (Current US$)'].mean().sort_values(ascending=False)
            fig_avg = px.bar(
                avg_gdp,
                title="PIB Moyen par Pays",
                template=PLOT_TEMPLATE,
                color_discrete_sequence=THEME_COLORS
            )
            fig_avg.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor=BACKGROUND_COLOR,
                paper_bgcolor=PAPER_COLOR
            )
            st.plotly_chart(fig_avg, use_container_width=True)
        
        with col4:
            avg_growth = filtered_df.groupby('Country')['GDP Growth (%)'].mean().sort_values(ascending=False)
            fig_avg_growth = px.bar(
                avg_growth,
                title="Croissance Moyenne du PIB",
                template=PLOT_TEMPLATE,
                color_discrete_sequence=THEME_COLORS
            )
            fig_avg_growth.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor=BACKGROUND_COLOR,
                paper_bgcolor=PAPER_COLOR
            )
            st.plotly_chart(fig_avg_growth, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Tableau détaillé
        st.markdown("""
            <div class="data-table">
                <h3>📑 Données Économiques Détaillées</h3>
                <p class="table-description">Ensemble complet des données historiques permettant une analyse 
                approfondie des trajectoires économiques individuelles.</p>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            filtered_df[['Country', 'Year', 'GDP (Current US$)', 'GDP Growth (%)']]
            .sort_values(['Country', 'Year']),
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erreur lors du chargement des données: {str(e)}")
    st.markdown("""
        <div class="error-message">
            <h3>Erreur</h3>
            <p>Veuillez vérifier que:</p>
            <ul>
                <li>Le fichier gdp_data.csv est présent dans le répertoire ./data/</li>
                <li>Le format des données est conforme aux attentes</li>
                <li>Les colonnes nécessaires sont présentes dans le fichier</li>
            </ul>
        </div>
    """, unsafe_allow_html=True) 