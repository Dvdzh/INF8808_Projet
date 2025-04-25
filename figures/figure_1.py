import math 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from helper import TRANSPARENT, generate_color_dict

class WaffleChart():

    def __init__(self):
        pass

    def _get_z_matrix(self, total, values, n_cols=10):
        n_rows = math.ceil(total / n_cols)
        z = values * [1] + (total - values) * [0.5] + (n_rows * n_cols - total) * [0]
        z = np.array(z).reshape(n_rows, n_cols)
        return z
    
    def _get_z_matrix_lower(self, total, values, n_cols=10):
        n_rows = math.ceil(total / n_cols)
        z = values * [1] + (total - values) * [0.5] + (n_rows * n_cols - total) * [0]
        z = np.array(z).reshape(n_rows, n_cols)
        return z
    
    def plot_scatter_waffle_chart(self, distribution, df, category, font_size=16, font_family='Jost', height=700, is_winner=False):
        """
        Génère un graphique en gaufre avec des points représentant les individus.
        
        Args:
            distribution: Dictionnaire contenant le nombre d'individus par catégorie
            df: DataFrame avec les données complètes
            category: Colonne à utiliser pour le regroupement
            font_size: Taille de police pour les annotations
            font_family: Police à utiliser
            height: Hauteur du graphique en pixels
            
        Returns:
            Figure Plotly
        """

        # Trouver la taille de grille maximale nécessaire
        max_len = max(distribution.values())



        # Créer la figure 
        cols = len(distribution)
        fig = make_subplots(rows=1, cols=cols, subplot_titles=list(distribution.keys()))

        # print(f"is_winner: {is_winner}, category: {category}, x_size: {x_size}, y_size: {y_size}, max_len: {max_len}, cols: {cols}")

        # Hard-code pour garder la même taille indépendamment des années        
        layout_by_winner = {
            True: {
                'Race or Ethnicity': {'x_size': 11, 'y_size': 39, 'max_len': 425, 'cols': 5, 'size': 15},
                'Gender': {'x_size': 13, 'y_size': 22, 'max_len': 284, 'cols': 2, 'size': 15},
                'Religion': {'x_size': 9, 'y_size': 34, 'max_len': 302, 'cols': 5, 'size': 15},
                'Age': {'x_size': 7, 'y_size': 22, 'max_len': 149, 'cols': 5, 'size': 20},
                'Sexual orientation': {'x_size': 11, 'y_size': 38, 'max_len': 417, 'cols': 5, 'size': 15}
            },
            None: {
                'Race or Ethnicity': {'x_size': 22, 'y_size': 98, 'max_len': 2140, 'cols': 5, 'size': 15},
                'Gender': {'x_size': 28, 'y_size': 50, 'max_len': 1395, 'cols': 2, 'size': 9},
                'Religion': {'x_size': 19, 'y_size': 81, 'max_len': 1534, 'cols': 5, 'size': 15},
                'Age': {'x_size': 13, 'y_size': 55, 'max_len': 712, 'cols': 5, 'size': 15},
                'Sexual orientation': {'x_size': 22, 'y_size': 92, 'max_len': 2017, 'cols': 5, 'size': 15}
            }
        }
        x_size = layout_by_winner[is_winner][category]['x_size'] 
        y_size = layout_by_winner[is_winner][category]['y_size']

        # Etablir la grille 
        x_grid = np.tile(np.linspace(0, 1, x_size), y_size)
        y_grid = np.repeat(np.linspace(0, 1, y_size), x_size)

        # max_len = layout_by_winner[is_winner][category]['max_len']

        # # Calculer la taille de la grille - ancienne méthode 
        # n_distribution = len(distribution)
        # x_size = math.ceil(math.sqrt(max_len / n_distribution)) + 1   # Exemple : 400 → 20
        # y_size = math.ceil(max_len / x_size)  # Exemple : 400 → 20
        # x_grid = np.tile(np.linspace(0, 1, grid_size), grid_size)
        # y_grid = np.repeat(np.linspace(0, 1, grid_size), grid_size)

        # Générer les couleurs 
        color_scale_dict = generate_color_dict(distribution.keys(), colorscale_name='Oranges')

        # Hover template 
        hovertemplate = (
            "<b>%{customdata[0]}</b><br><br>"                    # Nom en gras
            "<i>Catégorie:</i> %{customdata[1]}<br>"          # Catégorie
            "<i>Film:</i> <span style='color:#1f77b4'>%{customdata[2]}</span><br>"  # Film avec couleur
            "<i>Année:</i> %{customdata[3]}<br>"              # Année
            "<i>Statut:</i> %{customdata[4]}<br>"            # Gagnant
            "<extra></extra>"
        )

        # Pour chaque figure 
        for i, (key, count) in enumerate(distribution.items()):

            # Sous-dataframe pour chaque catégorie, avec nom acteur, film et année et catégorie
            sub_df = df[df[category] == key]

            # sub_df changer tout les Win_Oscar? true par 'Gagnant' et false par 'Nominée'
            sub_df['Win_Oscar?'] = sub_df['Win_Oscar?'].replace({True: 'WINNER', False: 'NOMINEE'})
            
            # On ne garde que le nombre pour cette période 
            x_vals = x_grid[:count]
            y_vals = y_grid[:count]

            # Scatter plot 
            fig.add_trace(go.Scatter(
                x=x_vals, 
                y=y_vals,
                mode='markers',
                marker=dict(
                    size=min(layout_by_winner[is_winner][category]['size'], height/(y_size + 3)), 
                    color=[color_scale_dict[key]] * len(x_vals),
                    symbol="circle",
                ),
                customdata=sub_df[['Name', 'Category', 'Film', 'Year_Ceremony', 'Win_Oscar?']],
                hovertemplate=hovertemplate,
            ), row=1, col=i+1)

            # Axis limits
            fig.update_xaxes(range=[-0.1, 1.05], row=1, col=i+1)
            fig.update_yaxes(range=[-0.1, 1.05], row=1, col=i+1)

            # Supprimer la grille 
            fig.update_xaxes(showline=False, zeroline=False, visible=False, row=1, col=i+1)
            fig.update_yaxes(showline=False, zeroline=False, visible=False, row=1, col=i+1)

            # Annotation pour le nom de la catégorie
            fig.add_annotation(x=0.5, y=-0.05, xref=f'x{i+1}', yref=f'y{i+1}',
                    text=key, showarrow=False, 
                    font_size=font_size, font_family=font_family)
        
        # Layout de la figure
        fig.update_layout(
            height=height,
            width=len(distribution) * 275,
            autosize=False,
            plot_bgcolor=TRANSPARENT, 
            paper_bgcolor=TRANSPARENT,
            margin=dict(l=0, r=0, t=0, b=10),
            showlegend=False,
            hoverlabel=dict(
                bgcolor="white",
                font_size=font_size,
                font_family=font_family
            )
        )

        return fig
