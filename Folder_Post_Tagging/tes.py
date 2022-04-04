import pandas as pd
#reading dataset from tsv file
dataset = pd.read_table('Indonesian_Manually_Tagged_Corpus.tsv', header=None, names=['words','tags'])

#counting how much tags in dataset
counted = dataset['tags'].value_counts()

#most 10 frequent tags
print('10 most frequent tags:', counted.head(10), sep='\n')


### PROCESSING
from nltk import hmm

# Creating list of list Tuple
# low: List of Words
# sep: separator (in this case is dot)
def c_list_of_sentences(low, sep):
    sentence = []
    sentences = []
    for word in low:
        sentence.append(word)
        if word == sep:
            sentences.append(sentence)
            sentence = []
    return sentences

#variable for processing
list_of_words = dataset.to_records(index=False).tolist()
sep = ('.', 'Z')

#list of datatraining (format in tuple)
train_data = c_list_of_sentences(list_of_words, sep)

#train model with HMM algorithm
trainer=hmm.HiddenMarkovModelTrainer()

#creating pos tag model
tagger=trainer.train_supervised(train_data)
loadData = open("/home/krisnabei/Documents/Dokumen_Krisna/NLP/Post_Tagging_Code/dataSet.txt", "r")
inputData = loadData.read()
#tagging process
print(tagger.tag(inputData.split()))