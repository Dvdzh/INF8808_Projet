import math
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from helper import TRANSPARENT, generate_color_dict

# Stacked Area Chart with Normalized Values

class StackedAreaChart():
    def __init__(self):
        pass

    def plot_stacked_area_chart(self, data, height=700):
        """
        Génère un graphique en aires empilées à partir des données fournies.
        
        Args:
            data: Dictionnaire de données par année et catégorie
            height: Hauteur du graphique en pixels
            
        Returns:
            Figure Plotly
        """
        # Convertir les données en DataFrame
        df = pd.DataFrame(data).T.fillna(0)
        df.index = df.index.astype(str)

        # Normaliser les valeurs
        df_normalized = df.div(df.sum(axis=1), axis=0)
        df_percentage = df_normalized * 100
        
        # Obtenir les couleurs pour chaque catégorie
        color_dict = generate_color_dict(identifiers=df_normalized.columns, colorscale_name='Oranges')
        color_sequence = [color_dict[cat] for cat in df_normalized.columns]

        # Créer une figure
        fig = go.Figure()
        
        # Ajouter chaque catégorie comme aire empilée
        for i, col in enumerate(df_percentage.columns):
            fig.add_trace(go.Scatter(
                x=df_percentage.index,
                y=df_percentage[col],
                mode='lines',
                stackgroup='one',
                name=col,
                line=dict(width=0),
                fillcolor=color_sequence[i],
                hoverinfo='skip'
            ))
        
        # Textes personnalisés pour les infobulles
        hover_texts = []
        for year in df_percentage.index:
            text = f"Année : {year}<br>"
            for col in df_percentage.columns:
                percentage = df_percentage.loc[year, col]
                absolute = df.loc[year, col]
                text += f"{col} : {percentage:.1f}% ({int(absolute)})<br>"
            hover_texts.append(text)
        
        # Trace invisible pour les infobulles personnalisées
        fig.add_trace(go.Scatter(
            x=df_percentage.index,
            y=[50] * len(df_percentage),
            mode='markers',
            marker=dict(opacity=0),
            hoverinfo='text',
            hovertext=hover_texts,
            showlegend=False,
        ))
        
        # Configuration du graphique
        fig.update_layout(
            title=None,
            height=height,
            autosize=False,
            xaxis=dict(
                title=None,
                showgrid=False,
                showspikes=True,
                spikecolor='black',
                spikethickness=1,
                spikedash='solid',
                spikemode='across'
            ),
            yaxis=dict(
                title={'text': 'Proportion (%)', 'font': {'family': 'Jost', 'size': 16}},
                showgrid=False,
                tickformat='.0f',
                ticksuffix='%',
                range=[0, 100],
                tickfont={'family': 'Jost'}
            ),
            legend_title={
                'text': 'Catégories',
                'font': {'family': 'Jost', 'size': 16}
            },
            legend={'font': {'family': 'Jost', 'size': 14}},
            hovermode='x',
            hoverdistance=100,
            hoverlabel=dict(
                bgcolor='white', 
                font_size=16,
                font_family='Jost'
            ),
            plot_bgcolor=TRANSPARENT,
            paper_bgcolor=TRANSPARENT,
            font={'family': 'Jost'},
            margin=dict(l=50, r=50, t=30, b=50)
        )
        
        return fig