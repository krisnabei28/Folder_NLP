class ngramsNLP:
    def __init__(self, words = [], count = 1, probability = 0):
        self.words = words
        self.probability = float(probability)
        self.count = count

    def unigram_prob(self, dict_words, count_word):
        self.probability = self.count/ count_word
        
    def bigram_prob(self, dict_words):
        self.probability = self.count/ dict_words.get(self.words[0])
        
    def trigram_prob(self, dict_words, bigram_lists):
        for i in range(0, len(bigram_lists)):
            if [self.words[0], self.words[1]] == bigram_lists[i].words:
                self.probability = self.count/ bigram_lists[i].count
                break
            
    def print_ngrams(self):
        print(str(self.words) + " : " + str(self.probability))

def preprocess_sentence(sentences):
    data_clean = sentences.split(".")
    data_clean = list(filter(None, data_clean))
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    count_sentence = 0
    count_word = 0
    
    for sentence in data_clean:
        for ele in sentence:
            data_clean[count_sentence] = data_clean[count_sentence].replace("\n", " ")
            if ele == '-':
                data_clean[count_sentence] = data_clean[count_sentence].replace(ele, " ")
            elif ele in punc:
                data_clean[count_sentence] = data_clean[count_sentence].replace(ele, "")
        data_clean[count_sentence] = "<s> " + data_clean[count_sentence] + " </s>"
        data_clean[count_sentence] = data_clean[count_sentence].lower()
        data_clean[count_sentence] = data_clean[count_sentence].split(" ")
        data_clean[count_sentence] = list(filter(None, data_clean[count_sentence]))
        
        count_word += len(data_clean[count_sentence])
        count_sentence += 1    
    
    return data_clean, count_word

def make_ngram(n, string, dict_words):
    lists = []
    for sentence in string:
        for i in range(0, len(sentence) - n + 1):
            words = sentence[i:i + n]
            for j in range(0, len(words)):  # ganti jadi sentence
                if words[j] not in dict_words.keys():
                    dict_words.update({words[j] : 1})
                    break
                else:
                    dict_words[words[j]] = dict_words.get(words[j]) + 1
            
            words_exist = False
            
            for j in range(0, len(lists)):
                if words == lists[j].words:
                    lists[j].count += 1 
                    words_exist = True
                    break    
            if not words_exist:
                lists.append(ngramsNLP(words))
    return lists

def calculate_prob(data, dict_words, lists, count_word, mode):
    if mode == 3:
        bigram_lists = make_ngram(2, data, dict_words)
        calculate_prob(data, dict_words, bigram_lists, count_word, 2)
        
    for ngram in lists:
        if mode == 1:
            ngram.unigram_prob(dict_words, count_word)
        elif mode == 2:
            ngram.bigram_prob(dict_words)
        elif mode == 3:
            ngram.trigram_prob(dict_words, bigram_lists)

def find_prob(n, sentence, lists):
    words = sentence.split(" ")
    probability = float(1.00)
    ngram_words = []
    for i in range(0, len(words) - n + 1):
        ngram_words.append(words[i:i + n])
    
    for i in range(0, len(ngram_words)):
        ngram_exist = False
        for j in range(0, len(lists)):
            if ngram_words[i] == lists[j].words:
                ngram_exist = True
                probability *= lists[j].probability
                break
        if not ngram_exist:
            probability = 0
            break
    return probability

def output(lists):
    for ngram in lists:
        ngram.print_ngrams()

def main():
    f = open("D:/Materi_Kuliah/Semester 6/Code/dataSet.txt", "r")
    input_text = f.read()
    data, count_word = preprocess_sentence(input_text)
    
    while True:    
        print("Menu :")
        print("1. Unigram")
        print("2. Bigram")
        print("3. Trigram")
        print("0. Exit")
        x = input("Choice : ")
        x = int(x)
        
        if x == 0:
            break
        elif x >= 1 and x<=3:
            dict_words = {}
            list_ngrams = make_ngram(x, data, dict_words)
            calculate_prob(data, dict_words, list_ngrams, count_word, x)
            
            output(list_ngrams)
            
            start_sentence = False
            end_sentence = False
            searchWord = input("Cari Kata & probabilitasnya : ")
            if start_sentence:
                searchWord = "<s> " + searchWord
            if end_sentence:
                searchWord = searchWord + " </s>"
            prob = find_prob(x, searchWord, list_ngrams)
            
            print("-> Kata yang dicari : " + searchWord)
            print("-> Probability kata : " + str(prob) + "\n")
            
        else:
            print("Input tidak tersedia !!")    
    
main()