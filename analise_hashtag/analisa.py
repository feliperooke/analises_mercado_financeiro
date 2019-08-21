#coding: utf-8
import nltk
import os
import json
import re
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt


# lista arquivos de capturados
def get_lista_arquivos_usuarios_capturados(dir_base = "."):
    
    dir_capturados = "{}/dados/capturados/".format(dir_base)
    return ["{}/{}".format(dirpath, arquivo[0]) for dirpath, _, arquivo in os.walk(dir_capturados) if arquivo != []]


# extrai conteudo de posts
def extrai_conteudo_posts(caminho):

    posts = []

    with open(caminho) as json_file:
        data = json.load(json_file)
        for post in data["GraphImages"]:
            try:
                posts.append(post["edge_media_to_caption"]["edges"][0]["node"]["text"])
            except:
                continue
            
    return posts


# extrai hashtags de frase
def extrai_hashtag_frase(frase):
    return re.findall(r"(#\w+)", frase)


# analiza cloudofwords
def gera_cloud_of_words(lista_de_palavras, new_stopwords={}):
    #convert list to string and generate
    unique_string=(" ").join(lista_de_palavras)
    wordcloud = WordCloud(width = 1000, 
                          height = 500,
                          stopwords=new_stopwords,
                          background_color='white',
                          max_words = 30, 
                          mode="RGB").generate(unique_string)
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("nuvem_de_palavras"+".png", bbox_inches='tight')
    plt.show()
    plt.close()

hashtags = []

caminhos = get_lista_arquivos_usuarios_capturados()
for caminho in caminhos:
    posts = extrai_conteudo_posts(caminho)
    for post in posts:
        hashtags = hashtags + extrai_hashtag_frase(post)

excluir = {"agripinocorleone", "mepoupe", "oprimorico", "youtube", "ahquefesta", "bulldog", "ad", "papodebolsa", "nathmeajuda"}
gera_cloud_of_words(hashtags, excluir)