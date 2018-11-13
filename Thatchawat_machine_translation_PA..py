import spacy
import collections

def process_dict_and_write(word_dict, output_file_name):
    '''
    Write dictionary file to tsv
    '''
    word_tran_list = []
    for word in word_dict:
        temp = []
        temp.append(word)
        for trans in word_dict[word].most_common(3):
            temp.append(trans[0])
            temp.append(trans[1])
        word_tran_list.append(temp)
    for word in word_tran_list:
        while len(word) != 7:
            word.append('x')
    writing_file = open(output_file_name, 'w')
    for word in word_tran_list:
        writing_file.write(
            '{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(word[0], word[1], word[2], word[3], word[4], word[5], word[6]))
    writing_file.close()

def learn_dictionary(word_list_file_name, en_data_file_name,
        foreign_data_file_name, output_file_name):
    """Learn a dictionary from a given parallel corpus
    
    >>> learn_dictionary('word_list.txt', 'europarl-v7.de-en.en', 'europarl-v7.de-en.de', 'de_to_en_dict.tsv')
    """
    en_data = open(en_data_file_name).readlines()
    fr_data = open(foreign_data_file_name).readlines()
    data = open(word_list_file_name)
    test_list = []
    for line in data:
        test_list.append(line.strip('\n'))
    word_tran_dict = {}
    for w in test_list:
        word_tran_dict[w] = collections.Counter()
    en_nlp = spacy.load('en', disable=['parser', 'ner', 'tagger'])
    fr_nlp = spacy.load('fr', disable=['parser', 'ner', 'tagger'])
    for eng_sen, fr_sen in zip(en_data, fr_data):
        en_token = en_nlp(eng_sen)
        fr_token = fr_nlp(fr_sen)
        for en_w in en_token:
            for fr_w in fr_token:
                if str(fr_w) in word_tran_dict:
                    word_tran_dict[str(fr_w)][str(en_w)] += 1
    process_dict_and_write(word_tran_dict, output_file_name)

def tag_data_file(model_file_name, data_file_name, output_file_name):
    """Tag data with POS tag

    Refer to https://attapol.github.io/programming/code/use_spacy.py
    for basic use of spacy
    >>> tag_data_file('en', 'europarl-v7.de-en.en', 'europarl-v7.de-en.tagged.en')
    """
    # disable sentence tree parser and name detector to improve speed
    processor = spacy.load(model_file_name, disable=['parser', 'ner'])

    file = open(data_file_name)
    output = open(output_file_name, 'w')
    for line in file:
        processed_line = processor(line.strip())
        for token in processed_line:
            output.write('{}/{} '.format(str(token), token.pos_))
        output.write('\n')
    output.close()


def learn_dictionary_pos(word_list_file_name, en_tagged_data_file_name, 
        foreign_tagged_data_file_name, output_file_name):
    """Learn a dictionary from a given tagged parallel corpus

    >>> learn_dictionary('word_list.txt', 'europarl-v7.de-en-tagged.en',
            'europarl-v7.de-en-tagged.de', 'de_to_en_dictv2.tsv')
    """
    word_list = open(word_list_file_name)
    eng_tag = open(en_tagged_data_file_name)
    fr_tag = open(foreign_tagged_data_file_name)
    word_test_list = []
    for line in word_list:
        word_test_list.append(line.strip('\n'))
    word_tran_dict = {}
    for w in word_test_list:
        word_tran_dict[w] = collections.Counter()
    for eng_sen, fr_sen in zip(eng_tag, fr_tag):
        eng_sen_list = eng_sen.split(' ')
        fr_sen_list = fr_sen.split(' ')
        for fr_w in fr_sen_list:
            fr_w_list = fr_w.split('/')
            if fr_w_list[0] in word_test_list:
                for eng_w in eng_sen_list:
                    eng_w_list = eng_w.split('/')
                    if eng_w_list[-1] == fr_w_list[-1]:
                        word_tran_dict[fr_w_list[0]][eng_w_list[0]] += 1
    process_dict_and_write(word_tran_dict,output_file_name)

def process_dict_file_to_dict(dictionary_file_name):
    '''
    Read dictionary's file
    file >>> dictionary
    '''
    dict = open(dictionary_file_name)

    final_dict = {}
    for line in dict:
        words = line.split('\t')
        final_dict[words[0]] = words[1]
    return final_dict

def translate_file(model, foreign_to_en_dictionary_file_name, foreign_sentence_file_name, output_file_name):
    """Translate sentences using the provided dictionary

    >>> translate_file('de_to_en_dict.tsv', 'de_sentences.txt')
    I am a Berliner .
    The parliament calls good men .
    """
    processor = spacy.load(model, disable=['parser', 'ner', 'tagger'])
    data = open(foreign_sentence_file_name)
    translated_list = []
    final_dict = process_dict_file_to_dict(foreign_to_en_dictionary_file_name)
    for line in data:
        tokens = processor(line.strip())
        empty_list = []
        for token in tokens:
            if str(token) in final_dict:
                empty_list.append(final_dict[str(token)])
            else:
                empty_list.append('NULL')
        translated_list.append(empty_list)

    final_file = open(output_file_name, 'w')
    for sentence in translated_list:
        final_file.write(' '.join(sentence)+'\n')
    final_file.close()


def translate_interactive(model, foreign_to_en_dictionary_file_name):
    """Translate interactively

    The user can type in a sentence to translate.
    The program exits when the user enters an empty string. 

    >>> translate_interactive('de_to_en_dict.tsv'):
    Enter a sentence to translate: 
    """
    processor = spacy.load(model, disable=['parser', 'ner', 'tagger'])
    final_dict = process_dict_file_to_dict(foreign_to_en_dictionary_file_name)
    processed_input = processor(input('Say whatever'))
    temp = []
    for data in processed_input:
        if str(data) in final_dict:
            temp.append(final_dict[str(data)])
        else:
            temp.append('NULL')
    print(' '.join(temp))

if __name__ == '__main__':
    # You should keep changing this part to test/run your programs
    learn_dictionary('word_list', 'europarl-v7.fr-en.en.short',
            'europarl-v7.fr-en.fr.short', 'fr_to_en_dict.tsv')
    tag_data_file('en', 'europarl-v7.fr-en.en.short', 'fr-en.tagged.en')
    tag_data_file('fr', 'europarl-v7.fr-en.fr.short', 'fr-en.tagged.fr')
    learn_dictionary_pos('word_list', 'fr-en.tagged.en',
                         'fr-en.tagged.fr', 'fr_to_en_dict_pos.tsv')
    translate_file('fr', 'fr_to_en_dict_pos.tsv', 'europarl-v7.fr-en.fr.short','translated_eng')
    translate_interactive('fr', 'fr_to_en_dict_pos.tsv')