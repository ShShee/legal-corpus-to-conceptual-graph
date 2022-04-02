from pyvi import ViTokenizer, ViPosTagger

ViTokenizer.tokenize("Trường đại học bách khoa hà nội")

print(ViPosTagger.postagging(ViTokenizer.tokenize("Quy định tham gia bảo hiểm thất nghiệp cho người lao động")))

from pyvi import ViUtils
print(ViUtils.remove_accents(u"Trường đại học bách khoa hà nội"))

from pyvi import ViUtils
print(ViUtils.add_accents(u'truong dai hoc bach khoa ha noi'))