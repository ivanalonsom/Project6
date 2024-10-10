import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def intro():
    st.image("data/demo_heath_map.png", use_column_width=True)

    st.markdown("<style>h1 {text-align: justify;}</style>", unsafe_allow_html=True)
    st.title("Project 6 - What if COVID-19 would never exist? An insight to how crimes in Spain would have developed in 2020 and 2021") 

    st.markdown("""<p style='font-size: 18px; text-align: justify'>
                 This project is a predictive analysis of crime statistics in Spain, focusing on how crime trends across different autonomous communities might have continued if 
                the COVID-19 pandemic had not occurred. Specifically, the model aims to estimate crime levels in 2022 by following the trend observed from 2010, disregarding the 
                drastic decrease in crime that occurred due to the lockdowns and other restrictions during the pandemic. The analysis leverages data cleaning, transformation, 
                **deep learning**, and visualization techniques to provide insights into these hypothetical crime trends.</p>
        """, unsafe_allow_html=True)
    
    
    st.markdown("<h3 style='color:gray; font-size: 18px'>Below is an example of the original dataframes, prior to the treatment performed.</h3>", unsafe_allow_html=True)
        
    if 'show_df' not in st.session_state:
        st.session_state.show_df = True

    if st.session_state.show_df:
        df_no_treatment_demo = pd.read_csv('data/df_merged_national.csv')

        st.write(df_no_treatment_demo)
        st.markdown("<p style='color:gray; font-size: 12px; text-align: right'>Data obtained from INE.</h3>", unsafe_allow_html=True)


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

    st.write("Real data from INE vs Calculated and predicted data:")
    st.image("data/real_v_pred.jpg", use_column_width=True)

    




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




