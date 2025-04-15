# dash app
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import json  # Ajout de l'import json

import figures.figure_1 as figure_1
import figures.figure_3 as figure_3
import figures.figure_4 as figure_4
import figures.figure_2 as figure_2

from helper import DataLoader
from layout import create_figure_section

print('hello')

FONT = 'Jost'

hauteur_default_figure = 700

app = dash.Dash(__name__, 
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
                    {"name": "description", "content": "Analyse de la diversité aux Oscars"}
                ],
                # Ajout des balises pour configurer le favicon
                update_title=None)

# Modification du titre de l'onglet du navigateur
app.title = "Oscars - Analyse de diversité"

# Ajout du favicon dans le layout
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
                title='Lors des 97 cérémonies des Oscars, il y a eu 416 gagnants. Voici leur distribution.',
                graph_id='waffle-chart',
                has_checklist=True,
                intervalle=intervalle_defaut,
                font=FONT
            ),
            
            # Espace entre les figures
            html.Div(style={'height': '150px', 'width': '100%', 'clear': 'both'}),
            
            # Figure 2
            html.Div(children=[
                html.H3('Comparatif des profils démographiques des nominés et des gagnants', 
                       className='figure-title'),

                html.Div([
                    dcc.Tabs(
                        id='tabs_fig_2',
                        value='Race or Ethnicity',
                        children=[
                            dcc.Tab(label='Ethnie', value='Race or Ethnicity', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Genre', value='Gender', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Religion', value='Religion', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Âge', value='Age', className='dash-tab', selected_className='dash-tab--selected'),
                            dcc.Tab(label='Orientation', value='Sexual orientation', className='dash-tab', selected_className='dash-tab--selected')
                        ],
                        className='dash-tabs'
                    ),

                    # Contrôles pour la figure 2
                    html.Div([
                        dcc.RadioItems(
                            id='winner-filter_fig_2',
                            #options=[
                           #     {'label': 'Gagnants seulement', 'value': 'winners'},
                                #{'label': 'Gagnants et nominés', 'value': 'all'}
                            #],
                            value='winners',
                            inline=True,
                            className='radio-filter'
                        )
                    ], style={'margin': '10px 0'}),

                    # Placeholder pour la figure 2
                    dcc.Graph(id='figure-2-graph', style={'width': '100%'}),

                    # Slider pour la plage d'années
                    dcc.RangeSlider(
                        id='year-slider_fig_2',
                        min=1928,
                        max=2025,
                        step=1,
                        marks={i: '{}'.format(i) for i in range(1928, 2025, 10)},
                        value=intervalle_defaut,
                        allowCross=False
                    )
                ], style={'width': '100%', 'margin': '0 auto'}),
            ],
            style={'margin': '0 auto', 'width': '100%', 'fontFamily': FONT, 'display': 'block', 'textAlign': 'center'}
            ),
            
            # Espace entre les figures
            html.Div(style={'height': '150px', 'width': '100%', 'clear': 'both'}),

            # Figure 3
            create_figure_section(
                figure_id=3,
                title='Évolution de la diversité au fil des ans',
                graph_id='line-chart',
                has_checklist=True,
                intervalle=intervalle_defaut,
                font=FONT
            ),
            
            # Espace entre les figures
            html.Div(style={'height': '150px', 'width': '100%', 'clear': 'both'}),
            
            # Figure 4
            create_figure_section(
                figure_id=4,
                title='L\'évolution de la diversité aux Oscars à travers les décennies.',
                graph_id='stacked-area-chart',
                has_checklist=True,
                intervalle=intervalle_defaut,
                font=FONT
            ),
            
            # Espace après la dernière figure
            html.Div(style={'height': '150px', 'width': '100%', 'clear': 'both'}),
        ],
        style={'width': '90%', 'margin': '0 auto', 'fontFamily': FONT, 'display': 'flex', 'flexDirection': 'column'}
        ),
        
        # Ajout d'un footer pour les crédits du logo et des créateurs
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

# Figure 1

# Figure 1

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


# Callback pour figure 1
@app.callback(
    Output('category-checklist_fig_1', 'options'),
    Output('category-checklist_fig_1', 'value'),
    Input('year-slider_fig_1', 'value'),
    Input('tabs_fig_1', 'value'),
    Input('winner-filter_fig_1', 'value'),
)
def update_category_dropdown_fig_1(year_range, category, winner_filter):
    # Filtrer par gagnants uniquement ou tous les nominés selon la valeur du bouton radio
    # TODO : Trier les catégories par nombre de représentants
    df, distribution_dict, options, selected = get_filtered_distribution(
        year_range, category, winner_filter, include_other=False
    )
    return options, selected

# Callback pour changer le waffle-chart 
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
    # sort the dictionary by value
    sorted_dict = dict(sorted(class_num_dict.items(), key=lambda item: item[1], reverse=True))
    return wchart.plot_scatter_waffle_chart(sorted_dict, df, category, height=hauteur_default_figure)
    # raise ValueError({key: distribution_dict[category][key] for key in selected_categories})
    # return wchart.plot_scatter_waffle_chart({key: distribution_dict[category][key] for key in selected_categories}, df, category)

# Figure 3

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
    Input('scale-selector_fig_3', 'value'),  # Nouvel input pour l'échelle
    allow_duplicate=True
)
def update_line_chart(year_range, category, selected_categories, winner_filter, scale_type):
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=is_winner)
    
    # Pour les données détaillées que nous allons afficher dans le hover
    hover_df = df.copy()
    
    # Utiliser get_cumulative_yearly_distribution pour obtenir les données cumulatives
    distribution_dict = dataloader.get_cumulative_yearly_distribution(
        df[['Year_Ceremony', category]], 
        selected_categories,
        time_granularity=1
    )
    
    # Initialize the line chart object
    line_chart = figure_3.LineChart()
    
    # Render the line chart with cumulative data and selected scale type
    return line_chart.plot_line_chart(
        distribution_dict, 
        category, 
        selected_categories, 
        hover_df, 
        cumulative=True, 
        scale_type=scale_type,
        height=hauteur_default_figure  # Ajout du paramètre de hauteur
    )

# Figure 4 

# Callback pour figure 4
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

# Callback pour le stacked area chart
@app.callback(
    Output('stacked-area-chart', 'figure'),
    Input('year-slider_fig_4', 'value'),
    Input('tabs_fig_4', 'value'),
    Input('category-checklist_fig_4', 'value'),
    Input('winner-filter_fig_4', 'value'),
    Input('granularity-selector_fig_4', 'value'),  # Nouveau input pour la granularité
    allow_duplicate=True
)
def update_stacked_area_chart(year_range, category, selected_categories, winner_filter, time_granularity):
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=is_winner)
    # On ne garde que l'année et la colonne de la catégorie
    distribution_dict = dataloader.get_yearly_distribution(
        df[['Year_Ceremony', category]], 
        selected_categories,
        time_granularity=time_granularity
    )
    
    stacked_chart = figure_4.StackedAreaChart()
    # Spécifier la hauteur souhaitée
    fig = stacked_chart.plot_stacked_area_chart(
        distribution_dict,
        height=hauteur_default_figure  # Hauteur en pixels
    )
    
    # Ajuster la mise en page selon la taille de l'écran
    fig.update_layout(
        autosize=True,
        margin=dict(l=30, r=30, t=30, b=50)  # Marges réduites pour les petits écrans
    )
    
    return fig

@app.callback(
    Output('figure-2-graph', 'figure'),
    Input('tabs_fig_2', 'value'),
    Input('winner-filter_fig_2', 'value'),
    Input('year-slider_fig_2', 'value'),
)
def update_sankey_chart(demographic_column, winner_filter, year_range):
    is_winner = None if winner_filter == 'all' else True
    df = dataloader.filter_data(year_range[0], year_range[1], is_winner=None)  # on prend tout pour comparer

    sankey = figure_2.SankeyDemographicChart()
    return sankey.plot_sankey_chart(df, demographic_column)


if __name__ == '__main__':
    app.run(port=8070, debug=True)