import sys
import nltk
import glob
from nltk.tokenize import RegexpTokenizer
from nltk import PorterStemmer

def stemming(word):
    word = PorterStemmer().stem_word(word.lower())
    return word

def create_inverse_index(files_list):
    #creating a dictionary of words
    index = dict()

    #creating frequency of the words
    freq_word = dict() 
    
    #reading multiple files and tokenizing the contents of the files
    for f in files_list:
        file_content = open(f).read()
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(file_content)
        #creating inverted index data structure
        for word in words:
            #keeping all the words in lower case
            word = stemming(word)
            if word not in index.keys():
                index[word] = [f]
            else:
                index[word].append(f)

    for word in index.keys():
        freq_word[word] = len(index[word])
        index[word] = list(set(index[word]))

    return index, freq_word

def search(term, files_list):
    index, freq_word = create_inverse_index(files_list)
    term = stemming(term)
    if term in index.keys():
        print index[term], freq_word[term]
        return index[term], freq_word[term]
    else:
        return "No files found", 0




if __name__ == '__main__':
    files_list = ['adventur.txt', 'apples.txt', 'hVDacrN0.html']
    search('html', files_list)