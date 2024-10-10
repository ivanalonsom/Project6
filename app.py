import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def show_boxplot(df_col):
    # Cargar datos
    df_outliers = pd.read_csv('data/df_all_outliers.csv')

    # Verificar si la columna 'clnt_tenure_mnth' existe
    if df_col.name in df_outliers.columns:
        # Crear el gráfico de cajas y bigotes
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df_col)
        plt.title(f'Gráfico de Cajas y Bigotes para {df_col.name}')
        plt.ylabel('Valores')
        plt.grid(True)
        st.pyplot(plt)
        
        # Mostrar outliers si existen
        desc = df_outliers['clnt_tenure_mnth'].describe()
        q1 = desc['25%']
        q3 = desc['75%']
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = df_outliers[(df_outliers[df_col.name].notna()) & (df_col < lower_bound) | (df_col > upper_bound)]
        if not outliers.empty:
            st.write(f"Outliers encontrados: {outliers.count()[0]}")
        else:
            st.write("No se encontraron outliers.")
    else:
        st.write("La columna no se encuentra en el DataFrame.")


def graph_bar_plot_control_v_test(df):
    # Filtrar los grupos de control y test utilizando la columna 'variation'
    df_control = df[df["variation"] == 0]
    df_test = df[df["variation"] == 1]

    # Contar y normalizar las ocurrencias de process_step en cada DataFrame
    control_counts = df_control['process_step'].value_counts(normalize=True).sort_index() * 100
    test_counts = df_test['process_step'].value_counts(normalize=True).sort_index() * 100

    # Crear un DataFrame para facilitar la comparación
    counts_df = pd.DataFrame({'Control (%)': control_counts, 'Test (%)': test_counts})

    # Graficar
    plt.figure(figsize=(10, 6))
    counts_df.plot(kind='bar')
    plt.title('Comparación Proporcional de process_step entre Control y Test')
    plt.xlabel('Process Step')
    plt.ylabel('Porcentaje de Ocurrencias (%)')
    plt.xticks(rotation=0)
    plt.legend(title='Grupo')
    plt.grid(axis='y')

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

 

def intro():
    st.image("https://ceblog.s3.amazonaws.com/wp-content/uploads/2018/06/29173427/ab-testing-2.jpg", use_column_width=True)
    st.markdown("<p style='text-align: right; font-size: 10px; padding: 0'>Image source: <em><a href=https://www.crazyegg.com/blog/ab-testing/'>https://www.crazyegg.com/blog/ab-testing/</em></a></p>", unsafe_allow_html=True)


    st.markdown("<style>h1 {text-align: justify;}</style>", unsafe_allow_html=True)
    st.title("Project 5 - Evaluation of Website Efficiency through Data Analysis using A/B Testing") 

    st.markdown("""<p style='font-size: 18px; text-align: justify'>
                 Intro al data.</p>
        """, unsafe_allow_html=True)
    
    
    st.markdown("<h3 style='color:gray; font-size: 18px'>Below is an example of the original dataframes, prior to the treatment performed.</h3>", unsafe_allow_html=True)
        

    if 'show_df' not in st.session_state:
        st.session_state.show_df = False    
    
    if 'show_boxplots' not in st.session_state:
        st.session_state.show_boxplots = False

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Show/Hide Dataframes"):
            st.session_state.show_df = not st.session_state.show_df

    with col2:
        if st.button("Show/Hide Boxplots"):
            st.session_state.show_boxplots = not st.session_state.show_boxplots

    
    if st.session_state.show_df:
        df_no_treatment_demo = pd.read_csv('original_data/df_final_demo.csv')
        df_no_treatment_experiment = pd.read_csv('original_data/df_final_experiment_clients.csv')
        df_no_treatment_webdataConcat = pd.read_csv('original_data/df_web_data_concat.csv')

        st.markdown("<p style='color:gray'>Clients data .</p>", unsafe_allow_html=True)
        st.write(df_no_treatment_demo)

        st.markdown("<p style='color:gray'>Webdata.</p>", unsafe_allow_html=True)
        st.write(df_no_treatment_webdataConcat)

        st.markdown("<p style='color:gray'>Final experiment.</p>", unsafe_allow_html=True)
        st.write(df_no_treatment_experiment)

    
    if st.session_state.show_boxplots:

        df_outliers = pd.read_csv('data/df_all_outliers.csv')
        show_boxplot(df_outliers["clnt_tenure_mnth"])

        df_no_outliers = pd.read_csv('data/df_all_cleaned.csv')
        show_boxplot(df_no_outliers["clnt_tenure_mnth"])


def statistics():
    from statistics_tests import analyze_numeric_variables


    df_all = pd.read_csv('data/df_powerbi.csv')
    # df_control = pd.read_csv('data/df_control_propio.csv')
    # df_test = pd.read_csv('data/df_test_propio.csv')

        # Seleccionar solo columnas numéricas y excluir algunas que no interesan
    df_num = df_all.select_dtypes(include=['int64', 'float64']).copy()
    df_num.drop(['client_id', 'num_accts', 'process_step', 'variation'], axis=1, inplace=True)

    # Seleccionar solo columnas categóricas
    df_cat = df_all.select_dtypes(include=['object']).copy()

    # Mostrar estadísticas de las variables numéricas
    st.write("Numerical variables statistics:")
    st.write(df_num.describe())

    # Mostrar estadísticas de las variables categóricas
    st.write("Categorical variables statistics:")
    st.write(df_cat.describe())

    # Graficar las tasas de conversión entre control y test (por ejemplo)
    # graph_bar_plot_control_v_test(df_all)
    # Define el texto en formato Markdown
    markdown_text = """
    ## Resultados del Experimento

    ## Experiment Results
    **Completion Rate of the Control Group:**
    12.04%

    **Completion Rate of the Test Group:**
    13.81%

    ---

    ### Z-Test (Two-Proportion Test)
    **Z-Test Result:**
    **Z-Statistic: -12.2592
    **P-Value: 1.50e-34
    **Conclusion:** We can state with 95% confidence that the difference in completion rates is statistically significant (we reject H0).


    ---

    ### Relative Increase Threshold
    - **Observed Increase:**
    The observed increase is 14.69%, meeting the 5% threshold.

    ---

    ### Chi-Square Test
    - **Chi-Square:** 150.1313
    - **P-Value:** 1.62e-34
    - **Conclusion:** The difference in completion rates is statistically significant (we reject H0)

    ---

    ### General Interpretation
    The results of the statistical tests (Z-Test and Chi-Square) confirm that the new user interface has a positive and significant impact on 
    the completion rate of the process compared to the traditional interface. Additionally, the relative increase in the completion rate of 
    the test group exceeds the 5% threshold, indicating that the new interface not only improves user experience but also contributes to 
    greater effectiveness in process completion.
    """

    # Mostrar el texto en formato Markdown en Streamlit
    st.markdown(markdown_text)

    st.write("A continuación se muestran las estadísticas de correlación de las variables numéricas:")
    st.pyplot(analyze_numeric_variables(df_all))


def prueba():
    st.markdown("""
            ## Vanguard Customer Experience Analysis
<p align="center">
<img src="https://fondosindexados.es/wp-content/uploads/2018/08/fondos-vanguard-logo.jpg" alt="Vanguard Logo">
</p>

## Project Overview

This project involves analyzing the results of a digital experiment conducted by **Vanguard**, a US-based investment management company. The goal is to determine whether a modernized, more intuitive user interface (UI) and timely contextual cues could improve the online process completion rates for Vanguard customers.

The experiment involved an A/B test with a **control group** (using the traditional UI) and a **test group** (using the new UI). By analyzing the data from this experiment, the aim is to see if the changes in the UI led to an improved user experience and higher process completion rates.

## Relevant Client Insights and conclusions 
[Tableau story - Clients analysis.](https://public.tableau.com/views/ABTesting_Project_Clients_Analysis/Clientinsights?:language=es-ES&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)  
## Relevant AB Testing Results 
PowerBI dashboard - Relevant Insights  



https://github.com/user-attachments/assets/98c2749f-6b8b-4c2e-8061-b89b30541c5f





## The Digital Challenge

Vanguard’s digital transformation aimed to enhance the online user experience by:
- Implementing a more intuitive UI.
- Adding contextual prompts such as messages, suggestions, or instructions.

The central question is: **Did these changes lead to more customers completing the process?**

### Experiment Overview
The A/B test was conducted from **March 15, 2017** to **June 20, 2017**, comparing:
- **Control Group**: Customers interacted with the traditional Vanguard online process.
- **Test Group**: Customers experienced the new, improved digital interface.

Both groups went through the same sequence: a landing page, three subsequent steps, and a confirmation page indicating process completion.

## Objectives

The main objective of this project is to:
- Analyze if the **new UI** leads to better **completion rates** compared to the traditional UI.
- Explore demographic factors that might influence the results, such as **age**, **gender**, or **account type**.
- Provide data-driven insights and recommendations based on the experiment results.

## Analysis Plan

1. **Data Cleaning & Preprocessing**:
   - Merge and clean the digital footprints dataset (`df_final_web_data` part 1 and part 2).
   - Handle missing values and ensure consistency in the customer profile data.
   
2. **Exploratory Data Analysis (EDA)**:
   - Analyze completion rates for both the control and test groups.
   - Investigate the impact of demographic factors on the experiment outcomes.

3. **Statistical Testing**:
   - Perform statistical tests to determine if the differences between the control and test groups are significant.
   - Use tools like **A/B testing** to quantify the effect of the new UI.

4. **Conclusion**:
   - Provide insights into whether the new UI improves the process completion rate.
   - Offer recommendations for future improvements based on data analysis.

## Tools & Technologies

- **Python** for data manipulation and analysis.
- **Pandas** for handling datasets.
- **Seaborn** and **Matplotlib** for data visualization.
- **SciPy/Statsmodels** for statistical testing (A/B test analysis).

## Datasets

The following datasets are used for this analysis:

1. **Customer Profiles (`df_final_demo`)**: Contains demographic data like age, gender, and account details of Vanguard's customers.
   
2. **Digital Footprints (`df_final_web_data`)**: Provides detailed records of online customer interactions, split into two parts (`pt_1` and `pt_2`). These parts must be merged before in-depth analysis.

3. **Experiment List (`df_final_experiment_clients`)**: Reveals which customers participated in the A/B experiment (either as part of the control or test group).

    [\[Link to source\]](https://github.com/ivanalonsom/Project5_EDA_Inferential_Stats/tree/main/original_data)

## How to Run the Project

1. Clone the repository:
   ```bash
   git clone https://github.com/ivanalonsom/Project5_EDA_Inferential_Stats.git
2. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
3. Open and run the Jupyter notebooks for data analysis and visualization. 
""", unsafe_allow_html=True)


st.sidebar.title("Navegation")
page = st.sidebar.selectbox("Select a page", ["Introduction", "Statistics", "Insights and conclusions"]) 
st.sidebar.markdown("<br>" * 20, unsafe_allow_html=True)
st.sidebar.markdown("""  
                ## This project has been developed by:
                Iván Alonso - https://github.com/ivanalonsom  
                Danny Rodas - https://github.com/cohet3
                """)

if page == "Introduction":
    intro()
elif page == 'Statistics':
    statistics()
elif page == 'Insights and conclusions':
    prueba()




