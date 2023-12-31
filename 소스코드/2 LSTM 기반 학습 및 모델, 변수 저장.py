from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from string import punctuation
import tensorflow as tf
import pandas as pd
import numpy as np
import pickle


# GPU 사용 가능 여부 확인
physical_devices = tf.config.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
    print("GPU가 사용 가능합니다.")
else:
    print("GPU를 찾을 수 없습니다. CPU를 사용합니다.")

df = pd.read_csv('output.csv')
Text = []
# 헤드라인의 값들을 리스트로 저장
Text.extend(list(df.Text.values))
print('총 샘플의 개수 : {}'.format(len(Text)))

Text = [word for word in Text if word != "ㅋ"]
print('노이즈값 제거 후 샘플의 개수 : {}'.format(len(Text)))

tokenizer = Tokenizer()
tokenizer.fit_on_texts(Text)
vocab_size = len(tokenizer.word_index) + 1
print('단어 집합의 크기 : %d' % vocab_size)

sequences = list()

for sentence in Text:
    encoded = tokenizer.texts_to_sequences([sentence])[0]
    for i in range(1, len(encoded)):
        sequence = encoded[:i+1]
        sequences.append(sequence)

max_len = max(len(l) for l in sequences)
print('샘플의 최대 길이 : {}'.format(max_len))

sequences = pad_sequences(sequences, maxlen=max_len, padding='pre')
sequences = np.array(sequences)
X = sequences[:, :-1]
y = sequences[:, -1]
y = to_categorical(y, num_classes=vocab_size)

embedding_dim = 10
hidden_units = 128

model = Sequential()
model.add(Embedding(vocab_size, embedding_dim))
model.add(LSTM(hidden_units))
model.add(Dense(vocab_size, activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])

# 모델 학습
model.fit(X, y, epochs=1, verbose=2)

# 모델 저장
model.save('my_model.keras', overwrite=True)
print("모델 저장이 완료되었습니다.")

# max_len 저장
with open('max_len.pkl', 'wb') as f:
    pickle.dump(max_len, f)

# tokenizer 저장
with open('tokenizer.json', 'w', encoding='utf-8') as f:
    f.write(tokenizer.to_json())
