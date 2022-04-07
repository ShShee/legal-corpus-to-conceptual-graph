from pickle import TRUE
import gensim

model = gensim.models.KeyedVectors.load_word2vec_format('wiki.vi.model.bin', binary=True)

print(model.similarity('nộp', 'gửi'))