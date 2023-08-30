import pandas as pd
import numpy as np
import unicodedata


def sanitize_spaces(string):
    return ' '.join(string.split())


def convert_case(string, case='original'):
    #Deja el case requerido
    if case == 'original':
        return string
    elif case == 'upper' or case == 'uppercase' or case == 'mayus':
        string = string.upper()

    elif case =='lower' or case == 'lowercase' or case == 'minus':
        string = string.lower()

    elif case == 'capitalize' or case == 'capital':
        string = string.capitalize()

    else:
        ValueError("El argumento de 'case' = ['original', 'upper', 'lower', 'capitalize']")


def to_ascii(string, enie=False):
    if enie == True:
        string = string.replace("ñ", "#!#").replace("Ñ", "$!$")
        string = unicodedata.normalize('NFKD', string).encode('ascii','ignore').decode('ascii')
        string = string.replace("#!#", "ñ").replace("$!$", "Ñ")
    else:
        string = unicodedata.normalize('NFKD', string).encode('ascii','ignore').decode('ascii')
    return string


def sanitize_string(string, case='original', enie=False):
    string = sanitize_spaces(string)
    string = convert_case(string, case=case)
    string = to_ascii(string, enie=enie)
    return string

#Aliases
sanear_texto = sanitize_string



def metodo_pivote(df, ix_multicol, last_index_col):
    '''
    df: dataframe a pivotear (Al leerlo header=None)
    ix_multicol: lista con el index de las filas a transformar
    last_index_col: Cantidad de columnas antes de realizar el melt
    '''
    aux =  np.array([df.loc[ix, :].values for ix in ix_multicol]).T
    aux = [';'.join([str(x) for x in item]) for item in aux]
    df.columns = aux
    df = df.drop(ix_multicol, axis=0)

    df = pd.melt(df, id_vars=df.columns[:last_index_col], value_vars=df.columns[last_index_col:], var_name='aux_var', value_name='aux_value')

    for ix in range( len(ix_multicol) ):
        df.insert(loc=last_index_col+ix, column='var_' + str(ix), value=df['aux_var'].apply(lambda x: x.split(';')[ix]))
    df = df.drop(columns=['aux_var'])

    return df
