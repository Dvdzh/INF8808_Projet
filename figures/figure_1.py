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
    
    def plot_scatter_waffle_chart(self, distribution, df, category, font_size=16, font_family='Jost', height=700):
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
        fig = make_subplots(rows=1, cols=len(distribution),
                            shared_yaxes=True, shared_xaxes=True,
                            horizontal_spacing=0.01, vertical_spacing=0.01)

        color_scale_dict = generate_color_dict(distribution.keys(), colorscale_name='Oranges')

        y_max = math.ceil(max(distribution.values()) // 10) + 1

        for i, (key, _) in enumerate(distribution.items()):
            
            sub_df = (df[df[category] == key]
                .assign(index=lambda x: range(len(x)))
                .assign(x=lambda x: x['index'] % 10)
                .assign(y=lambda x: x['index'] // 10))
        
            fig.add_trace(go.Scatter(
                x=sub_df['x'], y=sub_df['y'],
                mode='markers',
                marker=dict(
                    size=min(400/y_max, 20),
                    color=[color_scale_dict[key]] * len(sub_df),
                    symbol='circle'
                ),
                customdata=sub_df[['Name', 'Category', 'Film', 'Year_Ceremony']],
                hovertemplate='Name: %{customdata[0]}<br>Category: %{customdata[1]}<br>Film: %{customdata[2]}<br>Year: %{customdata[3]} <extra></extra>'
            ), row=1, col=i+1)

            fig.add_annotation(x=4.5, y=-1.5, xref=f'x{i+1}', yref=f'y{i+1}',
                            text=key, showarrow=False, 
                                font_size=font_size, font_family=font_family)

            # Configuration des limites des axes
            fig.update_xaxes(range=[-1, 10], row=1, col=i+1)
            fig.update_yaxes(range=[-3, y_max+0.5], row=1, col=i+1)
            fig.update_xaxes(visible=False, row=1, col=i+1)
            fig.update_yaxes(visible=False, row=1, col=i+1)

            fig.update_layout(showlegend=False)
            fig.update_layout(
                hoverlabel=dict(
                    bgcolor="white",
                    font_size=font_size,
                    font_family=font_family
                )
            )

        fig.update_layout(
            height=height,
            autosize=False,
            plot_bgcolor=TRANSPARENT, 
            paper_bgcolor=TRANSPARENT,
            margin=dict(l=0, r=0, t=0, b=10)
        )

        return fig
    
    def _get_hovertemplate(self, distribution):
        hovertemplate = []
        for id in distribution:
            hovertemplate += ['Name: ' + id]* distribution[id]
        return hovertemplate
