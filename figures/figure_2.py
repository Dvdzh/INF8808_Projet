import math
import pandas as pd
import plotly.colors as pc
import plotly.express as px
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from helper import TRANSPARENT, generate_color_dict

# Sankey Chart pour comparer les profils démographiques des nominés vs gagnants.
# On conserve seulement les 5 premières catégories (par nombre de nominés)
# et on regroupe toutes les autres dans une catégorie "Other".
class SankeyDemographicChart:
    def __init__(self):
        pass

    def plot_sankey_chart(self, df, demographic_column):
        """
        Sankey Chart montrant la répartition des nominés vers gagnants par profil démographique.
        Seules les 5 premières catégories (selon le nombre de nominés) sont affichées individuellement,
        les autres sont regroupées dans la catégorie "Other".
        Les infobulles sont personnalisées pour n'afficher que le label et le montant.
        """
        # Filtrer les données
        nominees_df = df.copy()
        winners_df = df[df["Win_Oscar?"] == True].copy()
        losers_df = df[df["Win_Oscar?"] == False].copy()

        # Calculer les comptes par catégorie sur l'ensemble des nominés
        nominee_counts = nominees_df[demographic_column].value_counts()
        winner_counts = winners_df[demographic_column].value_counts()
        loser_counts = losers_df[demographic_column].value_counts()
        # On ordonne les catégories par nombre de nominés décroissant
        sorted_categories = list(nominee_counts.index)
        # On prend les 5 premières
        top_categories = sorted_categories[:4]
        # Si d'autres catégories existent, on va les regrouper dans "Other"
        if len(sorted_categories) > 5:
            new_categories = top_categories + ["Other"]
        else:
            new_categories = top_categories

        # Constitution des comptes agrégés pour la nouvelle répartition
        new_nominee_counts = {}
        new_winner_counts = {}
        new_loser_counts = {}
        new_winner_percentages = {}

        # Pour les catégories affichées individuellement
        for cat in top_categories:
            new_nominee_counts[cat] = nominee_counts.get(cat, 0)
            new_winner_counts[cat] = winner_counts.get(cat, 0)
            new_loser_counts[cat] = loser_counts.get(cat, 0)
            if new_nominee_counts[cat] > 0:
                new_winner_percentages[cat] = (new_winner_counts[cat] / new_nominee_counts[cat]) * 100
            else:
                new_winner_percentages[cat] = 0

        # Pour la catégorie "Other", on agrège tous les autres
        if "Other" in new_categories:
            other_nominee = sum([nominee_counts.get(cat, 0) for cat in sorted_categories[5:]])
            other_winner = sum([winner_counts.get(cat, 0) for cat in sorted_categories[5:]])
            other_loser = sum([loser_counts.get(cat, 0) for cat in sorted_categories[5:]])
            new_nominee_counts["Other"] = other_nominee
            new_winner_counts["Other"] = other_winner
            new_loser_counts["Other"] = other_loser
            if other_nominee > 0:
                new_winner_percentages["Other"] = (other_winner / other_nominee) * 100
            else:
                new_winner_percentages["Other"] = 0

        # Construction des labels pour les nœuds
        # Nœuds de gauche : les catégories (nominés)
        left_labels = [f"{cat}" for cat in new_categories]
        # Nœuds de droite : "Gagnants <catégorie> (X%)"
        right_labels = [f"Gagnants {cat} ({new_winner_percentages[cat]:.1f}%)" for cat in new_categories]
        # Le nœud global pour les perdants
        loser_label = "Perdants"

        # Les labels finaux (affichés sur le graphique)
        labels = left_labels + right_labels + [loser_label]
        # Création du mapping label -> index
        label_indices = {label: i for i, label in enumerate(labels)}

        # Préparation des customdata pour affichage en hover (label et montant)
        left_customdata = [f"{cat} : {new_nominee_counts.get(cat, 0)}" for cat in new_categories]
        right_customdata = [f"Gagnants {cat} : {new_winner_counts.get(cat, 0)}" for cat in new_categories]
        loser_customdata = [f"Perdants : {sum(new_loser_counts.values())}"]
        node_customdata = left_customdata + right_customdata + loser_customdata

        # Construction des liens
        winner_source = []
        winner_target = []
        winner_value = []
        winner_link_colors = []

        loser_source = []
        loser_target = []
        loser_value = []
        loser_link_colors = []

        # Générer les couleurs pour les nœuds individuels
        # Pour "Other", on peut lui affecter une couleur spécifique (ici "gray")
        color_dict = generate_color_dict(top_categories, colorscale_name='Oranges')
        if "Other" in new_categories:
            color_dict["Other"] = "gray"

        # Pour chaque catégorie, créer le lien vers le nœud des gagnants et vers le nœud "Perdants"
        for cat in new_categories:
            # Lien pour les gagnants (de la catégorie nominés vers le nœud des gagnants)
            if new_winner_counts.get(cat, 0) > 0:
                winner_source.append(label_indices[f"{cat}"])
                winner_target.append(label_indices[f"Gagnants {cat} ({new_winner_percentages[cat]:.1f}%)"])
                winner_value.append(new_winner_counts.get(cat, 0))
                winner_link_colors.append(color_dict.get(cat, "gray"))
            # Lien pour les perdants (nominés - gagnants)
            losers_for_cat = new_nominee_counts.get(cat, 0) - new_winner_counts.get(cat, 0)
            if losers_for_cat > 0:
                loser_source.append(label_indices[f"{cat}"])
                loser_target.append(label_indices[loser_label])
                loser_value.append(losers_for_cat)
                loser_link_colors.append("lightgray")

        # Combinaison des liens (les perdants d'abord, puis les gagnants)
        source = loser_source + winner_source
        target = loser_target + winner_target
        value = loser_value + winner_value
        link_colors = loser_link_colors + winner_link_colors

        # Couleur par défaut pour les nœuds
        node_colors = ["#d9d9d9"] * len(labels)

        # Création du Sankey Chart avec les hovertemplates personnalisés
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=20,
                thickness=20,
                label=labels,
                customdata=node_customdata,
                hovertemplate="%{customdata}<extra></extra>",
                color=node_colors
            ),
            link=dict(
                source=source,
                target=target,
                value=value,
                color=link_colors,
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
