# $Key Terms Extraction
# Stage 4/4
import logging
import nltk
from lxml import etree
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from string import punctuation
from os import path


logging.basicConfig(filename='bo.log', level=logging.DEBUG, filemode='a',
                    format='%(levelname)s - %(message)s')


class KeyTermsExtractor:
    def __init__(self, file_path):
        self.filter_items = set(punctuation) | set(stopwords.words('english'))
        self.file_path = file_path
        self.titles = list()
        self.stories = list()  # noun tokens, joined in str: documents for calculating TF-IDF
        self.key_words = self.calculate_tf_idf()

    def parse_xml(self):
        """Parse xml file. Fill self.titles/self.stories"""
        root = etree.parse(self.file_path).getroot()
        for item in root[0]:
            title, story = [item.find(f'value[@name="{tag}"]').text for tag in ("head", "text")]
            self.titles.append(title)
            tokens = self.process_text(story)
            self.stories.append(' '.join(tokens))

    def print_key_words(self):
        for title, key_words in self.key_words.items():
            print(f'{title}:')
            print(*[key_word[0] for key_word in key_words], '\n')

    def process_text(self, some_text: str) -> list:
        """tokenize, perform lemmatization, get rid of stop words and punctuation marks"""
        tokens = nltk.tokenize.word_tokenize(some_text.lower())
        lemmatizer = WordNetLemmatizer()
        filtered_tokens = list(filter(lambda x: x not in self.filter_items, tokens))
        processed_tokens = filter(lambda x: nltk.pos_tag([x])[0][1] == 'NN',
                                  [lemmatizer.lemmatize(token) for token in filtered_tokens])
        return list(processed_tokens)

    def calculate_tf_idf(self) -> dict:
        """Calculate the TF-IDF for every word in all news stories
        Return {title: 5 key_words with highest scores}"""
        self.parse_xml()
        tfidf_scores = dict()
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.stories)
        terms = vectorizer.get_feature_names_out()
        for document_index in range(len(self.stories)):
            words_score = list(((term, score) for term, score in zip(terms, tfidf_matrix.toarray()[document_index])))
            ten_best_scores = sorted(words_score, key=lambda x: (x[1]), reverse=True)[:10]
            five_best_scores = sorted(ten_best_scores, key=lambda x: (x[1], x[0]), reverse=True)[:5]
            tfidf_scores[self.titles[document_index]] = five_best_scores
        return tfidf_scores


def main():
    filename = 'news.xml'
    # xml_path = path.join(path.dirname(__file__), "news.xml")
    new = KeyTermsExtractor(filename)
    KeyTermsExtractor.print_key_words(new)


if __name__ == '__main__':
    main()
