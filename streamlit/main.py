import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import StandardScaler

import pickle

def load_model():
    return pickle.load(open('modelo_eleicao_campos', 'rb'))

def load_data():
    return pd.read_csv('candidatos.csv',sep=';',encoding = "ISO-8859-1")

def get_partidos(data):
    """
        Obtem a lista de partidos na eleição sem duplicatas
    """
    return np.unique(data['NM_PARTIDO'].values)

def get_nr_partido(data, nm_partido):
    """
        Obtem o número do partido a partir de seu nome
    """
    return data[data['NM_PARTIDO'] == nm_partido]['NR_PARTIDO'].values[0]

def create_parameters(data):
    """
        Criar os parâmetros (filtros) para a página
    """
    params = {}

    params['Idade'] = st.sidebar.slider('Idade', 16, 100, 30) 

    params['Gênero'] = st.sidebar.radio(
        label="Escolha o Gênero",
        options=['MASCULINO', 'FEMININO']
    )

    params['Valor Despesa'] = st.sidebar.slider('Despesa', 0, 100000, 50000) 
    params['Valor Receita'] = st.sidebar.slider('Receita', 0, 100000, 50000) 

    params['Raça'] = st.sidebar.selectbox(
        label="Escolha a Raça",
        options=['BRANCA', 'PARDA', 'PRETA', 'INDÍGENA', 'AMARELA']
    )

    params['Partido'] = st.sidebar.selectbox(
        label="Escolha o Partido",
        options=get_partidos(data)
    )

    params['Escolaridade'] = st.sidebar.selectbox(
        label="Escolha a Escolaridade",
        options=[
            'ENSINO MÉDIO COMPLETO', 
            'SUPERIOR COMPLETO', 
            'ENSINO FUNDAMENTAL COMPLETO', 
            'ENSINO FUNDAMENTAL INCOMPLETO', 
            'SUPERIOR INCOMPLETO', 
            'SUPERIOR ENSINO MÉDIO INCOMPLETO', 
            'LÊ E ESCREVE', 
        ]
    )

    return pd.DataFrame(params, index=[0]) 

def convert_data_to_model(data, df):
    """
        Converte os dados do dataframe em um formtado que modelo consiga processar
    """
    x_data = df.values.reshape(1, -1)

    # Obtendo o número do partido a partir do nome
    x_data[0, 5] = get_nr_partido(data, x_data[0, 5])

    genero_dict = {
        'FEMININO': 0, 
        'MASCULINO': 1
    }

    raca_dict = {
        'AMARELA': 0, 
        'BRANCA': 1, 
        'INDÍGENA': 2, 
        'NÃO INFORMADO': 3, 
        'PARDA': 4, 
        'PRETA': 5
    }

    escolaridade_dict = {
        'ENSINO FUNDAMENTAL COMPLETO': 0, 
        'ENSINO FUNDAMENTAL INCOMPLETO': 1, 
        'ENSINO MÉDIO COMPLETO': 2, 
        'ENSINO MÉDIO INCOMPLETO': 3, 
        'LÊ E ESCREVE': 4, 
        'SUPERIOR COMPLETO': 5, 
        'SUPERIOR INCOMPLETO': 6
    }

    x_data[0, 1] = genero_dict[x_data[0, 1]]
    x_data[0, 4] = raca_dict[x_data[0, 4]]
    x_data[0, 6] = escolaridade_dict[x_data[0, 6]]

    scaler = StandardScaler()
    return scaler.fit_transform(x_data)

def main():
    st.write("""
    # Predição Eleição 2020 - Campos 
    # """)
    st.write('---')

    st.sidebar.header('Escolha de paramentros para Predição')

    data = load_data()
    df = create_parameters(data)

    st.header('Parametros especificados')
    st.write(df)
    st.write('---')

    model = load_model()
    x_data = convert_data_to_model(data, df)

    prediction = model.predict(x_data)

    st.header('Situação Eleitoral Prevista')
    st.write(prediction)
    st.write('---')

if __name__=='__main__':
    main()