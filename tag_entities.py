# -*- coding: utf-8 -*-
import pickle
import glob
import os

def type_entity(sent, i):
    length_sent = len(sent)
    try:
        if (i+1) < length_sent:
            if sent[i+1][0].isdigit():
                return 2
            elif i+2 < length_sent:
                if (sent[i+1] == "N°") or (sent[i+1] == "Nº"):
                    return 1
                else:
                    return 0
            else:
                return 0
    except:
        print("Except type entity law decret:" , sent, sent[i])
        return 0

        
#Expediente Nº 8766
#Decretos Nº 180
#Resolución Nº 265
#Disposición Nº 27
def Create_ouput_tsv(file_path, file_tsv):
    list_entities = ["ley", "decreto", "expediente", "decreto", "resolución", "disposición", "artículo"]
    statinfo = os.stat(file_tsv)
    try: 
        with open(file_path, 'rb') as handle:
            try:
                sent_list = pickle.load(handle)
            except Exception as e: 
                print (e)
        for sent in sent_list:
            count = 0
            for i, word in enumerate(sent):
                count += 1
                # Sentences length should be less than 50
                if count > 50:
                    with open(file_tsv, "a") as text_file:
                        text_file.write("\n")
                    count = 0
                if word.lower() in list_entities:
                    type_e = type_entity(sent , i)
                    # No es una entidad:
                    if type_e == 0:
                        with open(file_tsv, "a") as text_file:
                            text_file.write(word + "\t" + "O" + "\n") 
                    # Entidad de tipo: "ley nº 1" 
                    elif type_e == 1:
                        with open(file_tsv, "a") as text_file:
                            text_file.write(word + "\t" + "B_ENTITY" + "\n")
                            text_file.write(sent[i+1] + "\t" + "I_ENTITY" + "\n")
                            text_file.write(sent[i+2] + "\t" + "I_ENTITY" + "\n")
                        del sent[i+1]
                        del sent[i+1]
                    # Entidad de tipo: "ley 1" 
                    elif type_e == 2:
                        with open(file_tsv, "a") as text_file:
                            text_file.write(word + "\t" + "B_ENTITY" + "\n")
                            text_file.write(sent[i+1] + "\t" + "I_ENTITY" + "\n")
                        del sent[i+1] 
                # No es una entidad:                
                else:
                    with open(file_tsv, "a") as text_file:
                            text_file.write(word + "\t" + "O" + "\n")
        with open(file_tsv, "a") as text_file:
            text_file.write("\n")
        return(1)
    except:
        return(0)
