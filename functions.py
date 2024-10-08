def remove_dots(column_name):
    import re
    return re.sub(r'(\d)\.(?=\d)', r'\1', column_name)


def clean_df(df):
    import pandas as pd

    df.columns = [remove_dots(col) for col in df.columns]

    new_columns = {
        "Unnamed: 0" : "Region", 
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

    return df


def every_float_to_int(df):
    import pandas as pd

    df_temp = df.loc[:, df.columns != 'Region']
    df_temp = df_temp.astype(int)

    df = pd.concat([df["Region"], df_temp], axis=1)

    return df


def add_coordinates_from_dict(data_frame):
    
    autonomous_communities_coordinates = {
        'andalucia': {'Latitude': 37.3873, 'Longitude': -5.9869},
        'aragon': {'Latitude': 41.6488, 'Longitude': -0.8891},
        'asturias_principado_de': {'Latitude': 43.3619, 'Longitude': -5.8494},
        'balears_illes': {'Latitude': 39.5712, 'Longitude': 2.6466},
        'canarias': {'Latitude': 28.2916, 'Longitude': -16.6291},
        'cantabria': {'Latitude': 43.1828, 'Longitude': -3.9878},
        'castilla_y_leon': {'Latitude': 41.6523, 'Longitude': -4.7245},
        'castilla_-_la_mancha': {'Latitude': 39.8628, 'Longitude': -4.0273},
        'cataluna': {'Latitude': 41.3851, 'Longitude': 2.1734},
        'comunitat_valenciana': {'Latitude': 39.4699, 'Longitude': -0.3763},
        'extremadura': {'Latitude': 39.4765, 'Longitude': -6.3722},
        'galicia': {'Latitude': 42.5751, 'Longitude': -8.1339},
        'madrid_comunidad_de': {'Latitude': 40.4168, 'Longitude': -3.7038},
        'murcia_region_de': {'Latitude': 37.9922, 'Longitude': -1.1307},
        'navarra_comunidad_foral_de': {'Latitude': 42.6954, 'Longitude': -1.6761},
        'pais_vasco': {'Latitude': 43.2630, 'Longitude': -2.9349},
        'rioja_la': {'Latitude': 42.2871, 'Longitude': -2.5396},
        'ciudad_autonoma_de_ceuta': {'Latitude': 35.8894, 'Longitude': -5.3198},
        'ciudad_autonoma_de_melilla': {'Latitude': 35.2930, 'Longitude': -2.9387}
    }
    
    def get_lat_long(region):
        community_clean = region.strip()
        if community_clean in autonomous_communities_coordinates:
            return autonomous_communities_coordinates[community_clean]['Latitude'], autonomous_communities_coordinates[community_clean]['Longitude']
        else:
            print(f"Warning: Coordinates not found for {community_clean}")
            return None, None
    
    data_frame['Latitude'], data_frame['Longitude'] = zip(*data_frame['Autonomous Community'].apply(get_lat_long))
    
    return data_frame

def clean_region_names(data_frame):
    def clean_name(name):
        return name.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ñ", "n")

    data_frame['region_cleaned'] = data_frame['Region'].apply(clean_name)
    
    return data_frame