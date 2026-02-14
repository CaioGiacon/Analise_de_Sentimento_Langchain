import os
import pandas as pd
import csv

data = pd.read_csv(r'tratamento_de_dados\planilhas\reviews_usuarios.csv', quoting=csv.QUOTE_NONE, sep=',') # retirando a proteção das aspas
users_reviews = pd.DataFrame(data)

users_reviews['"id'] = users_reviews['"id'].str.replace('"', '') # tirando " de todos os campos da coluna "id
users_reviews['comentario"'] = users_reviews['comentario"'].str.replace('"', '') # tirando " de todos os campos da coluna comentario"

users_reviews = users_reviews.rename(columns={'"id' : 'id', 'comentario"' : 'comentario'}) # renomeando as colunas
path_archive = os.path.join('tratamento_de_dados', 'planilhas', 'reviews_usuarios_clean.csv')
os.makedirs(os.path.dirname(path_archive), exist_ok=True)
users_reviews.to_csv(path_archive, index=False)