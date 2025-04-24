import pandas as pd
import plotly.graph_objects as go
from helper import TRANSPARENT, generate_color_dict

class LineChart():
    def __init__(self):
        pass

    def plot_line_chart(self, distribution_dict, category, selected_categories, df, cumulative=True, scale_type='linear', height=700):
        """
        Génère un graphique en lignes montrant l'évolution d'une catégorie au fil du temps.
        
        Args:
            distribution_dict: Dictionnaire des distributions par année
            category: Colonne de regroupement (ex. 'Ethnicity', 'Gender', etc.)
            selected_categories: Liste des catégories à afficher
            df: DataFrame contenant les données complètes
            cumulative: Si True, affiche les données de manière cumulative
            scale_type: Type d'échelle pour l'axe Y ('linear' ou 'log')
            height: Hauteur du graphique en pixels
            
        Returns:
            Figure Plotly
        """
        fig = go.Figure()
        
        # Couleurs pour les catégories
        color_dict = generate_color_dict(selected_categories, colorscale_name='Oranges')
        
        # Tracer les courbes pour chaque catégorie
        for i, category_name in enumerate(selected_categories):
            x_years = sorted(distribution_dict.keys())
            y_values = [distribution_dict[year].get(category_name, 0) for year in x_years]
            
            # Données pour les infobulles
            filtered_df = df[df[category] == category_name]
            hover_texts = []
            
            for year in x_years:
                # Comptage annuel vs cumulatif
                year_count = distribution_dict[year].get(category_name, 0)
                annual_count = year_count
                
                if cumulative and year > min(x_years):
                    previous_year_index = x_years.index(year) - 1
                    previous_year = x_years[previous_year_index]
                    annual_count = year_count - distribution_dict[previous_year].get(category_name, 0)
                
                year_data = filtered_df[filtered_df['Year_Ceremony'] == year]
                
                # Texte pour l'infobulle
                text = f"<b>{category_name}</b><br>"
                text += f"Année: {year}<br>"
                
                if cumulative:
                    text += f"Total cumulé: {year_count}<br>"
                    text += f"Nouveaux cette année: {annual_count}<br>"
                else:
                    text += f"Nombre cette année: {annual_count}<br>"
                
                # Exemples de gagnants/nominés
                if not year_data.empty and annual_count > 0:
                    text += "<br>Exemples:<br>"
                    for _, entry in year_data.head(3).iterrows():
                        text += f"• {entry['Name']} ({entry['Film']})<br>"
                    
                    if len(year_data) > 3:
                        text += f"...et {len(year_data) - 3} autres"
                
                hover_texts.append(text)

            # Ajouter la trace au graphique
            fig.add_trace(go.Scatter(
                x=x_years,
                y=y_values,
                mode='lines+markers',
                name=category_name,
                line=dict(color=color_dict[category_name], width=3),
                marker=dict(size=8, color=color_dict[category_name]),
                hoverinfo='text',
                hovertext=hover_texts
            ))

        # Ligne verticale pour marquer 2015 (si dans l'intervalle)
        shapes = []
        if x_years and min(x_years) <= 2015 <= max(x_years):
            shapes.append(
                dict(
                    type='line',
                    x0=2015,
                    x1=2015,
                    y0=0,
                    y1=1,
                    xref='x',
                    yref='paper',
                    line=dict(
                        color='grey',
                        width=2,
                        dash='dashdot'
                    )
                )
            )

        # Configuration du graphique
        fig.update_layout(
            shapes=shapes,
            autosize=True,
            height=height,
            paper_bgcolor=TRANSPARENT,
            plot_bgcolor=TRANSPARENT,
            xaxis=dict(
                title={'text': 'Année', 'font': {'family': 'Jost', 'size': 16}},
                showgrid=False,
                showspikes=True,
                spikecolor='grey',
                spikethickness=1,
                spikedash='solid',
                spikemode='across',
                tickfont={'family': 'Jost'}
            ),
            yaxis=dict(
                title={'text': 'Nombre cumulé' if cumulative else 'Nombre', 'font': {'family': 'Jost', 'size': 16}},
                showgrid=True,
                gridcolor='rgba(0,0,0,0.1)',
                tickfont={'family': 'Jost'},
                type=scale_type
            ),
            legend_title={
                'text': 'Catégories',
                'font': {'family': 'Jost', 'size': 16}
            },
            legend={'font': {'family': 'Jost', 'size': 14}},
            hovermode='closest',
            hoverdistance=100,
            hoverlabel=dict(
                bgcolor='white', 
                font_size=16,
                font_family='Jost'
            ),
        )
        
        return fig