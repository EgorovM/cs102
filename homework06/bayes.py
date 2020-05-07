import pymorphy2
import math

class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha
        self.morph = pymorphy2.MorphAnalyzer()
        self.dictionary = {}
        self.labels = ["good", "maybe", "never"]
        self.labels_count = dict.fromkeys(self.labels, 0)
        self.size = 0
        self.word_probability = {}

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """

        for ind, text in enumerate(X):
            for word in text.split():
                norm_form = self.morph.parse(word)[0].normal_form

                if not norm_form in self.dictionary:
                    self.dictionary[norm_form] = dict.fromkeys(self.labels, 0)
                    self.size += 1

                if not norm_form in self.word_probability:
                    self.word_probability[norm_form] = dict.fromkeys(self.labels, 0)

                self.dictionary[norm_form][y[ind]] += 1

            self.labels_count[y[ind]] += 1

        for word in self.dictionary:
            for label in self.labels_count.keys():
                nc  = sum([self.dictionary[w][label] for w in self.dictionary])
                nic = self.dictionary[word][label]
                self.word_probability[word][label] = (nic + self.alpha) / (nc + self.size * self.alpha)

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        results = []

        for ind, text in enumerate(X):
            probabilities = dict.fromkeys(self.labels, 0)

            for label in probabilities:
                prob = self.labels_count[label] / sum(self.labels_count.values())
                probabilities[label] = math.log(prob) if prob != 0 else -100000

            for word in text.split():
                norm_form = self.morph.parse(word)[0].normal_form

                for label in self.labels:
                    if norm_form in self.word_probability:
                        probabilities[label] += math.log(self.word_probability[norm_form][label])

            max_prob = max(probabilities.values())

            for label in probabilities:
                if probabilities[label] == max_prob:
                    results.append(label)
                    break

        return results

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        y_pred = self.predict(X_test)

        results = [1 if y_pred[i] == y_test[i] else 0 for i in range(len(y_test))]

        return sum(results) / len(results)
