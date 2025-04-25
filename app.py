# dash app
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import json

import figures.figure_1 as figure_1
import figures.figure_3 as figure_3
import figures.figure_4 as figure_4
import figures.figure_2 as figure_2

from helper import DataLoader
from layout import create_figure_section

print("\nLancement de l'application Dash...")

FONT = 'Jost'


app = dash.Dash(__name__, 
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                    {"name": "description", "content": "Analyse de la diversité aux Oscars"}
                ],
                update_title=None)

# Modification du titre de l'onglet du navigateur
app.title = "Oscars - Analyse de diversité"

# Configuration du favicon dans le layout
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico">
        <link rel="shortcut icon" type="image/x-icon" href="assets/favicon.ico">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Crédit logo
logo_credit = html.A(
    "Oscar icons created by Freepik - Flaticon",
    href='https://www.flaticon.com/free-icons/oscar',
    title='oscar icons',
    target='_blank',
    style={'color': '#555', 'textDecoration': 'underline'}
)

intervalle_defaut = [1928, 2025]

hauteur_default_figure = 700

espace_entre_figures = 150


# Textes pour les explications (syntaxe Markdown: **texte** pour gras)
txt_fig1 = """Dans ce graphique, **chacun des points représente un gagnant ou un nominé aux Oscars**. En passant en survol sur chacun de ces points, un encadré vous indique à qui est attribué ce point. 

*Avez-vous réussi à trouver la première femme noire à avoir reçu un oscar ?*

Si nous analysons les résultats de l'onglet **Ethnie**, nous voyons la distribution des gagnants selon les groupes ethniques. Sur les 416 gagnants, **seulement 50 font partie de la population non-blanche**. Ce qui équivaut à 12% des gagnants. Étant donné que 40% de la population totale des État-Unis est non-blanche (selon Wikipédia), on peut estimer que les gagnants des Oscars ne représentent pas bien les gens de la diversité culturelle. 

Quand on s'intéresse à l'orientation sexuelle, on constate que 57 gagnants ne sont pas hétérosexuels. Cela donne un pourcentage de 13.7% gagnants. Selon le Williams Institute, 5,5% des adultes vivant aux États-Unis s'identifient comme LGBT. Le pourcentage de 13.7% de nos résultats est surement dû au grand nombre d'orientation sexuelle inconnue qui vient probablement fausser nos données.
"""

txt_fig2 = """Ce graphique s'intéresse à la relation nominée et gagnants. Nous voulions savoir si tous les nominés quelle que soit leur ethnie, leur âge, leur genre, leur religion ou leur orientation sexuelle, ont les mêmes chance de gagner. 

Pour chaque prix, il y a habituellement 5 nominés et un seul gagnant. **Les chances de gagner sont donc de 20%.**

Par l'entremise de ce tableau, nous pouvons constater que **ce pourcentage est respecté à travers la plupart des catégories.** Il ne semble pas y avoir de biais qui pousse à favoriser certains nominés par rapport à d'autres. Par contre, cette figure (et les autres) montrent une réelle disparité dans les nominations, qui se repercute dans les gagnants.
"""

txt_fig3 = """ Ce graphique montre l'évolution de la diversité au fil des ans. Le **nombre cumulé de gagnants (ou de nominés)** depuis la création des Oscars est représenté pour chaque catégorie. Un bouton permet de passer à une échelle logarithmique pour mieux visualiser les différences entre les catégories.

En passant la souris sur les lignes, vous pouvez voir plus de détails pour une certaine cérémonie ainsi que quelques informations supplémentaires sur les gagnants ou les nominés.

Il est intéressant de noter que la diversité a augmenté au fil des ans, mais il reste encore un long chemin à parcourir. En effet, **la majorité des gagnants sont toujours blancs et hétérosexuels**.

On peut aussi voir que les normes d'inclusivité mise en place en 2015 en réaction au mouvement *#OscarSoWhite* ont l'air d'avoir un **léger impact** sur la diversité des gagnants. En effet, la tendance à la hausse de la diversité semble s'accélérer dans les dernières années. *Ces tendeances sont plus facilement visibles dans le graphique suivant.*
"""

txt_fig4 = """Ce graphique est complémentaire au précédent. Il montre les proportions de nominés et de gagnants par catégorie. Il est possible de changer la granularité temporelle pour voir les données par année, par 5 ans ou par décennie.

Il permet de se rendre compte des changements de tendances au fil des ans. Par exemple, on peut voir que la **diversité éthnique a clairement augmenté depuis le début des années 2000.**

Aussi, on peut voir que la **diversité de genre a aussi augmenté, mais pas autant que l'ethnie.** En effet, en utilisant la granularité décennale, on peut voir que le nombre de femmes gagnantes a augmenté pour se rapprocher de 50% des gagnants. Il faut bien noter que la différence de genre ne se fait que dans la catégorie *Meilleur réalisateur/trice* car les autres catégories sont genrées.
"""

# Texte pour la conclusion
txt_conclusion = """À travers de tous ces tableaux, nous avons pu constater que la controverse #OscarSowhite était fondée. Par le passé, les gagnants et nominés des Oscars ont été en prédominance des personnes blanches.

De nos jours, cette tendance semble tranquillement se renverser à cause de la création de normes d'inclusivité et de notre société plus inclusive à la diversité. Il faut également se demander si la discrimination dont a été accusé les Oscars est vraiment un problème des Oscars ou de l'industrie de cinéma en entier. 

Malgré ces progrès, **le chemin vers une représentation équitable reste long**. Notre visualisation souligne l'importance de continuer à promouvoir la diversité et l'inclusion dans l'industrie cinématographique.
"""

app.layout = \
    html.Div([

        html.Header(children=[
            html.Div(children=[
                        html.H2('Les'),
                        html.H1('OSCARS'),
                        html.H2('Font-ils de la discrimination?'),
                        html.Hr(),
                        html.P('Nous avons analysé les gagnants des dernières éditions pour le savoir'), 
                    ],
                    className="texte-entete"
                    ),
        ]),
        
        html.Main(children=[

            # Figure 1
            create_figure_section(
                figure_id=1,
                title='Portrait des gagnants: Qui sont les lauréats des Oscars?',
                graph_id='waffle-chart',
                has_checklist=True,
                intervalle=intervalle_defaut,
                font=FONT,
                explanation_text=txt_fig1,
            ),
            
            # Espace entre les figures
            html.Div(style={'height': f'{espace_entre_figures}px', 'width': '100%', 'clear': 'both'}),
            
            # Figure 2
            create_figure_section(
                figure_id=2,
                title='Des chances égales? Le parcours des nominés vers la victoire',
                graph_id='figure-2-graph',
                has_checklist=True,
                has_control_elements=False,
                intervalle=intervalle_defaut,
                font=FONT,
                explanation_text=txt_fig2
            ),
            
            # Espace entre les figures
            html.Div(style={'height': f'{espace_entre_figures}px', 'width': '100%', 'clear': 'both'}),

            # Figure 3
            create_figure_section(
                figure_id=3,
                title='La progression à travers le temps: L\'évolution de la diversité aux Oscars',
                graph_id='line-chart',
                has_checklist=True,
                intervalle=intervalle_defaut,
                font=FONT,
                explanation_text=txt_fig3
            ),
            
            # Espace entre les figures
            html.Div(style={'height': f'{espace_entre_figures}px', 'width': '100%', 'clear': 'both'}),
            
            # Figure 4
            create_figure_section(
                figure_id=4,
                title='Les proportions changeantes: La transformation des Oscars au fil des décennies',
                graph_id='stacked-area-chart',
                has_checklist=True,
                intervalle=intervalle_defaut,
                font=FONT,
                explanation_text=txt_fig4
            ),
            
            # Espace après la dernière figure
            html.Div(style={'height': f'{espace_entre_figures}px', 'width': '100%', 'clear': 'both'}),

            
            # Section de conclusion
            html.H3("Conclusion", className='figure-title'),
            html.Div([
                dcc.Markdown(txt_conclusion, className='figure-explanation')
            ], style={'width': '100%', 'margin': '0 auto 50px auto'}),
            
            # Espace final
            html.Div(style={'height': f'50px', 'width': '100%', 'clear': 'both'}),

        ],
        style={'width': '90%', 'margin': '0 auto', 'fontFamily': FONT, 'display': 'flex', 'flexDirection': 'column'}
        ),
        
        # Footer avec crédits
        html.Footer([
            html.Div([
                # Crédit du logo
                html.Div([
                    html.P("Crédit logo: ", style={'fontWeight': 'bold', 'display': 'inline'}),
                    logo_credit
                ], style={'marginBottom': '10px'}),
                
                # Crédit des créateurs
                html.Div([
                    html.P("Groupe 10 : ", style={'fontWeight': 'bold', 'display': 'inline'}),
                    html.P("Carolina Espinosa - Léo Valette - Nino Montoya - Jean Vincent - Zhu David - Nkondog Yvan Aristide", style={'display': 'inline'})
                ])
            ], style={'textAlign': 'center', 'padding': '20px', 'borderTop': '1px solid #ccc', 'marginTop': '30px'})
        ])
    
    ],
    style={'width': '80%', 'margin': 'auto', 'fontFamily': FONT})

dataloader = DataLoader()
dataloader.load_data('assets/The_Oscar_Award_Demographics_1928-2025 - The_Oscar_Award_Demographics_1928-2025_v3.csv')
dataloader.preprocess_data()
df = dataloader.filter_data(1928, 2025)
distribution_dict, total = dataloader.get_unique_distribution(df)

# Fonctions utilitaires pour les callbacks
def get_filtered_distribution(year_range, category, winner_filter, include_other=False):
    """Fonction utilitaire pour obtenir la distribution filtrée des données"""
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=is_winner)
    distribution_dict, _ = dataloader.get_unique_distribution(df)
    
    # Préparation des options pour la checklist
    options = [{'label': key, 'value': key} for key in distribution_dict[category].keys()]
    if include_other:
        options.append({'label': 'Other', 'value': 'Other'})
    
    # Sélection des 5 premières catégories par défaut
    selected_categories = list(distribution_dict[category].keys())[:5]
    if include_other and len(distribution_dict[category]) > 5:
        selected_categories.append('Other')
    
    return df, distribution_dict, options, selected_categories


# Callbacks pour Figure 1
@app.callback(
    Output('category-checklist_fig_1', 'options'),
    Output('category-checklist_fig_1', 'value'),
    Input('year-slider_fig_1', 'value'),
    Input('tabs_fig_1', 'value'),
    Input('winner-filter_fig_1', 'value'),
)
def update_category_dropdown_fig_1(year_range, category, winner_filter):
    # Filtrer par gagnants uniquement ou tous les nominés
    df, distribution_dict, options, selected = get_filtered_distribution(
        year_range, category, winner_filter, include_other=False
    )
    return options, selected

@app.callback(
    Output('waffle-chart', 'figure'),
    Input('year-slider_fig_1', 'value'),
    Input('tabs_fig_1', 'value'),
    Input('category-checklist_fig_1', 'value'),
    Input('winner-filter_fig_1', 'value'),
    allow_duplicate=True
)
def update_waffle_chart(year_range, category, selected_categories, winner_filter):
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=is_winner)
    distribution_dict, _ = dataloader.get_unique_distribution(df)
    wchart = figure_1.WaffleChart()
    class_num_dict = {key: distribution_dict[category][key] for key in selected_categories}
    # Trie du dictionnaire par valeur décroissante
    sorted_dict = dict(sorted(class_num_dict.items(), key=lambda item: item[1], reverse=True))
    return wchart.plot_scatter_waffle_chart(sorted_dict, df, category, height=hauteur_default_figure, is_winner=is_winner)

# Callbacks pour Figure 3
@app.callback(
    Output('category-checklist_fig_3', 'options'),
    Output('category-checklist_fig_3', 'value'),
    Input('year-slider_fig_3', 'value'),
    Input('tabs_fig_3', 'value'),
    Input('winner-filter_fig_3', 'value'),
)
def update_category_dropdown_fig_3(year_range, category, winner_filter):
    df, distribution_dict, options, selected = get_filtered_distribution(
        year_range, category, winner_filter, include_other=True
    )
    return options, selected

@app.callback(
    Output('line-chart', 'figure'),
    Input('year-slider_fig_3', 'value'),
    Input('tabs_fig_3', 'value'),
    Input('category-checklist_fig_3', 'value'),
    Input('winner-filter_fig_3', 'value'),
    Input('scale-selector_fig_3', 'value'),
    allow_duplicate=True
)
def update_line_chart(year_range, category, selected_categories, winner_filter, scale_type):
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=is_winner)
    
    # Données détaillées pour l'affichage au survol
    hover_df = df.copy()
    
    # Obtenir les données cumulatives
    distribution_dict = dataloader.get_cumulative_yearly_distribution(
        df[['Year_Ceremony', category]], 
        selected_categories,
        time_granularity=1
    )
    
    line_chart = figure_3.LineChart()
    
    return line_chart.plot_line_chart(
        distribution_dict, 
        category, 
        selected_categories, 
        hover_df, 
        cumulative=True, 
        scale_type=scale_type,
        height=hauteur_default_figure
    )

# Callbacks pour Figure 4
@app.callback(
    Output('category-checklist_fig_4', 'options'),
    Output('category-checklist_fig_4', 'value'),
    Input('year-slider_fig_4', 'value'),
    Input('tabs_fig_4', 'value'),
    Input('winner-filter_fig_4', 'value'),
)
def update_category_dropdown_fig_4(year_range, category, winner_filter):
    df, distribution_dict, options, selected = get_filtered_distribution(
        year_range, category, winner_filter, include_other=True
    )
    return options, selected

@app.callback(
    Output('stacked-area-chart', 'figure'),
    Input('year-slider_fig_4', 'value'),
    Input('tabs_fig_4', 'value'),
    Input('category-checklist_fig_4', 'value'),
    Input('winner-filter_fig_4', 'value'),
    Input('granularity-selector_fig_4', 'value'),
    allow_duplicate=True
)
def update_stacked_area_chart(year_range, category, selected_categories, winner_filter, time_granularity):
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=is_winner)
    # Extraction de l'année et de la catégorie
    distribution_dict = dataloader.get_yearly_distribution(
        df[['Year_Ceremony', category]], 
        selected_categories,
        time_granularity=time_granularity
    )
    
    stacked_chart = figure_4.StackedAreaChart()
    fig = stacked_chart.plot_stacked_area_chart(
        distribution_dict,
        height=hauteur_default_figure
    )
    
    # Configuration responsive
    fig.update_layout(
        autosize=True,
        margin=dict(l=30, r=30, t=30, b=50)
    )
    
    return fig

# Callbacks pour Figure 2
@app.callback(
    Output('category-checklist_fig_2', 'options'),
    Output('category-checklist_fig_2', 'value'),
    Input('year-slider_fig_2', 'value'),
    Input('tabs_fig_2', 'value'),
)
def update_category_dropdown_fig_2(year_range, category):
    df, distribution_dict, options, selected = get_filtered_distribution(
        year_range, category, "all", include_other=True
    )
    return options, selected

@app.callback(
    Output('figure-2-graph', 'figure'),
    Input('tabs_fig_2', 'value'),
    Input('year-slider_fig_2', 'value'),
    Input('category-checklist_fig_2', 'value')
)
def update_sankey_chart(demographic_column, year_range, selected_categories):
    # Inclure tous les nominés pour la comparaison
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=None)
    if selected_categories:
        df = df[df[demographic_column].isin(selected_categories)]
    sankey = figure_2.SankeyDemographicChart()
    return sankey.plot_sankey_chart(df, demographic_column, height=hauteur_default_figure)


if __name__ == '__main__':
    app.run(port=8070, debug=True)