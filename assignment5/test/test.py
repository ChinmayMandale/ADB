import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

pages = [r"C:\Users\ojasb\OneDrive\Desktop\Chinmay\ADB\ADB\assignment5\AliceCleaner.txt",r"C:\Users\ojasb\OneDrive\Desktop\Chinmay\ADB\ADB\assignment5\AliceInWonderland.txt"]

for i in pages:
    with open(i) as inp:
        data = inp.read().split()
        # print(data)
        documents_clean = []
        for d in data:
            document_test = re.sub(r'[^\x00-\x7F]+', ' ', d)
            document_test = re.sub(r'@\w+', '', document_test)
            document_test = document_test.lower()
            document_test = re.sub(r'[%s]9' % re.escape(string.punctuation), ' ', document_test)
            document_test = re.sub(r'[0-]', '', document_test)
            document_test = re.sub(r'\s{2,}', ' ', document_test)
            documents_clean.append(document_test)
        print(documents_clean)
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(documents_clean)
        X = X.T.toarray()
        df = pd.DataFrame(X, index=vectorizer.get_feature_names_out())
        # print(df)
