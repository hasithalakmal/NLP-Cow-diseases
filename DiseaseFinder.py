import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from QueryExecuter import QueryExecuter
from difflib import SequenceMatcher
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
import re

#training data set
train = [
    ('It has fever', 'pos'),
    ("It doesn't have fever", 'neg'),
    ('It is suffering from headache', 'pos'),
    ('It is not suffering from headache', 'neg'),
    ("He has cought cold", 'pos'),
    ("He hasn't cought cold", 'neg'),
    ('It does not have fever', 'neg'),
    ("He is in pain", 'pos'),
    ('It feels bad', 'pos'),
    ('He is lethargic', 'pos'),
    ('He seems to be lethargic', 'pos'),
    ('It lacks appetite', 'pos'),
    ('It has got fever', 'pos'),
    ("It hasn't got fever", 'neg'),
    ("no it hasn't got fever", 'neg'),
    ("no it hasn't got fever", 'neg'),
    ("no it doesn't have fever", 'neg'),
    ("no it doesn't have fever", 'neg'),
    ('yes it has fever', 'pos'),
    ('yes it is suffering from headache', 'pos'),
    ("no but has fever", 'pos'),
    ("no but it is suffering from headache", 'pos'),
    ("but it is suffering from headache", 'pos'),
    ("but it has fever", 'pos'),
    ('no', 'neg'),
    ('it is in pain', 'pos'),
    ('it is not in pain', 'neg'),
    ('there is lack of mobility', 'pos'),
    ("there isn't lack of mobility", 'neg'),
    ('there is not lack of mobility', 'neg')

]


class DiseaseFinder:

    important_operators = set(('of', 'in', 'to', 'due'))
    stop_words = set(stopwords.words()) - important_operators
    queryExecuter = None
    current_symptom = ""
    is_hit = False
    identified_disease = ""
    trainer = None
    sdd = {}
    symp_list = []
    dd = {}

    def __init__(self, age, type):
        self.queryExecuter = QueryExecuter()
        self.symp_list = self.queryExecuter.find_symptoms(age, type)
        self.sdd = self.queryExecuter.get_symp_disease_list()
        self.dd = self.queryExecuter.get_disease_frequency_list()
        self.trainer = NaiveBayesClassifier(train)

    def preprocess_user_input(self, user_input):
        positive_user_response = ""
        negative_user_response = ""

        tokenized_sentences = sent_tokenize(user_input.lower())
        is_current_symp_positive = False
        is_current_symp_negative = False

        iterator = 0

        for sentence in tokenized_sentences:

            #classify the given sentence is positive or negative
            sentence_state = self.trainer.classify(sentence)

            if iterator == 0:
                if self.findWholeWord('no')(sentence):
                    sentence_state = 'neg'
            iterator = (iterator + 1)

            if sentence_state == 'pos':
                tokenized_words = nltk.word_tokenize(sentence)
                tagged_words = nltk.pos_tag(tokenized_words)
                for w in tagged_words:
                    # and (w[0] != "n't" and w[0] != "not")) and (w[1] == 'DT' and w[0] != "no"
                    # if (w[0] != "n't" and w[0] != "not" and w[0] != "no" and (w[0] not in stop_words)):
                    if w[0] == "yes":
                        is_current_symp_positive = True

                    if w[0] not in self.stop_words:
                        positive_user_response += w[0] + " "


            elif sentence_state == 'neg':
                tokenized_words = nltk.word_tokenize(sentence)
                tagged_words = nltk.pos_tag(tokenized_words)

                for w in tagged_words:

                    if w[0] == "no":
                        is_current_symp_negative = True

                    if w[0] not in self.stop_words:
                        negative_user_response += w[0] + " "

        if is_current_symp_positive:
            positive_user_response += self.current_symptom + " "

        if is_current_symp_negative:
            negative_user_response += self.current_symptom + " "

        return positive_user_response,negative_user_response

    def find_disease(self, hit_symp):

        matching_diseases = self.sdd[hit_symp]
        for i in range(len(matching_diseases)):
            disease = matching_diseases[i]
            self.dd[disease][1] += 1
            self.dd[disease][2] = self.dd[disease][1] / self.dd[disease][0]

            if self.dd[disease][2] == 1:
                self.identified_disease = disease
                return True

        return False

    def make_question(self):

        # pop the last symptom from the list
        try:
            self.current_symptom = self.symp_list[(len(self.symp_list) - 1)]
            # make the question
            reply = "Does it has these symptoms? {} ?".format(self.current_symptom)

            return True, reply

        except IndexError:
            return False, "Sorry no entries found for this information"

    def find_hit_diseases(self,user_input):

        is_hit_current_symp = False

        if len(self.symp_list) != 0 and self.is_hit == False:
            # preprocess user response
            positive_user_response, negative_user_response = self.preprocess_user_input(user_input)

            # check for matching diseases with positive responses
            for hit_symp in self.symp_list[:]:

                # checking the misspelled words of user response
                is_simillar = self.check_for_misspelled_words(hit_symp,positive_user_response)

                if is_simillar:
                    self.is_hit = self.find_disease(hit_symp)
                    self.symp_list.remove(hit_symp)

                    if hit_symp == self.current_symptom:
                        is_hit_current_symp = True


            # check for matching diseases with negative responses
            for hit_symp in self.symp_list[:]:

                # checking the misspelled words of user response
                is_simillar = self.check_for_misspelled_words(hit_symp,negative_user_response)

                if is_simillar:
                    self.symp_list.remove(hit_symp)
                    if hit_symp == self.current_symptom:
                        is_hit_current_symp = True


            if self.is_hit == True:
                return 1, self.identified_disease

            if len(self.symp_list) == 0 and self.is_hit == False:
                conclude_diseases = []

                for key in self.dd:
                    if self.dd[key][2] > .50:
                        conclude_diseases.append(key+" ({} %) ".format(str(round(self.dd[key][2]*100,2))))

                if (len(conclude_diseases) != 0):
                    return 2, conclude_diseases

            if is_hit_current_symp == False:
                return 4, self.current_symptom

            return 3, ""

    def check_for_misspelled_words(self,hit_symp,user_response):

        for i in range(0, len(user_response) - len(hit_symp)):
            if SequenceMatcher(None,hit_symp,user_response[i:i+len(hit_symp)]).ratio() > .75:
                return True
        return False

    def remove_current_symp(self,hit_symp):
        if hit_symp in self.symp_list:
            self.symp_list.remove(hit_symp)
            if hit_symp == self.current_symptom:
                return True

        return False

    def findWholeWord(self,w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search