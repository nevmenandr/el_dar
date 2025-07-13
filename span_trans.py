import pymorphy2
from transliterate import translit
from razdel import sentenize

def is_noun(word, morph):
    """Проверяет, является ли слово существительным."""
    parsed = morph.parse(word)[0]
    if 'NOUN' in parsed.tag:
        return parsed.normal_form

def transliterate_word(word, is_n, capitalize=False):
    """Транслитерирует слово в латиницу."""
    transliterated = translit(word, 'ru', reversed=True)
    if is_n:
        prefix = 'El' if capitalize else 'el'
        transliterated = f'{prefix} {transliterated}'
    return transliterated

def process_words(text, morph):
    """Обрабатывает слова."""
    words = text.split()
    processed_words = []

    for i, word in enumerate(words):
        if i == 0 and is_noun(word, morph):
            processed_words.append(transliterate_word(is_noun(word, morph), is_n=True, capitalize=True))
        elif is_noun(word, morph):
            processed_words.append(transliterate_word(is_noun(word, morph), is_n=True))
        else:
            processed_words.append(transliterate_word(word, is_n=False))
    return processed_words

def process_text(input_file, output_file):
    """Читает, обрабатывает и записывает текст."""
    morph = pymorphy2.MorphAnalyzer()
    
    processed_text = []

    with open(input_file, 'r', encoding='utf-8') as file:
        for line in file:
            processed_line = []
            for sent in sentenize(line):
                sentence_processed = process_words(sent.text, morph)
                sentence_processed = ' '.join(sentence_processed)
                if sentence_processed.endswith("!"):
                    sentence_processed = '¡' + sentence_processed
                if sentence_processed.endswith("?"):
                    sentence_processed = '¿' + sentence_processed
                processed_line.append(sentence_processed)
            processed_line = ' '.join(processed_line)
            
            processed_text.append(processed_line)
            

    with open(output_file, 'w', encoding='utf-8') as file:
        translated = '\n'.join(processed_text)
        translated = translated.replace("n'", 'ñ')
        file.write(translated)

# Имена файлов
input_file = '0006_ r_dar.txt'
output_file = 'el_dar.txt'

process_text(input_file, output_file)
