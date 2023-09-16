from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import pickle


def sentence_generation(model, tokenizer, current_word, n):
    init_word = current_word
    sentence = ''

    for _ in range(n):
        encoded = tokenizer.texts_to_sequences([current_word])[0]
        encoded = pad_sequences([encoded], maxlen=max_len-1, padding='pre')

        result = model.predict(encoded, verbose=0)
        result = np.argmax(result, axis=1)

        for word, index in tokenizer.word_index.items():
            if index == result:
                break

        current_word = current_word + ' ' + word
        sentence = sentence + ' ' + word

    sentence = init_word + sentence
    return sentence


# max_len 로드
with open('max_len.pkl', 'rb') as f:
    max_len = pickle.load(f)

# tokenizer 로드
with open('tokenizer.json', 'r', encoding='utf-8') as f:
    tokenizer = tokenizer_from_json(f.read())

# 모델 로드
loaded_model = load_model('my_model.keras')

# 시작 단어와 생성할 단어 수 설정
seed_text = '코로나'
num_words_to_generate = 7

# 텍스트 생성
generated_text = sentence_generation(
    loaded_model, tokenizer, seed_text, num_words_to_generate)

print("="*100)
print(generated_text)
print("="*100)
