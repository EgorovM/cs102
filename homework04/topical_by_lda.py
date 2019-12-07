from normilize_text import normilize_texts, preparation_text

from normilize_text import normilize_texts
from gensim.models.ldamulticore import LdaModel
from gensim.corpora.dictionary import Dictionary


def get_lda_model_byDomains(domains):
    """ Создать LDA модель из заданных ссылок
    :param domains: имена сообществ VK
    """

    common_texts = normilize_texts(domains[0])

    for i in range(1, len(domains)):
        common_texts += normilize_texts(domains[i])

    common_dictionary = Dictionary(common_texts)
    common_corpus = [common_dictionary.doc2bow(text) for text in common_texts]
    lda = LdaModel(common_corpus, num_topics=len(domains))

    return lda


def predict_topic(lda, text):
    """ Предсказать тему текста на основе LDA

    :param lda: заранее подготовленная LdaModel
    :param text: текст для предсказывания

    :return vector: вектор вероятностных исходов
    """

    predict_texts = [preparation_text(text)]
    predict_dictionary = Dictionary(predict_texts)
    predict_corpus = [predict_dictionary.doc2bow(text) for text in predict_texts]
    unseen_doc = predict_corpus[0]

    vector = lda[unseen_doc]

    return vector
