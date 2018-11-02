import xml.etree.ElementTree as ET
from nltk import sent_tokenize 
import pickle
import re
import glob
import os
from pathlib import Path
import pandas as pd
import numpy as np
import csv
pd.options.display.float_format = '{:.10G}'.format

def add_entity_to_tsv(word, tag, output):
    with open(output, "a") as text_file:
        text_file.write(word + "\t" + tag + "\n")

def add_enter(output):
    with open(output, "a") as text_file:
        text_file.write("\n")

def generate_tsv(text, links, output):
    buff = 0
    reg = 0
    clasificacion = {'decisión': 'DECISION', 'instrucción': 'INSTRUCCION', 'decreto': 'DECRETO'} 

    regexp_ley = re.compile(r'ley nº \d+[.]?\d*[.,]?|ley n° \d+[.]?\d*[.,]?|ley \d+[.,]?\d*[.,]?')
    regexp_decreto = re.compile(r'decreto \d+[.]?\d*/\d+[.,]?|decreto n° \d+[.]?\d*/\d+[.,]?|decreto nº \d+[.]?\d*/\d+[.,]?|decreto nº \d+[.]?\d*[.,]?|decreto n° \d+[.]?\d*[.,]?')
    regexp_resolucion = re.compile(r'resolución nº \d+[.]?\d*/\d+[.,]?|resolución n° \d+[.]?\d*/\d+[.,]?|resolución n° \d+[.]?\d*[.,]?|resolución \d+[.]?\d*[.,]?|resolución \d+[.]?\d*/\d+[.,]?|resolución nº \d+[.,]?')
    regexp_articulo = re.compile(r'artículo nº \d+[.]?\d*[.,]?|artículo n° \d+[.]?\d*[.,]?|artículo \d+[.]?\d*[.,]?')
    regexp_expediente = re.compile(r'expediente \d+[.]?\d*/\d+[.,]?|expediente n° \d+[.]?\d*/\d+[.,]?|expediente nº \d+[.]?\d*/\d+[.,]?')
    regexp_disposicion = re.compile(r'disposición \d+[.]?\d*/\d+[.,]?|disposición n° \d+[.]?\d*/\d+[.,]?|disposición nº \d+[.]?\d*/\d+[.,]?|disposición nº \d+[.]?\d*[.,]?|disposición n° \d+[.]?\d*[.,]?')
     
    added = 0
    has_entity = False
    for link in links:
        begin = int(link["begin"])
        end = int(link["end"])
        entity = text[begin:end]
        if not (regexp_ley.search(entity.lower()) or regexp_expediente.search(entity.lower()) or regexp_disposicion.search(entity.lower()) or regexp_decreto.search(entity.lower()) or regexp_resolucion.search(entity.lower()) or regexp_articulo.search(entity.lower())) :
            has_entity = True
    if has_entity:             
        statinfo = os.stat(output)
        if statinfo.st_size < 7000000:
            for link in links:
                added = 1
                part_of_text = text[buff:begin]            
                begin = int(link["begin"])
                end = int(link["end"])
                entity = text[begin:end]
                count = 0    
                buff = end + 1
                for word in part_of_text.split():
                    tag = "O"
                    if word != "" and word != " ":
                        word = "".join(word.split())
                        count += 1
                        if count < 50:
                            add_entity_to_tsv(word, tag, output)
                        else:
                            add_enter(output)
                            add_entity_to_tsv(word, tag, output)
                            count = 0
                if not (regexp_ley.search(entity.lower()) or regexp_expediente.search(entity.lower()) or regexp_disposicion.search(entity.lower()) or regexp_decreto.search(entity.lower()) or regexp_resolucion.search(entity.lower()) or regexp_articulo.search(entity.lower())) :
                    
                    has_clasif = False
                    for word in entity.split(" "):
                        word = "".join(word.split())                    
                        if word.lower() in clasificacion:
                            has_clasif = True
                            class_entity = clasificacion[word.lower()]
                    for word in entity.split(" "):
                        word = "".join(word.split())
                        count += 1
                        if not has_clasif:
                            tag = "ENTITY"
                        else:
                            tag = class_entity
                        add_entity_to_tsv(word, tag, output)
                else:
                    tag = "O"
                    for i, word in enumerate(entity.split(" ")):
                        add_entity_to_tsv(word, tag, output)
    return(added) 
            
        

def get_links(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    count = 0
    links = []
    for t in root.findall('text'):
        sentence = t.text
    for link in root.iter('link'):
        links.append(link.attrib)
    return links, sentence

def parse_link(filename, path_to_save):
    count = 0
    links, text = get_links(filename)
    added = 0
    if links != []:
        #print(filename)
        added = generate_tsv(text, links, path_to_save)
        count = 1
    return count, added


def main():
    #file_xml = '/Users/karenhaag/Documents/tesis/data/train_xml/*.xml'
    #path_to_save = '/Users/karenhaag/Documents/tesis/stanford-ner-2018-02-27/train_links/train_links.tsv'
    file_xml = '/Users/karenhaag/Documents/tesis/data/test_xml/*.xml'    
    path_to_save = '/Users/karenhaag/Documents/tesis/stanford-ner-2018-02-27/train_links/test_links.tsv'
    result_model = '/Users/karenhaag/Documents/tesis/stanford-ner-2018-02-27/result_linked.tsv'    
    #path_to_save = '/Users/karenhaag/Documents/tesis/train_links.tsv'
    open(path_to_save, 'w').close()
    open(result_model, 'w').close()
    count_total_documentos = 0
    count = 0
    count_parsed = 0
    document = []
    for filename in glob.glob(file_xml):
        count_total_documentos += 1
        result, added = parse_link(filename, path_to_save)
        count_parsed += added
        if result == 1:
            document.append(filename)
        count += result
    df = pd.read_csv(path_to_save, sep='\t',quoting=csv.QUOTE_NONE, encoding='utf8',error_bad_lines=False)
    df = df.dropna()
    print(df.head())
    df.to_csv(path_to_save, sep='\t', index=False)
            
    print("total documentos con links: ", count)
    print(count_total_documentos)  
    print("Documentos parseados: ", count_parsed)
    print(document[0])
    my_file = 'documents_parsed.pickle'
    with open('/Users/karenhaag/Documents/tesis/'+ my_file, 'wb') as handle:
        pickle.dump(document, handle, protocol=pickle.HIGHEST_PROTOCOL) 

def parser_tsv_with_rgxp(input_data):
    import csv
    with open(input_data) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        count = 0
        for line in tsvreader:
            print (line)
            count += 1            
            if count > 3:
                break

main()