import pandas as pd
import math

# Função para transformar em listas as strings que representam listas dentro do dataset
def clean_alt_list(list_):
    list_ = list_.replace(', ', '","')
    list_ = list_.replace('[', '["')
    list_ = list_.replace(']', '"]')
    return list_


# Função para cruzar os dados e gerar um dataset unificado
def join_dfs(df_main_id_column, df_aux, df_main):
    
    # Obtém nome da coluna de identificação e o nome da coluna de descrição
    # das tabelas auxiliares à dataset
    id_column = df_aux.columns[0]
    name_column = df_aux.columns[1]
    
    # Gera um dicionário a ser utilizado para unir as informações dos dfs
    dict_aux = df_aux.set_index(id_column)[name_column].to_dict()
    
    if name_column not in df_main.columns:   
        
        # Localiza a posição da coluna do dataset referente ao id da auxiliar
        # e cria uma nova coluna na posição seguinte
        ix = df_main.columns.get_loc(df_main_id_column) + 1
        df_main.insert(ix, name_column, '')
        
        # Se a coluna que referencia a tabela auxiliar é uma string que representa lista
        # ela será tratada para virar uma lista
        if df_main[df_main_id_column].dtype == 'object':
            df_main[df_main_id_column] = df_main[df_main_id_column].apply(clean_alt_list)
            df_main[df_main_id_column] = df_main[df_main_id_column].apply(eval)
    
    # Se a coluna que referencia a tabela auxiliar é uma lista, as descrições 
    # serão unidas em uma string e adicionadas a nova coluna
    if df_main[df_main_id_column].dtype == 'object':
        df_main[name_column] = ['; '.join([str(dict_aux[int(j)]) for j in i if j != '']) for i in df_main[df_main_id_column]]
    
    # Caso contrátio os valores serão inseridos diretamente
    else:
        df_main[name_column] = [(dict_aux[i] if not math.isnan(i) else '') for i in df_main[df_main_id_column]]


# Função para transformar as colunas com listas em colunas com valores únicos (1D)
def to_1D(series):
    return pd.Series([x for _list in series for x in _list])


# Função para agrupar os df e ordená-los a partir da sua contagem
def group_and_sort(id_name, df_aux, df_main):
    id_column = df_aux.columns[0]
    name_column = df_aux.columns[1]

    df_group = pd.DataFrame({id_column: to_1D(df_main[id_name]), 'contagem': 1})
    df_group[id_column] = pd.to_numeric(df_group[id_column])
    df_group = pd.merge(df_group, df_aux)[[name_column, 'contagem']]
    df_group = df_group.groupby(name_column, as_index=False).count()
    df_group = df_group.sort_values(name_column)
    
    df_sort = df_group.sort_values('contagem', ascending=False)
    return df_group, df_sort