import math
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from helper import TRANSPARENT, generate_color_dict

# Sankey Chart pour comparer les profils démographiques des nominés vs gagnants,
# avec l'affichage des pourcentages des gagnants pour chaque catégorie.
class SankeyDemographicChart:
    def __init__(self):
        pass

    def plot_sankey_chart(self, df, demographic_column):
        """
        Sankey Chart montrant la répartition des nominés vers gagnants par profil démographique.
        Les nœuds « Gagnants <catégorie> » affichent le pourcentage de gagnants par rapport aux nominés.
        Les infobulles des nœuds et des liens sont personnalisées pour n'afficher que les informations désirées.
        """
        # Filtrer les données
        nominees_df = df.copy()
        winners_df = df[df["Win_Oscar?"] == True].copy()
        losers_df = df[df["Win_Oscar?"] == False].copy()
        
        # Récupérer les catégories démographiques
        categories = nominees_df[demographic_column].unique()
        
        # Comptages par catégorie
        nominee_counts = nominees_df[demographic_column].value_counts()
        winner_counts = winners_df[demographic_column].value_counts()
        loser_counts = losers_df[demographic_column].value_counts()
        
        # Calculer les pourcentages de gagnants pour chaque catégorie
        winner_percentages = {}
        for cat in categories:
            total = nominee_counts.get(cat, 0)
            if total > 0:
                winner_percentages[cat] = (winner_counts.get(cat, 0) / total) * 100
            else:
                winner_percentages[cat] = 0
        
        labels = (
            [f"{cat}" for cat in categories] +
            [f"Gagnants {cat} ({winner_percentages[cat]:.1f}%)" for cat in categories] +
            ["Perdants"]
        )
        # Mapping label -> index
        label_indices = {label: i for i, label in enumerate(labels)}
        
        winner_source = []
        winner_target = []
        winner_value = []
        winner_link_colors = []
        
        loser_source = []
        loser_target = []
        loser_value = []
        loser_link_colors = []
        
        color_dict = generate_color_dict(categories, colorscale_name='Oranges')
        
        for cat in categories:
            if cat in nominee_counts:
                # Lien pour les gagnants : de la catégorie vers le noeud du gagnant
                if cat in winner_counts and winner_counts[cat] > 0:
                    winner_source.append(label_indices[f"{cat}"])
                    winner_target.append(label_indices[f"Gagnants {cat} ({winner_percentages[cat]:.1f}%)"])
                    winner_value.append(winner_counts[cat])
                    winner_link_colors.append(color_dict[cat])
                
                # Lien pour les perdants : de la catégorie vers le noeud global "Perdants"
                if cat in loser_counts and loser_counts[cat] > 0:
                    loser_source.append(label_indices[f"{cat}"])
                    loser_target.append(label_indices["Perdants"])
                    loser_value.append(loser_counts[cat])
                    loser_link_colors.append("lightgray")
        
        source = loser_source + winner_source
        target = loser_target + winner_target
        value = loser_value + winner_value
        link_colors = loser_link_colors + winner_link_colors
        
        # Couleur par défaut pour les nœuds
        node_colors = ["#d9d9d9"] * len(labels)
        
        # Création du Sankey Chart
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=20,
                thickness=20,
                label=labels,
                color=node_colors,
                # Affiche uniquement le label sans infos complémentaires
                hovertemplate="%{label} : %{value}<extra></extra>"
            ),
            link=dict(
                source=source,
                target=target,
                value=value,
                color=link_colors,
                # Affiche la relation et la valeur sans les infos "incoming/outcoming flow count"
                hovertemplate="%{source.label} → %{target.label}: %{value}<extra></extra>"
            )
        )])
        
        fig.update_layout(
            font=dict(family="Jost", size=14),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=30, r=30, t=30, b=30)
        )
        
        return fig