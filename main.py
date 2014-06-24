import sys
import nltk
import glob
from nltk.tokenize import RegexpTokenizer

def main():
    #creating a dictionary of words
    index = dict()

    #creating frequency of the words
    freq_word = dict() 
    
    #reading multiple files and tokenizing the contents of the files
    for f in glob.glob('*.txt'):
        file_content = open(f).read()
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(file_content)
        for word in words:
            #keeping all the words in lower case
            word = word.lower()
            if word not in index.keys():
                index[word] = [f]
            else:
                index[word].append(f)

    for word in index.keys():
        freq_word[word] = len(index[word])
        index[word] = list(set(index[word]))

    print index
    print freq_word




if __name__ == '__main__':
    main()