import os.path as os
import re
import pymorphy2
import gram
from random import randint

string = "Купец купцу конкурент"
string1 = "Маша, Маша растеряша"
string2 = "Идти далеко - не значит идти долго!"
string3 = "Трусливый друг страшнее врага, ибо врага опасаешься, а на друга надеешься"

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
                    # Совпадение есть, выбираем синоним, если ни у одного нет пробела
                    space = [True for el in lines if el.isalpha()]
                    if True not in space:
                        break

                    i = lines.index(key)
                    syn_i = randint(0, len(lines)-1)

                    while syn_i == i or not lines[syn_i].isalpha():
                        syn_i = randint(0, len(lines)-1)
                        if not lines[syn_i].isalpha():
                            syn_i = randint(0, len(lines) - 1)

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

    # Слова в нижний регистр
    words = [el.lower() for el in words]

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

    h = morph.parse('агена')[0]
    h = h.inflect({'gent','sing'})

    # Вставка синонимов в исходную строку
    for key in d_synonym.keys():
        for el in d_synonym[key]:
            if el.word in words:
                i = words.index(el.word)
                if el.word != el.normal_form:
                    key_morph = morph.parse(key)[0]

                    if el.tag.POS == 'VERB':
                        words[i] = key_morph.inflect(
                            {el.tag.aspect, el.tag.tense, el.tag.number, el.tag.gender}).word

                    elif el.tag.POS == 'INFN':
                        words[i] = key_morph.inflect({el.tag.aspect, el.tag.transitivity}).word

                    elif el.tag.POS == 'ADJF' or el.tag.POS == 'ADJS':
                        words[i] = key_morph.inflect({el.tag.gender, el.tag.case, el.tag.number}).word

                    else:
                        words[i] = key_morph.inflect({el.tag.case, el.tag.number}).word
                else:
                    words[i] = key
                # Глаголу - aspect, mood, person, tense, transitivity

    return words

print(synonymizer(string4))
