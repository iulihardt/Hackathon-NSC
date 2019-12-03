from nltk_word import * #Biblioteca nltk para ML word 
import csv #biblioteca csv para ler arquivos CSV
import spacy #bilbioteca Spacy para auxiliar a leitura de palavras

#Classe criada por nossa equipe para identificar a cidade com o DDD
from origin_to_phone import IdentifyOriginPhone 

# https://developers.facebook.com/docs/whatsapp/api/webhooks/inbound DOCUMENTAÇÃo API whatsapp
#https://leportella.com/pt-br/2017/11/30/brincando-de-nlp-com-spacy.html EXEMPLO uso da SPACY

base_csv = "C:\\Users\\Toccato.000\\Dropbox\\Toccato\\Pythons\\hackathon\\sample.csv"

nlp = spacy.load('pt') #carrega a lingua mae do spacy
spacy_stopwords = spacy.lang.pt.stop_words.STOP_WORDS #carrega stops words

#add stop word customizado:
#foi nescessario implementar novas palavras ao stopwords
customize_stop_words = ['a', "o", "?",'e',',','.','!','1',"2","3","4","5","6","7","8","9","10"
,"Há","há", "tá", "já","o","ir",'é',"?","ate","A","d"]
for w in customize_stop_words:
    nlp.vocab[w].is_stop = True

#
# Remover as stopswords da frase a ser testada 
#+++
def remove_stopwords(doc):
    raiz3 = []
    for token in doc:
        if not token.is_stop:
           raiz3.append(token.lemma_)
    return raiz3

#open .csv files
uniquewords = open('uniquewords.csv', 'w', newline='')# as csv_file:
frases = open('frases.csv', 'w', newline='')# as csv_file:
pessoas = open('pessoas.csv', 'w', newline='')# as csv_file:
entidades = open('entidades.csv', 'w', newline='')# as csv_file:

#
# Funcao II 
# Transforma o sample.csv em 4 arquivos:
# uniquewords.csv plavras splitadas por espaço com a identificação id_sms
# frases.csv frase completa lincada com id_sms, telefone e classificação da palavra
# pessoas.csv Telefone da pessoa e cidade em relação ao DDD do celular
# entidades.csv a biblioteca nltk possui a classe .ents que separa nomes proprios em uma outra lista lincada com id_sms
#
def create_csv(dic_mensage,frases,uniquewords,pessoas,text_o):
    doc = dic_mensage['body'] #TEXTO DO Whtasapp
    frases.write(dic_mensage['id_sms']) #id do whatsapp 
    frases.write(";")
    frases.write(dic_mensage["telefone"])
    frases.write(";")
    frases.write(doc.text)
    frases.write(";")
    frases.write(testar_frase(row["text"])) #testar frase
    frases.write(";")
    frases.write(dic_mensage["time_stamp"])
    frases.write('\n')

    pessoas.write(dic_mensage["telefone"])
    pessoas.write(";")
    pessoas.write(str(IdentifyOriginPhone(dic_mensage["telefone"])).split("/")[0]) #por telefone classifica o DDD
    pessoas.write('\n')

    for palavra in remove_stopwords(doc):
        uniquewords.write(dic_mensage["id_sms"])
        uniquewords.write(";")
        uniquewords.write(palavra)
        uniquewords.write(";")
        uniquewords.write('\n')
    
    for entidade in (doc.ents):
        entidades.write(dic_mensage["id_sms"])
        entidades.write(";")
        entidades.write(entidade.text)
        entidades.write(";")
        entidades.write('\n')
    

#
# Main faz tudo:
#
# Abre o arquivo sample.csv - exemplo de base de whatsapp para processamento, existe uma parte REAL
# e uma parte criada pela equipe, com a inteção de aumentar o volume de frases que viriam do whatsapp.
with open(base_csv) as base:
    csv_read = csv.DictReader(base, delimiter=',')
    for row in csv_read:
        texto = row["text"]
        dic_mensage = {        
            "body"        : nlp(row["text"]),
            "telefone"    : row["from"],
            "id_sms"      : row["id"],
            "time_stamp"  : row["timestamp"],
            "xtype_obj"   : row['type'],

        }
        create_csv(dic_mensage,frases,uniquewords,pessoas,texto) #Fucao II


#teste = 'Alguem poderia me ajudar tem buraco aqui na nossa rua como pode fazer?'
#print(testar_frase(teste), "SENTIMENTO DO TESTE")
