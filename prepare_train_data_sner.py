import tag_entities
import glob
import pickle

path_trainning = '/Users/karenhaag/Documents/tesis/data/tokenized_data/tokenized_data_training/'
output_data = '/Users/karenhaag/Documents/tesis/training.tsv'
count = 0
for filename in glob.glob('/Users/karenhaag/Documents/tesis/data/tokenized_data/tokenized_data_training/*.pickle'):
    if count < 1:
        count += 1
        tag_entities.Create_ouput_tsv(filename, output_data)
    else:
        break