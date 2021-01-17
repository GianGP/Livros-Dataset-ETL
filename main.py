import pandas as pd
import copy
from utils import join_dfs, group_and_sort

#==============================Importação dos csv=====================================
autores = pd.read_csv('./datasets/authors.csv')
categorias = pd.read_csv('./datasets/categories.csv')
formatos = pd.read_csv('./datasets/formats.csv')
ds = pd.read_csv('./datasets/dataset.csv')

aux = {'authors': autores,
       'categories': categorias,
       'format': formatos}


# Cria-se uma cópia da dataset e une as informações das tabelas auxiliares a ela
df = copy.deepcopy(ds)
for aux_id_name, aux_df in aux.items():
    join_dfs(aux_id_name, aux_df, df)


#==================================Questões==========================================

#========================Transformações========================
# Transformações Questão 2
df.insert(2, 'author_quantity', 0)
df['author_quantity'] = df.apply(lambda row: len(row['authors']), axis=1)

# Transformações Questão 3
_, ranked_authors = group_and_sort('authors', autores, df)
ranked_authors = ranked_authors.head()

# Transformações Questão 4 e Questão 5
total_category, ranked_category = group_and_sort('categories', categorias, df)
ranked_category = ranked_category.head()

# Transformações Questão 6:
_ = df[['format_name', 'title']].groupby('format_name', as_index=False).count().sort_values('title', ascending=False)
most_used_format, quantity_format = _.head(1).iloc[0]

# Transformações Questão 7:
ranked_bestseller = df[['title', 'bestsellers-rank']].sort_values('bestsellers-rank').head(10)

# Transformações Questão 8:
ranked_rating = df[['title', 'rating-avg']].sort_values('rating-avg', ascending=False).head(10)

# Transformações Questão 9:
best_ratings = df[df['rating-avg'] > 3.5].title.count()

# Transformações Questão 10:
books_new_decade = df[df['publication-date'] > '2020-01-01'].title.count()


#========================Soluções========================
# Questão 1:
print('>> Questão 1:')
print('Há {} livros no dataset'.format(df.title.count()))

# Questão 2:
print('\n>> Questão 2:')
print('Há {} livros com apenas 1 autor'.format(df[df['author_quantity'] == 1].title.count()))

# Questão 3:
print('\n>> Questão 3:')
print('Top 5 autores com maiores quantidades de livros:\n')
for ix, row in enumerate(ranked_authors.values):
    print('{}° autor: "{}" com {} livros'.format(ix+1, row[0], row[1]))

# Questão 4:
#print('\n>> Questão 4:')
#print('Quantidade de livros por categoria:\n')
#for row in total_category.values:
#    print('Categoria: {:75} Livros: {}'.format(row[0], row[1]))

# Questão 5:
print('\n>> Questão 5:')
print('Top 5 categorias com maiores quantidades de livros:\n')
for ix, row in enumerate(ranked_category.values):
    print('{}° categoria: "{}" com {} livros'.format(ix+1, row[0], row[1]))
    
# Questão 6:
print('\n>> Questão 6:')
print('Formato mais utilizado: "{}" com {} utilizações'.format(most_used_format, quantity_format))

# Questão 7:
print('\n>> Questão 7:')
print('Livros mais bem posicionados relativos a bestseller:\n')
for row in ranked_bestseller.values:
    print('Livro: "{}" na posição {}'.format(row[0], int(row[1])))

# Questão 8:
print('\n>> Questão 8')
print('Livros mais bem posicionados relativos a média de nota:\n')
for row in ranked_rating.values:
    print('Livro: "{}" com nota {}'.format(row[0], row[1]))

# Questão 9:
print('\n>> Questão 9:')
print('{} livros possuem nota maior que 3,5'.format(best_ratings))

# Questão 10:
print('\n>> Questão 10:')
print('{} livros foram publicados após "01-01-2020"'.format(books_new_decade))



#========================Geração Arquivos Saída========================

# Arquivo dataset com junções
df.to_csv('./resolucao/dataset_unificado.csv', index=False)

# Arquivo questão 4
total_category.to_csv('./resolucao/questao_4.csv', index=False, sep=';')

# Arquivo questões 1 a 3 e 5 a 10
with open('./resolucao/solucoes.txt', 'w') as outfile:
    outfile.write('>> Questão 1:\n')
    outfile.write('Há {} livros no dataset\n\n'.format(df.title.count()))
    
    outfile.write('>> Questão 2:\n')
    outfile.write('Há {} livros com apenas 1 autor\n\n'.format(df[df['author_quantity'] == 1].title.count()))
    
    outfile.write('>> Questão 3:\n')
    outfile.write('Top 5 autores com maiores quantidades de livros:\n')
    for ix, row in enumerate(ranked_authors.values):
        outfile.write('{}° autor: "{}" com {} livros\n'.format(ix+1, row[0], row[1]))
    
    
    outfile.write('\n>> Questão 5:\n')
    outfile.write('Top 5 categorias com maiores quantidades de livros:\n')
    for ix, row in enumerate(ranked_category.values):
        outfile.write('{}° categoria: "{}" com {} livros\n'.format(ix+1, row[0], row[1]))
    
    outfile.write('\n>> Questão 6:\n')
    outfile.write('Formato mais utilizado: "{}" com {} utilizações\n\n'.format(most_used_format, quantity_format))
    
    outfile.write('>> Questão 7:\n')
    outfile.write('Livros mais bem posicionados relativos a bestseller:\n')
    for row in ranked_bestseller.values:
        outfile.write('Livro: "{}" na posição {}\n'.format(row[0], row[1]))
        
    outfile.write('\n>> Questão 8:\n')
    outfile.write('Livros mais bem posicionados relativos à média de nota:\n')
    for row in ranked_rating.values:
        outfile.write('Livro: "{}" com nota {}\n'.format(row[0], row[1]))
    
    
    outfile.write('\n>> Questão 9:\n')
    outfile.write('{} livros possuem nota maior que 3,5\n\n'.format(best_ratings))
    
    outfile.write('>> Questão 10:\n')
    outfile.write('{} livros foram publicados após "01-01-2020"'.format(books_new_decade))


