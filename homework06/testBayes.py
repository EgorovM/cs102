from bayes import NaiveBayesClassifier
from stop_words import get_stop_words

extra_chars = ['-', ',', '.', '!', '?', '(', ')', '[', ']', '\n']
stop_words = get_stop_words('en')

def feature_target_split(df):
    features, target = [[df[i][0] for i in range(len(df))],  [df[i][1] for i in range(len(df))]]

    return features, target

def normilize_texts(texts):
    texts = [text.lower() for text in texts]

    for ind, text in enumerate(texts):
        for char in extra_chars:
            text = text.replace(char, " ")

        texts[ind] = text

    return texts


train = [
    ('I love this sandwich.', 'positive'),
    ('This is an amazing place!', 'positive'),
    ('I feel very good about these beers.', 'positive'),
    ('This is my best work.', 'positive'),
    ("What an awesome view", 'positive'),
    ('I do not like this restaurant', 'never'),
    ('I am tired of this stuff.', 'never'),
    ("I can't deal with this", 'never'),
    ('He is my sworn enemy!', 'never'),
    ('My boss is horrible.', 'never')
]
test = [
    ('The beer was good.', 'positive'),
    ('I do not enjoy my job', 'never'),
    ("I ain't feeling dandy today.", 'never'),
    ("I feel amazing!", 'positive'),
    ('Gary is a friend of mine.', 'positive'),
    ("I can't believe I'm doing this.", 'never')
]

clf = NaiveBayesClassifier()
X_train, y_train = feature_target_split(train)
X_test, y_test   = feature_target_split(test)

X_test = normilize_texts(X_test)
clf.fit(normilize_texts(X_train), y_train)
