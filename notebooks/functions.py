from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd

def remove_dots(column_name):
    import re
    return re.sub(r'(\d)\.(?=\d)', r'\1', column_name)


def clean_df(df):
    import pandas as pd

    df.columns = [remove_dots(col) for col in df.columns]

    new_columns = {
        "Unnamed: 0" : "region", 
        "1 CONTRA LAS PERSONAS": "1_against_people",
        "11-Homicidios dolosos/asesinatos": "1.1_intentional_homicides_murders",
        "111-Homicidios dolosos/asesinatos consumados": "1.1.1_intentional_homicides_murders_committed",
        "12-Lesiones": "1.2_injuries",
        "13-Malos tratos ámbito familiar": "1.3_domestic_violence",
        "14-Otros contra las personas": "1.4_other_crimes_against_people",
        "2 CONTRA LA LIBERTAD": "2_against_freedom",
        "21-Malos tratos habituales en el ámbito familiar": "2.1_habitual_domestic_violence",
        "22-Otros contra la libertad": "2.2_other_crimes_against_freedom",
        "3 LIBERTAD SEXUAL": "3_sexual_freedom",
        "31-Agresión sexual": "3.1_sexual_assault",
        "32-Agresión sexual con penetración": "3.1.1_sexual_assault_with_penetration",
        "33-Corrupción de menores o incapacitados": "3.2_corruption_of_minors_or_disabled",
        "34-Pornografía de menores": "3.3_child_pornography",
        "35-Otros contra la libertad sexual": "3.4_other_crimes_against_sexual_freedom",
        "4 RELACIONES FAMILIARES": "4_family_relationships",
        "5 PATRIMONIO": "5_property_crimes",
        "51-Hurtos": "5.1_thefts",
        "52-Robos con fuerza en las cosas": "5.2_robbery_with_force",
        "521-Robos con fuerza en el interior de vehículos": "5.2.1_robbery_with_force_inside_vehicles",
        "522-Robos con fuerza en viviendas": "5.2.2_robbery_with_force_in_homes",
        "523-Robos con fuerza en establecimientos": "5.2.3_robbery_with_force_in_establishments",
        "53-Robos con violencia o intimidación": "5.3_robbery_with_violence_or_intimidation",
        "531-Robos con violencia en vía pública": "5.3.1_robbery_with_violence_in_public_ways",
        "532-Robos con violencia en viviendas": "5.3.2_robbery_with_violence_in_homes",
        "533-Robos con violencia en establecimientos": "5.3.3_robbery_with_violence_in_establishments",
        "54-Sustracción de vehículos": "5.4_vehicle_theft",
        "55-Estafas": "5.5_fraud",
        "551-Estafas informáticas": "5.5.1_computer_fraud",
        "56-Daños": "5.6_damage",
        "57-Contra la propiedad intelectual/industrial": "5.7_against_intellectual_industrial_property",
        "58-Blanqueo de capitales": "5.8_money_laundering",
        "59-Otros contra el patrimonio": "5.9_other_property_crimes",
        "6 SEGURIDAD COLECTIVA": "6_collective_security",
        "61-Tráfico de drogas": "6.1_drug_trafficking",
        "62-Contra la seguridad vial": "6.2_against_road_safety",
        "63-Otros contra la seguridad colectiva": "6.3_other_collective_security_crimes",
        "7 FALSEDADES": "7_forgeries",
        "8 ADMÓN PÚBLICA": "8_public_administration",
        "9 ADMÓN JUSTICIA": "9_justice_administration",
        "10 ORDEN PÚBLICO": "10_public_order",
        "11 LEGISLACIÓN ESPECIAL": "11_special_legislation",
        "12 OTRAS INFRACCIONES PENALES": "12_other_criminal_offenses",
        "TOTAL INFRACCIONES PENALES": "total_criminal_offenses",
        "Year": "year"
    }

    df = df.rename(columns=new_columns)

    if df.columns[-2] == "Unnamed: 45":
        df.drop("Unnamed: 45", axis=1, inplace=True)
    df.columns = df.columns.str.replace(' ', '_').str.replace('-', '_')
    df.drop("total_criminal_offenses", axis=1, inplace=True)
    return df


def every_float_to_int(df):
    import pandas as pd

    df_temp = df.loc[:, df.columns != 'region']
    df_temp = df_temp.astype(int)

    df = pd.concat([df["region"], df_temp], axis=1)

    return df


def add_coordinates_from_dict(data_frame):
    
    autonomous_communities_coordinates = {
        'ANDALUCÍA': {'latitude': 37.3873, 'longitude': -5.9869},
        'ARAGÓN': {'latitude': 41.6488, 'longitude': -0.8891},
        'ASTURIAS (PRINCIPADO DE)': {'latitude': 43.3619, 'longitude': -5.8494},
        'BALEARS (ILLES)': {'latitude': 39.5712, 'longitude': 2.6466},
        'CANARIAS': {'latitude': 28.2916, 'longitude': -16.6291},
        'CANTABRIA': {'latitude': 43.1828, 'longitude': -3.9878},
        'CASTILLA Y LEÓN': {'latitude': 41.6523, 'longitude': -4.7245},
        'CASTILLA - LA MANCHA': {'latitude': 39.8628, 'longitude': -4.0273},
        'CATALUÑA': {'latitude': 41.3851, 'longitude': 2.1734},
        'COMUNITAT VALENCIANA': {'latitude': 39.4699, 'longitude': -0.3763},
        'EXTREMADURA': {'latitude': 39.4765, 'longitude': -6.3722},
        'GALICIA': {'latitude': 42.5751, 'longitude': -8.1339},
        'MADRID (COMUNIDAD DE)': {'latitude': 40.4168, 'longitude': -3.7038},
        'MURCIA (REGIÓN DE)': {'latitude': 37.9922, 'longitude': -1.1307},
        'NAVARRA (COMUNIDAD FORAL DE)': {'latitude': 42.6954, 'longitude': -1.6761},
        'PAÍS VASCO': {'latitude': 43.2630, 'longitude': -2.9349},
        'RIOJA (LA)': {'latitude': 42.2871, 'longitude': -2.5396},
        'CIUDAD AUTÓNOMA DE CEUTA': {'latitude': 35.8894, 'longitude': -5.3198},
        'CIUDAD AUTÓNOMA DE MELILLA': {'latitude': 35.2930, 'longitude': -2.9387}
    }
    
    def get_lat_long(region):
        community_clean = region.strip()
        if community_clean in autonomous_communities_coordinates:
            return autonomous_communities_coordinates[community_clean]['latitude'], autonomous_communities_coordinates[community_clean]['longitude']
        else:
            print(f"Warning: Coordinates not found for {community_clean}")
            return None, None
    
    data_frame['latitude'], data_frame['longitude'] = zip(*data_frame['region'].apply(get_lat_long))
    
    return data_frame

def clean_region_names(data_frame):
    def clean_name(name):
        return name.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")

    data_frame['region_cleaned'] = data_frame['region'].apply(clean_name)
    
    return data_frame


def delete_sub_crimes(df):
    import re

    df = df.loc[:, ~df.columns.str.match(r'^\d{2,}')]

    return df


def convert_region_into_numeric(df_col, crimesdf):

    if crimesdf:
        regions = {
        "ANDALUCÍA": 0,
        "ARAGÓN": 1,
        "ASTURIAS (PRINCIPADO DE)": 2,
        "BALEARS (ILLES)": 3,
        "CANTABRIA": 4,
        "CANARIAS": 5,
        "CASTILLA - LA MANCHA": 6,
        "CASTILLA Y LEÓN": 7,
        "CATALUÑA": 8,
        "CIUDAD AUTÓNOMA DE CEUTA": 9,
        "CIUDAD AUTÓNOMA DE MELILLA": 10,
        "COMUNITAT VALENCIANA": 11,
        "EXTREMADURA": 12,
        "GALICIA": 13,
        "MADRID (COMUNIDAD DE)": 14,
        "MURCIA (REGIÓN DE)": 15,
        "NAVARRA (COMUNIDAD FORAL DE)": 16,
        "PAÍS VASCO": 17,
        "RIOJA (LA)": 18
        }
        
    else:
        regions = {
        "01 Andalucía": 0,
        "02 Aragón": 1,
        "03 Asturias Principado de": 2,
        "04 Balears Illes": 3,
        "06 Cantabria": 4,
        "05 Canarias": 5,
        "08 Castilla - La Mancha": 6,
        "07 Castilla y León": 7,
        "09 Cataluña": 8,
        "18 Ceuta": 9,
        "19 Melilla": 10,
        "10 Comunitat Valenciana": 11,
        "11 Extremadura": 12,
        "12 Galicia": 13,
        "13 Madrid Comunidad de": 14,
        "14 Murcia Región de": 15,
        "15 Navarra Comunidad Foral de": 16,
        "16 País Vasco": 17,
        "17 Rioja La": 18
    }
        
    return df_col.replace(regions)


def get_previous_years(df_unpivot_transformed):
    import pandas as pd

    df_try_minus_years = df_unpivot_transformed 

    df_previous_year = df_unpivot_transformed.copy()
    df_previous_year['year'] += 1 
    df_previous_year = df_previous_year[['year', 'region', 'variable', 'value']]
    df_previous_year.rename(columns={'value': 'values_year_minus_1'}, inplace=True)

    df_try_minus_years = pd.merge(
        df_try_minus_years,
        df_previous_year,
        on=['year', 'region', 'variable'],
        how='left'
    )

    df_try_minus_years


    df_previous_year_2 = df_unpivot_transformed.copy()
    df_previous_year_2['year'] += 2  
    df_previous_year_2 = df_previous_year_2[['year', 'region', 'variable', 'value']]
    df_previous_year_2.rename(columns={'value': 'values_year_minus_2'}, inplace=True)

    df_try_minus_years = pd.merge(
        df_try_minus_years,
        df_previous_year_2,
        on=['year', 'region', 'variable'],
        how='left'
    )

    df_previous_year_3 = df_unpivot_transformed.copy()
    df_previous_year_3['year'] += 3  
    df_previous_year_3 = df_previous_year_3[['year', 'region', 'variable', 'value']]
    df_previous_year_3.rename(columns={'value': 'values_year_minus_3'}, inplace=True)

    df_try_minus_years = pd.merge(
        df_try_minus_years,
        df_previous_year_3,
        on=['year', 'region', 'variable'],
        how='left'
    )
    
    df_try_minus_years = df_try_minus_years.dropna(subset=['values_year_minus_1', 'values_year_minus_2', 'values_year_minus_3']).reset_index(drop=True)
    
    return df_try_minus_years


def apply_pca(df, columns, n_components=0.9, random_state=42):
    """
    Apply PCA to the specified columns of a DataFrame and add the PCA results to a copy of the original DataFrame.

    Parameters:
    df (pd.DataFrame): The original DataFrame.
    columns (list): The list of columns to apply PCA on.
    n_components (float or int): Number of components to keep. If 0 < n_components < 1, it represents the variance ratio.
    random_state (int): Random state for reproducibility.

    Returns:
    pd.DataFrame: A new DataFrame with the PCA results added.
    """
    # Extract the data for the specified columns
    values_data = df[columns]

    # Standardize the data
    scaler = StandardScaler()
    values_scaled = scaler.fit_transform(values_data)

    # Apply PCA
    pca = PCA(n_components=n_components, random_state=random_state)
    pca_result = pca.fit_transform(values_scaled)

    # Create PCA column names
    pca_columns = [f'Value_year_PCA{i+1}' for i in range(pca_result.shape[1])]
    df_pca_values = pd.DataFrame(pca_result, columns=pca_columns)

    # Create a copy of the original DataFrame and add the first PCA component
    df_pca = df.copy()
    df_pca['Values_year_PCA'] = df_pca_values['Value_year_PCA1']

    # Drop the original columns used for PCA
    df_pca = df_pca.drop(columns=columns)

    return df_pca