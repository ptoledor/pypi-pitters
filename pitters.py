import pandas as pd
import numpy as np
import unicodedata


def standard_string(cadena, case='original', keep_enie=False):

    #Quita espacios excesivos    
    cadena = ' '.join(cadena.split())
    
    #Deja el case requerido
    if case == 'original':
        pass
    elif case == 'upper' or case == 'uppercase' or case == 'mayus':
        cadena = cadena.upper()

    elif case =='lower' or case == 'lowercase' or case == 'minus':
        cadena = cadena.lower()

    elif case == 'capitalize' or case == 'capital':
        cadena = cadena.capitalize()

    else:
        ValueError("El argumento de 'case' = ['original', 'upper', 'lower', 'capitalize']")


    #Quita acentos y non-ASCII characters
    if keep_enie == True:
        cadena = cadena.replace("ñ", "#!#").replace("Ñ", "$!$")
        cadena = unicodedata.normalize('NFKD', cadena).encode('ascii','ignore').decode('ascii')
        cadena = cadena.replace("#!#", "ñ").replace("$!$", "Ñ")
    else:
        cadena = unicodedata.normalize('NFKD', cadena).encode('ascii','ignore').decode('ascii')

    return cadena



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
