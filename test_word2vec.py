import gensim

model = gensim.models.KeyedVectors.load_word2vec_format('word2vec_vi_syllables_300dims.txt', binary=False)

print(model.similarity('hưởng', 'nhận'))