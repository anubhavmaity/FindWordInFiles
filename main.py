import sys
import nltk
import glob
from nltk.tokenize import RegexpTokenizer
from nltk import PorterStemmer

def combine_indexes(words_list_stemmed, files_list):
    index, freq_word = create_inverse_index(files_list)

    sum_freq = 0
    index_list = []
    print words_list_stemmed
    for term in words_list_stemmed:
        if term in index.keys():
            print "Term is " + str(term)
            print "Index term "+ str(index[term]) 
            index_list.append(index[term])        
            sum_freq = sum_freq + freq_word[term]
                
    print "Index list " + str(index_list)    
    

    
    if sum_freq:
        index_result = list(set.intersection(*index_list))
        print "Index result is " + str(index_result)
        return index_result, sum_freq
    else:
        return ["No results found"], 0


def parse_input(word):
    word  =  word.strip()
    if ',' in word:
        words_list = word.split(',')
    elif ' ' in word:
        words_list = word.split(' ')
    elif ';' in word:
        words_list = word.split(';')
    elif ':' in word:
        words_list = word.split(':')
    else:
        words_list = [word]

    return words_list

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
        index[word] = set(index[word])

    return index, freq_word

def search(term, files_list):
    words_list = parse_input(term)
    print "WOrds list is " + str(words_list)
    words_list_stemmed = [stemming(word.strip()) for word in words_list]
    index_result, sum_freq = combine_indexes(words_list_stemmed, files_list)    
    return index_result, sum_freq



if __name__ == '__main__':
    files_list = ['adventur.txt', 'apples.txt', 'hVDacrN0.html']
    search('html', files_list)