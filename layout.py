from dash import html, dcc


def create_figure_section(figure_id, title, graph_id, has_checklist=True, has_control_elements=True, intervalle=[1928, 2025], font='Jost', explanation_text=None):
    """
    Génère un blueprint commun pour toutes les figures
    
    Args:
        figure_id: Identifiant de la figure (1, 2, 3, 4)
        title: Titre à afficher pour la figure
        graph_id: ID du graphique Dash
        has_checklist: Si True, inclut une checklist pour les catégories
        has_control_elements: Si True, inclut les éléments de contrôle
        intervalle: Intervalle d'années pour le slider
        font: Police de caractères à utiliser
        explanation_text: Texte explicatif pour la figure (optionnel)
        
    Returns:
        Une section de figure complète avec les contrôles
    """
    # Sélecteur de granularité temporelle (figure 4 uniquement)
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
    ], className='control-item', style={'padding': '10px'}) if figure_id == 4 else None
    
    # Filtres gagnants/nominés
    winners_filter = html.Div([
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
    ], className='control-item', style={'padding': '10px'})
    
    # Checklist des catégories
    checklist = html.Div([
        html.P('Filtres:'),
        dcc.Checklist(
            id=f'category-checklist_fig_{figure_id}',
            options=[],
            value=[],
            inline=True,
            className='dash-checklist'
        )
    ], className='control-item', style={'padding': '10px'}) if has_checklist else None
    
    # Slider d'années
    year_slider = html.Div([
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
    ], className='control-item year-slider', style={'padding': '10px'})
    
    # Sélecteur d'échelle (figure 3 uniquement)
    scale_selector = html.Div([
        html.P('Échelle:'),
        dcc.RadioItems(
            id=f'scale-selector_fig_{figure_id}',
            options=[
                {'label': 'Linéaire', 'value': 'linear'},
                {'label': 'Logarithmique', 'value': 'log'}
            ],
            value='linear',
            inline=True,
            className='radio-filter'
        )
    ], className='control-item', style={'padding': '10px'}) if figure_id == 3 else None
    
    # Assembler les contrôles actifs
    if has_control_elements:
        control_elements = [winners_filter]
    else:
        control_elements = []
    if checklist:
        control_elements.append(checklist)
    control_elements.append(year_slider)
    if granularity_selector:
        control_elements.append(granularity_selector)
    if scale_selector:
        control_elements.append(scale_selector)
    
    # Conteneur des contrôles
    controls = html.Div(
        control_elements,
        className='controls-container',
        style={'margin': '20px 0'}
    )
    
    return html.Div(children=[
        # Titre de la figure
        html.H3(title, className='figure-title'),
        
        # Explication de la figure
        dcc.Markdown(explanation_text, className='figure-explanation') if explanation_text else None,

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
            
            # Contrôles
            controls,
            
        ], style={'width': '100%', 'margin': '0 auto'}),
    ],
    style={'margin': '0 auto', 'width': '100%', 'fontFamily': font, 'display': 'block', 'textAlign': 'center'})