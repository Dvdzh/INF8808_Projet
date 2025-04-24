import pandas as pd 
import math
import plotly.colors as pc
import plotly.express as px
import numpy as np

# Couleurs personnalisées pour les marqueurs dans le diagramme en gaufre
CUSTOM_COLORS = [
    '#FFFFFF',  # Blanc
    '#000000',  # Noir
    '#BE8F4D',  # Bronze
    '#FFDA6E',  # Or
    '#C56D65',  # Rose
    '#593A1E'   # Marron
]

TRANSPARENT = 'rgba(0,0,0,0)'

class DataLoader():

    def __init__(self):
        self.data = None

    def load_data(self, path):
        self.data = pd.read_csv(path)
    
    def preprocess_data(self):
        self.data['Birth_Date'] = pd.to_datetime(self.data['Birth_Date'], format='%Y-%m-%d', errors='coerce')
        self.data['Ceremony_Date'] = pd.to_datetime(self.data['Year_Ceremony'], format='%Y').apply(lambda x: x.replace(month=3, day=1))
        self.data['Age'] = ((self.data['Ceremony_Date'] - self.data['Birth_Date']).dt.days / 365.25).apply(math.floor, 0)
        # Regrouper dans des tranches d'âges de 10 ans
        self.data['Age'] = (self.data['Age'] // 10) * 10
        self.data = self.data.drop(columns=['Birth_Date', 'Birth_Place', 'Ceremony_Date', 'Link', 'Ceremony_Date'])
        return self.data
    
    def filter_data(self, start_year, end_year, is_winner=None):
        """
        Filtre les données en fonction des années de début et de fin et du statut de gagnant.
        
        Args:
            start_year (int): L'année de début pour le filtrage
            end_year (int): L'année de fin pour le filtrage
            is_winner (bool, optional): Si True, seuls les gagnants sont inclus. 
                                      Si False, seuls les non-gagnants. 
                                      Si None, les gagnants et les nominés sont inclus.
        
        Returns:
            pandas.DataFrame: Le dataframe filtré
        """
        filtered_df = self.data[(self.data['Year_Ceremony'] >= start_year) & 
                              (self.data['Year_Ceremony'] <= end_year)]
        
        # Appliquer le filtre de gagnant si spécifié
        if is_winner is not None:
            filtered_df = filtered_df[filtered_df['Win_Oscar?'] == is_winner]
            
        return filtered_df
    
    def get_unique_distribution(self, data):
        """ 
        Calcule la distribution des valeurs uniques pour chaque colonne.
        
        Returns:
            tuple: (distribution_dict, total) où distribution_dict contient les comptages 
                  pour chaque valeur unique et total est le nombre total d'enregistrements
        """
        df = data.copy()    
        df.drop(columns=['Category', 'Name', 'Film', 'Year_Ceremony', 'Win_Oscar?'], inplace=True)
        df = df.reindex(sorted(df.columns), axis=1)

        result_dict = {}
        for col in df.columns:
            result_dict[col] = df.groupby(col).size().to_dict()
            result_dict[col] = dict(sorted(result_dict[col].items(), key=lambda item: item[1], reverse=True))

        total = len(df)

        return result_dict, total
    
    def get_yearly_distribution(self, data, selected_categories=None, time_granularity=1):
        """
        Fonction qui retourne la distribution des valeurs uniques pour chaque année ou période.
        
        Paramètres:
        -----------
        data : pandas.DataFrame
            DataFrame contenant les données à analyser avec les colonnes Year_Ceremony et la catégorie étudiée
        selected_categories : list, optionnel
            Liste des catégories à inclure. Si 'Other' est présent, les catégories non sélectionnées seront regroupées
        time_granularity : int, par défaut=1
            Granularité temporelle: 1 pour année par année, 5 pour tranches de 5 ans, 10 pour décennies
            
        Retourne:
        --------
        dict
            Dictionnaire de la forme {période: {catégorie1: valeur1, catégorie2: valeur2, ...}}
        """
        df = data.copy()
        
        # Appliquer la granularité temporelle
        if time_granularity > 1:
            # Arrondir les années à la granularité spécifiée
            df['Year_Ceremony'] = (df['Year_Ceremony'] // time_granularity) * time_granularity
        
        df = df.groupby(['Year_Ceremony', df.columns[1]]).size().unstack(fill_value=0)
        df = df.astype(int)
        df = df.reindex(sorted(df.columns), axis=1)
        distribution_dict = {year: row.to_dict() for year, row in df.iterrows()}
        # Trier par année
        distribution_dict = dict(sorted(distribution_dict.items(), key=lambda item: item[0]))

        # Gestion de la catégorie "Other" si nécessaire
        need_other = False
        if selected_categories is not None:
            if 'Other' in selected_categories:
                selected_categories.remove('Other')
                need_other = True

        if selected_categories is not None:
            for year, distribution in distribution_dict.items():
                filtered_distribution = {key: distribution[key] for key in selected_categories if key in distribution}
                if need_other:
                    filtered_distribution['Other'] = sum(value for key, value in distribution.items() if key not in selected_categories)
                distribution_dict[year] = filtered_distribution

        return distribution_dict

    def get_cumulative_yearly_distribution(self, data, selected_categories=None, time_granularity=1):
        """
        Fonction qui retourne la distribution cumulative des valeurs pour chaque année ou période.
        
        Paramètres:
        -----------
        data : pandas.DataFrame
            DataFrame contenant les données avec les colonnes Year_Ceremony et la catégorie étudiée
        selected_categories : list, optionnel
            Liste des catégories à inclure. Si 'Other' est présent, les catégories non sélectionnées seront regroupées
        time_granularity : int, par défaut=1
            Granularité temporelle: 1 pour année par année, 5 pour tranches de 5 ans, 10 pour décennies
            
        Retourne:
        --------
        dict
            Dictionnaire de la forme {période: {catégorie1: valeur_cumulative1, catégorie2: valeur_cumulative2, ...}}
        """
        # Obtenir la distribution non-cumulative année par année
        yearly_distribution = self.get_yearly_distribution(data, selected_categories, time_granularity)
        
        # Convertir en dataframe pour faciliter le calcul cumulatif
        years = sorted(yearly_distribution.keys())
        categories = list(set().union(*[d.keys() for d in yearly_distribution.values()]))
        
        # Créer un DataFrame vide avec années comme index et catégories comme colonnes
        cumulative_df = pd.DataFrame(index=years, columns=categories).fillna(0)
        
        # Remplir avec les valeurs annuelles
        for year, dist in yearly_distribution.items():
            for category, count in dist.items():
                cumulative_df.loc[year, category] = count
        
        # Calculer les valeurs cumulatives
        cumulative_df = cumulative_df.cumsum()
        
        # Convertir le DataFrame en dictionnaire
        cumulative_dict = {year: row.to_dict() for year, row in cumulative_df.iterrows()}
        
        return cumulative_dict


def generate_color_dict(identifiers=None, n_colors=None, colorscale_name='Set1'):
    """
    Génère un dictionnaire associant des identifiants à des couleurs
    
    Paramètres:
    -----------
    identifiers : liste, optionnel
        Liste des identifiants de catégories à associer aux couleurs
    n_colors : int, optionnel
        Nombre de couleurs à générer si les identifiants ne sont pas fournis
    colorscale_name : str, par défaut='Set1'
        Nom de l'échelle de couleurs Plotly à utiliser
        
    Retourne:
    --------
    dict
        Dictionnaire associant chaque identifiant à une couleur
    """
    # Déterminer le nombre de couleurs nécessaires
    if identifiers is not None:
        n_colors = len(identifiers)
    elif n_colors is None:
        raise ValueError("Soit les identifiants, soit le nombre de couleurs doivent être fournis")
    
    # Obtenir des couleurs à partir de l'échelle de couleurs spécifiée
    try:
        # Pour les échelles de couleurs qualitatives/discrètes
        if colorscale_name in ['Plotly', 'D3', 'G10', 'T10', 'Alphabet', 
                              'Dark24', 'Light24', 'Set1', 'Set2', 'Set3', 
                              'Pastel1', 'Pastel2']:
            colors = getattr(pc.qualitative, colorscale_name)
            # Répéter les couleurs si nécessaire
            colors = (colors * (n_colors // len(colors) + 1))[:n_colors]
        else:
            # Pour les échelles de couleurs continues
            colorscale = getattr(px.colors.sequential, colorscale_name, None)
            if colorscale is None:
                colorscale = getattr(px.colors.diverging, colorscale_name, None)
            if colorscale is None:
                colorscale = getattr(px.colors.cyclical, colorscale_name, None)
            if colorscale is None:
                # Utiliser l'échelle de couleurs continue par défaut
                color_positions = np.linspace(0, 1, n_colors)
                colorscale = px.colors.sample_colorscale(colorscale_name, color_positions)
                colors = colorscale
            else:
                # Pour les listes de couleurs des modules sequential/diverging
                step = max(1, len(colorscale) // n_colors)
                colors = colorscale[::step][:n_colors]
                # Ajouter plus si nécessaire
                if len(colors) < n_colors:
                    indices = np.linspace(0, len(colorscale)-1, n_colors-len(colors)).astype(int)
                    colors.extend([colorscale[i] for i in indices])
    except (AttributeError, ValueError):
        # Utiliser l'échelle Viridis par défaut
        color_positions = np.linspace(0, 1, n_colors)
        colors = px.colors.sample_colorscale("Viridis", color_positions)
    
    # Créer la correspondance identifiants-couleurs
    if identifiers is not None:
        color_dict = {id_val: colors[i % len(colors)] for i, id_val in enumerate(identifiers)}
    else:
        color_dict = {i: colors[i % len(colors)] for i in range(n_colors)}
        
    return color_dict