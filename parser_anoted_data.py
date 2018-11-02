import xml.etree.ElementTree as ET
from nltk import sent_tokenize 
import pickle
import re
import glob
import os
from pathlib import Path
import csv
import codecs


def add_enter(output):
    with open(output, "a") as text_file:
        text_file.write("\n")
        
def add_entity_to_tsv(word, tag, output):
    with open(output, "a") as text_file:
        text_file.write(word + "\t" + tag + "\n")

def main():
    path_to_save = '/Users/karenhaag/Documents/tesis/stanford-ner-2018-02-27/train_links/test_anoted.tsv'
    data_path = '/Users/karenhaag/Documents/tesis/data/anoted_data/anotaciones_infoleg/'
    clasificacion= {'decisión': 'DECISION', 'ley': 'LEY', 'decreto': 'DECRETO', 'resolución': 'RESOLUCIÓN', 'artículo': 'ARTÍCULO', 'expediente': 'EXPEDIENTE', 'disposición': 'DISPOSICIÓN'} 
    for filename in glob.glob(data_path + '*.ann'):
        lines = open(filename).readlines()
        number = re.findall(r'\d+', filename)[0]
        with open(data_path + number + '.txt', 'r') as f:
            text = f.read()
        buff = 0
        for l in lines:
            begin = int(l.split()[2])
            end = int(l.split()[3])
            part_of_text = text[buff:begin]
            buff = end + 1
            entity = text[begin:end]
            

            count = 0
            for word in part_of_text.split():
                tag = "O"
                if word != "" and word != " ":
                    word = "".join(word.split())
                    count += 1
                    if count < 50:
                        add_entity_to_tsv(word, tag, path_to_save)
                    else:
                        add_enter(path_to_save)
                        add_entity_to_tsv(word, tag, path_to_save)
                        count = 0
            has_clasif = False
            for word in entity.split(" "):
                if word != "" and word != " ":
                    word = "".join(word.split())                    
                    if word.lower() in clasificacion:
                        has_clasif = True
                        class_entity = clasificacion[word.lower()]
            for word in entity.split(" "):
                if word != "" and word != " ":
                    word = "".join(word.split())
                    count += 1
                    if not has_clasif:
                        tag = "ENTITY"
                    else:
                        tag = class_entity
                    add_entity_to_tsv(word, tag, path_to_save)
        part_text = part_of_text[buff:len(part_of_text)-1]
        for word in part_text.split():
            tag = "O"
            if word != "" and word != " ":
                word = "".join(word.split())
                count += 1
                if count < 50:
                    add_entity_to_tsv(word, tag, path_to_save)
                else:
                    add_enter(path_to_save)
                    add_entity_to_tsv(word, tag, path_to_save)
                    count = 0
            
main()