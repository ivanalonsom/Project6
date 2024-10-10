import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# def show_boxplot(df_col):
#     # Cargar datos
#     df_outliers = pd.read_csv('data/df_all_outliers.csv')

#     # Verificar si la columna 'clnt_tenure_mnth' existe
#     if df_col.name in df_outliers.columns:
#         # Crear el gráfico de cajas y bigotes
#         plt.figure(figsize=(10, 6))
#         sns.boxplot(data=df_col)
#         plt.title(f'Gráfico de Cajas y Bigotes para {df_col.name}')
#         plt.ylabel('Valores')
#         plt.grid(True)
#         st.pyplot(plt)
        
#         # Mostrar outliers si existen
#         desc = df_outliers['clnt_tenure_mnth'].describe()
#         q1 = desc['25%']
#         q3 = desc['75%']
#         iqr = q3 - q1
#         lower_bound = q1 - 1.5 * iqr
#         upper_bound = q3 + 1.5 * iqr
        
#         outliers = df_outliers[(df_outliers[df_col.name].notna()) & (df_col < lower_bound) | (df_col > upper_bound)]
#         if not outliers.empty:
#             st.write(f"Outliers encontrados: {outliers.count()[0]}")
#         else:
#             st.write("No se encontraron outliers.")
#     else:
#         st.write("La columna no se encuentra en el DataFrame.")


# def graph_bar_plot_control_v_test(df):
#     # Filtrar los grupos de control y test utilizando la columna 'variation'
#     df_control = df[df["variation"] == 0]
#     df_test = df[df["variation"] == 1]

#     # Contar y normalizar las ocurrencias de process_step en cada DataFrame
#     control_counts = df_control['process_step'].value_counts(normalize=True).sort_index() * 100
#     test_counts = df_test['process_step'].value_counts(normalize=True).sort_index() * 100

#     # Crear un DataFrame para facilitar la comparación
#     counts_df = pd.DataFrame({'Control (%)': control_counts, 'Test (%)': test_counts})

#     # Graficar
#     plt.figure(figsize=(10, 6))
#     counts_df.plot(kind='bar')
#     plt.title('Comparación Proporcional de process_step entre Control y Test')
#     plt.xlabel('Process Step')
#     plt.ylabel('Porcentaje de Ocurrencias (%)')
#     plt.xticks(rotation=0)
#     plt.legend(title='Grupo')
#     plt.grid(axis='y')

#     # Mostrar el gráfico en Streamlit
#     st.pyplot(plt)

 

def intro():
    st.image("data/demo_heath_map.png", use_column_width=True)

    st.markdown("<style>h1 {text-align: justify;}</style>", unsafe_allow_html=True)
    st.title("Project 6 - What if Covid would never exist? An insight to the future of crime in Spain using Deep Learning") 

    st.markdown("""<p style='font-size: 18px; text-align: justify'>
                 This project is a predictive analysis of crime statistics in Spain, focusing on how crime trends across different autonomous communities might have continued if 
                the COVID-19 pandemic had not occurred. Specifically, the model aims to estimate crime levels in 2022 by following the trend observed from 2010, disregarding the 
                drastic decrease in crime that occurred due to the lockdowns and other restrictions during the pandemic. The analysis leverages data cleaning, transformation, 
                machine learning, and visualization techniques to provide insights into these hypothetical crime trends. This README will guide you through understanding the project 
                components and how to run the code.</p>
        """, unsafe_allow_html=True)
    
    
    st.markdown("<h3 style='color:gray; font-size: 18px'>Below is an example of the original dataframes, prior to the treatment performed.</h3>", unsafe_allow_html=True)
        
    if 'show_df' not in st.session_state:
        st.session_state.show_df = True

    if st.session_state.show_df:
        df_no_treatment_demo = pd.read_csv('data/df_merged_national.csv')

        st.write(df_no_treatment_demo)


def deep_learning():

    st.write("RF:")

    code = """
        df_total_predict_202021 = df_total_values_PCA.copy()

    future_years = [2020, 2021]

    for year in future_years:

    #Drop PCA var
    df_total_predict_202021 = df_total_predict_202021.drop(columns=['Values_year_PCA'], errors='ignore')

    #Recalculate year_minus
    df_total_predict_202021 = get_previous_years(df_total_predict_202021)

    #Apply PCA
    df_total_predict_202021 = apply_pca(df_total_predict_202021, columns_pca)

    #Predict next year
    X_year = df_total_predict_202021[df_total_predict_202021['year'] == year - 1][features_nn]
    y_pred_year = best_rf_model.predict(X_year)

    new_year_df = df_total_predict_202021[df_total_predict_202021['year'] == year - 1].copy()
    new_year_df['year'] = year
    new_year_df['value'] = y_pred_year

    df_total_predict_202021 = pd.concat([df_total_predict_202021, new_year_df], ignore_index=True)

    y_year = df_total_values[df_total_values['year'] == year]['value']
    """

    st.code(code, language='python')


    if 'show_df' not in st.session_state:
        st.session_state.show_df = True

    if st.session_state.show_df:
        df_predicted = pd.read_csv('data/df_201321_with_202021_predicted.csv')
        st.write("The dataframes after the treatment and prediction has been performed:")
        st.write(df_predicted)


def conclusions():
    st.write("The obtained score for Random Forest is:")
    st.code("Mean Absolute Error (MAE): 1033.0388923532064 \nRoot Mean Squared Error (RMSE): 4707.907926358289 \nR² Score: 0.9896681902859178")

    st.image("data/crimes_year_mean_pred.png", use_column_width=True)




st.sidebar.title("Navegation")
page = st.sidebar.selectbox("Select a page", ["Introduction", "Deep Learning", "Insights and conclusions"]) 
st.sidebar.markdown("<br>" * 20, unsafe_allow_html=True)
st.sidebar.markdown("""  
                ## This project has been developed by:
                Iván Alonso - https://github.com/ivanalonsom  
                Luis Rodríguez - https://github.com/LuisHRF
                """)

if page == "Introduction":
    intro()
elif page == 'Deep Learning':
    deep_learning()
elif page == 'Insights and conclusions':
    conclusions()




