# Overview
This project focuses on exploring and visualizing data from the bike-sharing-dataset Pecatu Bicycle.

# Requirements

To run this program , u need install following python framework:
matplotlib==3.10.0

pandas==2.2.3

scipy==1.14.1

seaborn==0.13.2

streamlit==1.41.1

# Setup Environment - Anaconda
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt


# Setup Environment - Shell/Terminal
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

# Run steamlit app
streamlit run dashboard.py
