import nltk
import string
nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag
nltk.download('punkt')
from nltk.tokenize import word_tokenize 
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from collections import OrderedDict
import numpy as np


class extractKeywords():
    def __init__(self):
        self.d = 0.85 # damping coefficient, usually is .85
        self.min_diff = 1e-5 # convergence threshold
        self.steps = 10 # iteration steps
        self.node_weight = None # save keywords and its weight
        self.stopwords = set(stopwords.words('english'))
        self.vocab = OrderedDict()
        self.vocab_idx = 0
        
    def tokenize(self, line):
        punct = set(string.punctuation)
        punct.update(['’','”','“','—','%','‘'])
        token = word_tokenize(line)
        token = [''.join(c for c in s if not c.isdigit()) for s in token]
        token = [''.join(c for c in s if c not in punct) for s in token]
        return token
    
    def lemmatize(self, tokens):
        return [ WordNetLemmatizer().lemmatize(token) for token in tokens if token != '']
 
    def setStopword(self, stop_word):
        self.stopwords = self.stopwords.union(set(stop_word))
    
    def notStopword(self, token):
        if token in self.stopwords:
            return False
        return True
    
    def isCandidate(self, token, candidate_pos):
        tag = pos_tag([token])[0][1]
        if tag in candidate_pos:
            return True
        return False

    def sentence_segment(self, article, candidate_pos, lower):
        """Store those words only in cadidate_pos"""
        sentences = []
        for line in article:
            selected_words = []
            tokens = self.tokenize(line)
            tokens = self.lemmatize(tokens)
            for token in tokens:
                if self.isCandidate(token, candidate_pos) and self.notStopword(token):
                    if lower is True:
                        selected_words.append(token.lower())
                    else:
                        selected_words.append(token)
            sentences.append(selected_words)
        return sentences

    def build_vocab(self, sentences):
        for sentence in sentences:
            for word in sentence:
                if word not in self.vocab:
                    self.vocab[word] = self.vocab_idx
                    self.vocab_idx += 1

    def get_vocab(self):
        return self.vocab

    def get_token_pairs(self, window_size, sentences):
        """Build token_pairs from windows in sentences"""
        token_pairs = list()
        for sentence in sentences:
            for i, word in enumerate(sentence):
                for j in range(i+1, i+window_size):
                    if j >= len(sentence):
                        break
                    pair = (word, sentence[j])
                    if pair not in token_pairs:
                        token_pairs.append(pair)
        return token_pairs

    def symmetrize(self, a):
        return a + a.T - np.diag(a.diagonal())

    def get_matrix(self, token_pairs):
        """Get normalized matrix"""
        # Build matrix
        vocab_size = len(self.vocab)
        g = np.zeros((vocab_size, vocab_size), dtype='float')
        for word1, word2 in token_pairs:
            i, j = self.vocab[word1], self.vocab[word2]
            g[i][j] = 1

        # Get Symmeric matrix
        g = self.symmetrize(g)

        # Normalize matrix by column
        norm = np.sum(g, axis=0)
        g_norm = np.divide(g, norm, where=norm!=0) # this is ignore the 0 element in norm

        return g_norm


    def get_keywords(self, number=10):
        """Print top number keywords"""
        node_weight = OrderedDict(sorted(self.node_weight.items(), key=lambda t: t[1], reverse=True))
        result = []
        for i, (key, value) in enumerate(node_weight.items()):
            result.append([key, value])
            if i > number:
                break
        return result


    def analyze(self, articles,
                candidate_pos=['NN', 'NNS', 'NNP', 'NNPS', 'FW'],
                window_size=4, lower=False, stopwords=list()):
        """Main function to analyze text"""

        # Set stop words
        self.setStopword(stopwords)
        
        for article in articles:
            sentences = self.sentence_segment(article, candidate_pos, lower)
            self.build_vocab(sentences)

        # Build vocabulary
        vocab = self.get_vocab()

        # Get token_pairs from windows
        token_pairs = self.get_token_pairs(window_size, sentences)

        # Get normalized matrix
        g = self.get_matrix(token_pairs)

        # Initionlization for weight(pagerank value)
        pr = np.array([1] * len(vocab))

        # Iteration
        previous_pr = 0
        for epoch in range(self.steps):
            pr = (1-self.d) + self.d * np.dot(g, pr)
            if abs(previous_pr - sum(pr))  < self.min_diff:
                break
            else:
                previous_pr = sum(pr)

        # Get weight for each node
        node_weight = dict()
        for word, index in vocab.items():
            node_weight[word] = pr[index]

        self.node_weight = node_weight
