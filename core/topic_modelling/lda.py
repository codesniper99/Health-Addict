from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import math
from gensim import corpora


class LDA:
    def __init__(self, l):
        self.input_list = l
        self.outputs = []

    def find_no(self, res):
        num = 0
        for val in res:
            num = num + len(val)
        if num < 20:
            return 1
        return math.ceil(num / 20.0)

    def clean(self, doc):
        stop = set(stopwords.words('english'))
        exclude = set(string.punctuation)
        lemma = WordNetLemmatizer()
        stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
        punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
        normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
        return normalized

    def do_this_now(self, res):
        doc_clean = [self.clean(doc).split() for doc in res]
        numm = self.find_no(doc_clean)
        dictionary = corpora.Dictionary(doc_clean)
        doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
        Lda = gensim.models.ldamodel.LdaModel
        ldamodel = Lda(doc_term_matrix, num_topics=numm, id2word=dictionary, passes=50)
        top_words = ldamodel.show_topics(num_topics=numm, num_words=1, formatted=False)
        final_res = {}
        for x in top_words:
            temp = x[1]
            for y in temp:
                final_res[y[0]] = max(y[1], 0.0)
        return final_res

    def generate_tags(self):
        print('Generating Tags ...')
        pp = self.do_this_now(self.input_list)
        qq = {}
        for k, v in pp.items():
            qq[v] = k
        res = []
        for k, v in sorted(qq.items()):
            res.append(v)
        p = res[::-1]
        return p
