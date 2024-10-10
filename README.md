# Crime trend in 2020 and 2021 in a non-COVID-19 scenario

## Overview

This project is a predictive analysis of crime statistics in Spain, focusing on how crime trends across different autonomous communities might have continued if the COVID-19 pandemic had not occurred. Specifically, the model aims to estimate crime levels in 2022 by following the trend observed from 2010, disregarding the drastic decrease in crime that occurred due to the lockdowns and other restrictions during the pandemic. The analysis leverages data cleaning, transformation, machine learning, and visualization techniques to provide insights into these hypothetical crime trends. This README will guide you through understanding the project components and how to run the code.

## Link to Streamlit
https://deep-learning-spain-crimen-study.streamlit.app/

## Team Members 

| Name             | LinkedIn Profile | Brief Description |
|----------------------------------|-------------------------------------------|-------------------------------------------|
| Iván Alonso        |   [LinkedIn](https://www.linkedin.com/in/ivan-alonsom/)   | Data Analyst |
| Luis H. Rodríguez Fuentes	 |   [LinkedIn](https://www.linkedin.com/in/luis-h-rodr%C3%ADguez-fuentes/)    | Data Analyst |



## Files in This Repository

1. **df_total.csv**: This file contains the full dataset of crime data, including different types of crimes across various regions in Spain.

2. **df_total_pca_values.csv**: This dataset contains the transformed features after applying Principal Component Analysis (PCA) to reduce the dimensionality of the original crime data.

3. **df_total_values.csv**: This file includes the cleaned and preprocessed values for the crime dataset, ready for analysis.

4. **functions.py**: A Python script containing utility functions used in this project. These functions perform various tasks, such as cleaning column names, converting floats to integers, adding latitude and longitude coordinates based on regions, and merging data for different years.

5. **main_principal.ipynb**: The Jupyter Notebook that includes all the analysis steps, data visualization, machine learning model training, and insights derived from the dataset. It orchestrates the use of other files, processing the data and displaying the results.

## Functionality

### Main Functions in functions.py

- **remove_dots(column_name)**: Cleans the column names by removing unnecessary dots that could create issues when processing.
- **clean_df(df)**: Cleans the dataset by renaming columns, removing unused columns, and standardizing the column names.
- **every_float_to_int(df)**: Converts all float values in the dataset (except for the region) to integers for easier data handling.
- **add_coordinates_from_dict(data_frame)**: Adds latitude and longitude columns to the data based on the Spanish region.
- **clean_region_names(data_frame)**: Standardizes region names to a consistent format for easier analysis.
- **delete_sub_crimes(df)**: Removes columns representing subcategories of crimes to focus on higher-level crime categories.
- **get_previous_years(df_unpivot_transformed)**: Adds columns to represent the crime data from previous years (up to 3 years back), allowing for trend analysis.

### Data Preprocessing

The `functions.py` script is crucial for data preprocessing. It helps in preparing the dataset for further analysis, including the following steps:

1. **Cleaning Column Names**: Unifies the naming convention and removes problematic characters.
2. **Adding Coordinates**: Enriches the dataset by adding geographical information, such as latitude and longitude, based on the autonomous community.
3. **Handling Missing Values**: Ensures all numerical columns are properly formatted and any `NaN` values are addressed.

## Machine Learning Development

The **main.ipynb** notebook includes the development of machine learning models to analyze and predict crime trends. The steps include:

- **Feature Selection and Engineering**: PCA is used to reduce the dimensionality of the data, enabling us to focus on the most important features contributing to crime rates. Specifically, PCA was used to reduce the number of columns representing values from previous years (`values_year_minus_1`, `values_year_minus_2`, and `values_year_minus_3`) into a single column (`values_year_PCA`) that retained 90% of the information. This allowed for a more concise representation without significant loss of information.
- **Conversion of Crime Types to Binary**: Each crime type is converted to a binary format to indicate the presence or absence of that crime type in a particular year and region. This transformation makes the data suitable for classification models and helps in understanding the distribution of different crime types.
- **Temporal Feature Engineering**: We expanded the dataset to include not only the crime statistics for each year but also for the previous year. This helps the model understand temporal trends and correlations in crime rates.
- **Model Selection**: A Random Forest classifier was selected for predicting crime trends, given its effectiveness in handling high-dimensional data and its ability to capture complex interactions among features.
- **Training and Evaluation**: The dataset was split into training and test sets to evaluate the performance of the Random Forest model. Metrics such as accuracy, precision, recall, and F1-score were used to determine the effectiveness of the model in predicting crime categories.
- **Hyperparameter Tuning**: Hyperparameter tuning was conducted using Random Search to optimize the performance of the Random Forest model. This involved testing different combinations of parameters such as the number of estimators, maximum depth, and minimum samples per leaf to identify the best-performing model configuration.
- **Cross-Validation**: K-Fold cross-validation was applied to ensure that the models are generalizable and not overfitting to the training data, providing a more robust evaluation of model performance.

## Analysis Notebook

The **main.ipynb** notebook performs the following:

- **Exploratory Data Analysis (EDA)**: Visualizes the crime trends across different regions and crime categories to understand patterns. This includes plotting heatmaps to understand correlations, bar charts to visualize crime frequency, and line plots to observe trends over time.
- **PCA Implementation**: Reduces the dataset's dimensionality for better visualization and interpretation of the results. PCA helped in identifying the most significant features contributing to crime rates and visualizing the overall variance in the data. In particular, PCA was used to combine the columns `values_year_minus_1`, `values_year_minus_2`, and `values_year_minus_3` into a single column (`values_year_PCA`) that retained 90% of the information, making the dataset more manageable and reducing model complexity.
- **Binary Transformation of Crime Data**: Each crime type was converted into binary values to facilitate classification tasks. This transformation was instrumental in simplifying the model training process and improving model interpretability.
- **Temporal Data Integration**: To enhance the model's capability to understand temporal relationships, each row was expanded to include crime statistics of the current year and the previous year. This allowed the model to capture trends and shifts over time, thereby enhancing its predictive performance.
- **Prediction Modeling**: A Random Forest classifier was used for prediction, which was tuned using Random Search to improve the accuracy of predictions. The model's hyperparameters such as `n_estimators`, `max_depth`, and `min_samples_split` were optimized to achieve the best performance. Evaluation metrics such as precision, recall, and F1-score were used to validate the results.
- **Hyperparameter Tuning**: Fine-tuning of the machine learning models was performed to improve accuracy and reduce prediction errors. Random Search was employed to efficiently navigate the hyperparameter space, and cross-validation ensured that the tuned model performed consistently across different subsets of the data.

## Model Performance Scores

The performance of the models was evaluated using different metrics for the years 2018 and 2019:

### 2018
- **Mean Absolute Error (MAE)**: 676.55
- **Root Mean Squared Error (RMSE)**: 4197.78
- **R² Score**: 0.9918

### 2019
- **Mean Absolute Error (MAE)**: 1073.83
- **Root Mean Squared Error (RMSE)**: 5660.86
- **R² Score**: 0.9859

These metrics indicate that the model performed well in predicting crime trends, with a high R² score for both years, demonstrating strong predictive power. The errors, while present, are within acceptable limits given the complexity of the data and the variations between regions.

## How to Run the Project

1. Clone this repository to your local machine:

   ```sh
   git clone https://github.com/ivanalonsom/Project6/tree/luis_branch_new
   cd Project6
   ```

2. Install the required Python packages:

   ```sh
   pip install -r requirements.txt
   ```

3. Run the Jupyter Notebook (**main.ipynb**) to see the data analysis and machine learning results:

   ```sh
   jupyter notebook main.ipynb
   ```

4. You can use **functions.py** to preprocess any updates to the dataset before running the analysis.

## Key Insights

- **Crime Trends by Region**: Certain regions showed higher prevalence in specific crime categories, suggesting targeted interventions.
- **Dimensionality Reduction**: PCA helped identify the most significant features contributing to crime rates, facilitating clearer visualization while reducing the complexity of the dataset.
- **Prediction of Crime Trends**: Leveraging historical data and region-based information enabled the prediction of potential future crime trends if the COVID-19 pandemic had not occurred.
- **Machine Learning Performance**: The use of hyperparameter tuning and cross-validation ensured that the models are robust and provide reliable predictions.
- **Temporal Analysis**: Including features from previous years improved the model's understanding of crime trends, making the predictions more accurate and insightful.

## Conclusions

The predicted data from 2018 to 2022 provides valuable insights into the trends in crime across Spain's autonomous communities if the COVID-19 pandemic had not intervened. Based on the model's results, the following conclusions can be drawn:

- **Continued Crime Growth**: Crime levels in 2022 would likely have followed the increasing trends seen in previous years (2010-2019), particularly in property-related crimes, such as theft and robbery. The absence of pandemic-related disruptions suggests a steady upward trajectory.
- **Regional Variability**: Certain regions, such as Andalucía and Madrid, would have continued to experience higher crime rates compared to other regions, indicating the need for targeted law enforcement and community support measures.
- **Violent Crimes**: The data suggests that violent crime levels would have remained relatively stable, following historical trends without any drastic increases or decreases, underscoring the need for ongoing intervention and prevention strategies.
- **Impact of PCA**: The use of PCA allowed us to effectively reduce data complexity while retaining critical information, which improved the efficiency of the machine learning model without compromising prediction accuracy.

These conclusions can help policymakers, law enforcement, and social services better understand the potential long-term crime trends and develop strategies that are proactive rather than reactive. The results also highlight the importance of considering external factors—such as a pandemic—when analyzing crime trends.

## Contributions

Contributions are welcome! Please feel free to submit a pull request or raise an issue to improve this analysis.

## License

This project is licensed under the MIT License.

## Contact

For any questions or feedback, please contact Iván Alonso and Luis H. Rodriguez.
