import collections

from flask import Flask, render_template, request
import os
import re
import string
from textblob import TextBlob
import nltk
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

app = Flask(__name__)
app.config["DEBUG"] = True
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Link to home page
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


# Upload Multiple files
@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        # Multiple file upload to be implemented
        f = request.files['file']
        if f.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            f.save(file_path)
        return 'file uploaded successfully'


# Search inputs for user
@app.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        searchWord1 = request.form.get("searchWord1")

        n = request.form.get("n")
        top = request.form.get("top")

        number = request.form.get("number")

        if searchWord1 != None:
            words = []
            words.append(searchWord1)
            result = (searchWordCount(words))
            return render_template('data.html', result=result)
        elif n != None and top != None:
            result = str(searchTopNGrams(int(n), int(top)))
            return render_template('nGramsData.html', result=result)
        elif number != None:
            answer = punctuateData(int(number))
            result = {'output':answer, 'length':len(answer)}
            return render_template('nGramsData.html', result=result)


@app.route("/searchWordForm")
def searchWordForm():
    return render_template('searchWordForm.html')


@app.route("/nGramsForm")
def nGramsForm():
    return render_template('nGramsForm.html')

@app.route("/punctuateForm")
def punctuateForm():
    return render_template('punctuateForm.html')


# Frequency of each word in a document
def searchWordCount(searchWords):
    words = []
    nltk.download('popular')
    file_list = os.listdir(app.config['UPLOAD_FOLDER'])
    for index, file in enumerate(file_list):
        with open(os.path.join(app.config['UPLOAD_FOLDER'], file), encoding="ISO-8859-1") as f:
            input = f.read()
            data = cleanPunctuate(input)
            text = TextBlob(data)
            for searchWord in searchWords:
                if(searchWord != None and searchWord != ''):
                    count = text.words.count(searchWord)
                    words.append({'DocumentName': searchWord, 'Frequency': count})
    return words


# topNGrams(data, n, top)
# text2 = str(stem_text(text))
# text2 = TextBlob(text2)
# count2 = text2.words.count(searchWord)


# Bi-grams, Tri-grams, N-grams implementation
def searchTopNGrams(n, top):
    result = []
    nltk.download('popular')
    file_list = os.listdir(app.config['UPLOAD_FOLDER'])
    for index, file in enumerate(file_list):
        with open(os.path.join(app.config['UPLOAD_FOLDER'], file), encoding="ISO-8859-1") as f:
            data = f.read()
            data = cleanData(data)
            result.append(topNGrams(data, n, top))
    return result

def punctuateData(number):
    words = ''
    nltk.download('popular')
    file_list = os.listdir(app.config['UPLOAD_FOLDER'])
    for index, file in enumerate(file_list):
        with open(os.path.join(app.config['UPLOAD_FOLDER'], file), encoding="ISO-8859-1") as f:
            input = f.read()
            data = cleanPunctuate(input)
            words = data[0:number]
    return words

def cleanPunctuate(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    newVal = text.encode("ascii", "ignore")
    newtext = newVal.decode()
    newtext = removeSetOfWords(newtext)
    return newtext


def topNGrams(text, n, top):
    nGrams = ngrams(str(remove_stopwords(text)).split(), n)
    nGramsFreq = collections.Counter(nGrams)
    return str(nGramsFreq.most_common(top))


def cleanData(data):
    data = re.sub(r"[^A-Za-z0-9\s]+", " ", data)
    data = re.sub(r'@\w+', '', data)
    data = data.lower()
    data = re.sub(r'[%s]9' % re.escape(string.punctuation), ' ', data)
    data = re.sub(r'[0-]', '', data)
    data = re.sub(r'\s{2,}', ' ', data)
    return data


def remove_punctuation(text):
    text = re.sub(r'[^\w\s]+', ' ', text)
    return text

def remove_stopwords(text):
    stopwordsSet = set(stopwords.words("english"))
    text = ' '.join([word for word in text.split() if word not in stopwordsSet])
    return text

def stem_text(text):
    text = ' '.join([stm.stem(word) for word in text.split()])
    return text


stm = PorterStemmer()
lmtz = WordNetLemmatizer()


if __name__ == '__main__':
    app.run(debug=True)