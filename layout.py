from dash import html, dcc


def create_figure_section(figure_id, title, graph_id, has_checklist=True, intervalle=[1928, 2025], font='Jost'):
    """
    Génère un blueprint commun pour toutes les figures
    
    Args:
        figure_id: Identifiant de la figure (1, 2, 3, 4)
        title: Titre à afficher pour la figure
        graph_id: ID du graphique Dash
        has_checklist: Si True, inclut une checklist pour les catégories
        
    Returns:
        Une section de figure complète avec les contrôles
    """
    # Ajouter un sélecteur de granularité temporelle spécifiquement pour la figure 4
    granularity_selector = html.Div([
        html.P("Granularité temporelle:"),
        dcc.RadioItems(
            id=f'granularity-selector_fig_{figure_id}',
            options=[
                {'label': 'Année par année', 'value': 1},
                {'label': 'Par 5 ans', 'value': 5},
                {'label': 'Par décennie', 'value': 10}
            ],
            value=5,  # Valeur par défaut: regrouper par 5 ans
            inline=True,
            className='radio-filter'
        )
    ], style={'flex': '1', 'padding': '10px'}) if figure_id == 4 else None
    
    controls = html.Div([
        # Filtres (gauche)
        html.Div([
            html.P('Utilisez ces filtres pour visualiser plus de données:'),
            dcc.RadioItems(
                id=f'winner-filter_fig_{figure_id}',
                options=[
                    {'label': 'Gagnants seulement', 'value': 'winners'},
                    {'label': 'Gagnants et nominés', 'value': 'all'}
                ],
                value='winners',
                inline=True,
                className='radio-filter'
            )
        ], style={'flex': '1', 'padding': '10px'}),
        
        # Checklist (centre) - optionnelle
        html.Div([
            html.P('Filtres:'),
            dcc.Checklist(
                id=f'category-checklist_fig_{figure_id}',
                options=[],
                value=[],
                inline=True,
                className='dash-checklist'
            )
        ], style={'flex': '1', 'padding': '10px'}) if has_checklist else None,

        # Slider des années (droite)
        html.Div([
            html.P('Années:'),
            dcc.RangeSlider(
                id=f'year-slider_fig_{figure_id}',
                min=1928,
                max=2025,
                step=1,
                marks={i: '{}'.format(i) for i in range(1928, 2025, 10)},
                value=intervalle,
                allowCross=False
            )
        ], style={'flex': '1', 'padding': '10px'}),
        
        # Ajouter le sélecteur de granularité si applicable
        granularity_selector
        
    ], style={'margin': '20px 0', 'display': 'flex', 'flexDirection': 'row'})
    
    # Remplacer la section de contrôles existante par notre nouvelle version
    return html.Div(children=[
        # Titre de la figure
        html.H3(title, className='figure-title'),

        # Contenu principal
        html.Div([
            # Onglets de catégories
            dcc.Tabs(
                id=f'tabs_fig_{figure_id}',
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

            # Graphique
            dcc.Graph(id=graph_id, style={'width': '100%', 'margin': '40px 0'}),
            # dcc.Graph(id=graph_id, style={'width': '100%', 'margin': '40px 0' if figure_id == 1 else '0'}),
            
            # Controls (section modifiée)
            controls
            
        ], style={'width': '100%', 'margin': '0 auto'}),
    ],
    style={'margin': '0 auto', 'width': '100%', 'fontFamily': font, 'display': 'block', 'textAlign': 'center'})