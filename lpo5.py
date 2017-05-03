import os.path as os
import re
import pymorphy2
import gram
from random import randint

string = "Лучше приходи всегда в один и тот же час,  - попросил Лис."
string1 = "Сражение выигрывает тот, кто твердо решил его выиграть! "
string2 = "Солнце ушло, однако, как сказала Маша, на улице жарко, как в полдень"
string3 = "Рыбак рыбака видит издалека"


# Функция разбиения строки на слова
def get_tokens(input):
    return re.sub('[ .,?:;\'\"!()\[\]\n0123456789]+', ' ', input).strip().split(' ')

# Функция, вычленяющая разделители из строки
def get_seps(input):
    return re.split('\w+', input)


# Парсер словаря синонимов
def syn_parser(nf_and_word):
    file = open(os.abspath('synmaster.txt'), 'r').readlines()

    # Словарь для найденных синонимов (ключ=синоним, значение=слово)
    d_synonym = {}

    for key in nf_and_word.keys():
        if len(nf_and_word[key]) > 1:

            for line in file:
                # Разбиваем строку по разделителю '|'
                lines = str(line).split('|')
                # Ищем совпадения в строке с текущим словом
                if key in lines:
                    # Совпадение есть, выбираем синоним
                    i = lines.index(key)
                    syn_i = randint(0, len(lines)-1)

                    while syn_i == i:
                        syn_i = randint(0, len(lines)-1)

                    synonym = lines[syn_i].strip()
                    word = nf_and_word[key]
                    d_synonym[synonym] = word
                    break

    return d_synonym


# Функция, проводящая частотный анализ
def synonymizer(input):
    # Раздаление строки на слова и разделители
    words = get_tokens(input)
    seps = get_seps(input)

    # Морфологический анализ слов
    morph = pymorphy2.MorphAnalyzer()
    morphs_of_words = [morph.parse(el)[0] for el in words]
    # Отбор нужных слов
    for_synonymize = [morphs_of_words[i] for i in range(len(morphs_of_words))
                            if morphs_of_words[i].tag.POS in gram.pos_for_synonim and not 'Name' in morphs_of_words[i].tag]

    # Переход к нормальной форме
    nf_and_word = {}
    nf_set = set()
    for el in for_synonymize:
        nf = el.normal_form
        if nf in nf_set:
            lst = nf_and_word[nf]
            lst.append(el)
            nf_and_word[nf] = lst
        else:
            nf_set.add(nf)
            nf_and_word[nf] = [el]

    # Парсинг словаря синонимов
    d_synonym = syn_parser(nf_and_word)

    print(d_synonym.keys())



    return for_synonymize

print(synonymizer(string3))
