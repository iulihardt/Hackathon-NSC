"""
.py para pegar a base de treinamento e criar o modelo de machine learning.
FLUXO
Par de chave, FRASE , SENTIMENTO, remove da frase stop words, e pondera em relação a base de trenamento o sentimento classificada
para caca palavra

EQUIPE 2 HACKATHON NSC 2019

"""
import nltk
#from base_treinamento import * #BASE DE TREINAMENTO em SENTIMENTOS
from base_training2 import *  #BASE DE TREINAMENTO em CLASSE da NSC

basetreinamento #BASE DE TREINAMENTO sentimentos OU CLASSE NSC

stop_words_nltk = nltk.corpus.stopwords.words('portuguese') #NLTK stopwords

#Adicionar stop word manualmente
#pode ser validada olhando a funçao 7x "classificador.show_most_informative_features(5)"
add_stop_words = ["vou", "ser"]
for i in add_stop_words:
    stop_words_nltk.append(i)


#exemplo para limpeza de RADICAL e remoção de stopwords:
#problema, novamente e novo fica nov
def aplicastemer(texto):
    stemmer = nltk.stem.RSLPStemmer() # RSLPStemmer funciona para o portugues
    frasesteming = []
    for (palavras, emocao) in texto:
        comstemming =[str(stemmer.stem(p)) for p in palavras.split() if p not in stop_words_nltk]
        frasesteming.append((comstemming,emocao))
    return frasesteming


frases_com_stemming = aplicastemer(basetreinamento)


def bucasplavras(frase):
    todas_as_palavras = []
    for (palavras, emocao) in frase:
        todas_as_palavras.extend(palavras)
    return todas_as_palavras

palavras = bucasplavras(frases_com_stemming)


def buscafrequencia(palavras):
    palavras = nltk.FreqDist(palavras)
    return palavras

frequencia = buscafrequencia(palavras)

def busca_palavras_unicas(frequencia):
    freq=frequencia.keys()
    return freq

palavras_unicas = busca_palavras_unicas(frequencia)


def extratorpalavras(documento):
    doc = set(documento)
    caracteristicas = {}
    for palavras in palavras_unicas:
        caracteristicas['%s' % palavras ] = (palavras in doc)
    return caracteristicas

basecompleta = nltk.classify.apply_features(extratorpalavras, frases_com_stemming)

classificador = nltk.NaiveBayesClassifier.train(basecompleta)

classificador.labels()
#classificador.show_most_informative_features(5)

teste = "Buraco na rua na minha csa, odeio isso pode ajudar?"

"""
pega a frase a ser testada, splita por sepaços e PROBABILISTICAMENTE na base de treino SOMA as probabildiades do modelo,
aquele sentimento que tiver maior valor a frase é classificada com esse senetimento
"""

def testar_frase(teste):
    testestimming = []
    stemmer = nltk.stem.RSLPStemmer()
    for (palavras) in teste.split():
        comstem = [p for p in palavras.split()]
        #print(comstem) Cada palavra da frase
        testestimming.append(str(stemmer.stem(comstem[0])))

    novo = extratorpalavras(testestimming) #passa cada stimming no modelo de treinamento
    
    distribuicao = classificador.prob_classify(novo)
    print("----------------")
    print("--------------------------")
    print("-----------------------------------------")
    print("--------------------------------------------------------")
    print("---------------------------------------------------------------------")
    print("-----------------------------------------------------------------------------------")
    print("RESUTADO")
    print(classificador.classify(novo)) # resultado da classificação
    print(teste)
    for classe in distribuicao.samples():
        print("%s: %f" % (classe, distribuicao.prob(classe)))

    
    #print(classificador.classify(novo)) # resultado da classificação
    return classificador.classify(novo)



