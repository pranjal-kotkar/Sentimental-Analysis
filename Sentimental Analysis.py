
#Install nltk
pip install nltk

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import re
import string
from textblob import TextBlob
import nltk

from nltk.corpus import stopwords

nltk.download('punkt')

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

from keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from keras.layers import LSTM, Dense, SimpleRNN, Embedding, Flatten, Dropout
from keras.activations import softmax
from sklearn.model_selection import train_test_split

"""For ignoring warnings"""

import warnings
warnings.filterwarnings('ignore')

pip install emoji

import emoji

df = pd.read_csv('Sentiment.csv', encoding='latin-1')
df.head()

# Rename columns
df.rename(columns={'message to examine': 'Text', 'label (depression result)': 'Label'}, inplace=True)
df.head()

df.shape

# Convert 'Text' column to lowercase
df['Text'] = df['Text'].str.lower()
df.head()

from bs4 import BeautifulSoup

def remove_html_tags(text):
    if isinstance(text, str):  # Check if text is a string
        soup = BeautifulSoup(text, 'html.parser')
        return soup.get_text()
    else:
        return str(text)  # Convert non-string input to string

# Assuming 'df' is your DataFrame containing the 'Text' column
# Apply the remove_html_tags function to the 'Text' column
df['Text'] = df['Text'].apply(remove_html_tags)

# Define a function to remove URLs using regular expressions
def remove_urls(text):
    return re.sub(r'http\S+|www\S+', '', text)

# Apply the function to the 'Text' column
df['Text'] = df['Text'].apply(remove_urls)

string.punctuation

punctuation=string.punctuation

def remove(text):
   return  text.translate(str.maketrans(' ',' ',punctuation))

df['Text']=df['Text'].apply(remove)

df.head(15)

chat_words = {
    "AFAIK": "As Far As I Know",
    "AFK": "Away From Keyboard",
    "ASAP": "As Soon As Possible",
    "ATK": "At The Keyboard",
    "ATM": "At The Moment",
    "A3": "Anytime, Anywhere, Anyplace",
    "BAK": "Back At Keyboard",
    "BBL": "Be Back Later",
    "BBS": "Be Back Soon",
    "BFN": "Bye For Now",
    "B4N": "Bye For Now",
    "BRB": "Be Right Back",
    "BRT": "Be Right There",
    "BTW": "By The Way",
    "B4": "Before",
    "B4N": "Bye For Now",
    "CU": "See You",
    "CUL8R": "See You Later",
    "CYA": "See You",
    "FAQ": "Frequently Asked Questions",
    "FC": "Fingers Crossed",
    "FWIW": "For What It's Worth",
    "FYI": "For Your Information",
    "GAL": "Get A Life",
    "GG": "Good Game",
    "GN": "Good Night",
    "GMTA": "Great Minds Think Alike",
    "GR8": "Great!",
    "G9": "Genius",
    "IC": "I See",
    "ICQ": "I Seek you (also a chat program)",
    "ILU": "ILU: I Love You",
    "IMHO": "In My Honest/Humble Opinion",
    "IMO": "In My Opinion",
    "IOW": "In Other Words",
    "IRL": "In Real Life",
    "KISS": "Keep It Simple, Stupid",
    "LDR": "Long Distance Relationship",
    "LMAO": "Laugh My A.. Off",
    "LOL": "Laughing Out Loud",
    "LTNS": "Long Time No See",
    "L8R": "Later",
    "MTE": "My Thoughts Exactly",
    "M8": "Mate",
    "NRN": "No Reply Necessary",
    "OIC": "Oh I See",
    "PITA": "Pain In The A..",
    "PRT": "Party",
    "PRW": "Parents Are Watching",
    "QPSA?": "Que Pasa?",
    "ROFL": "Rolling On The Floor Laughing",
    "ROFLOL": "Rolling On The Floor Laughing Out Loud",
    "ROTFLMAO": "Rolling On The Floor Laughing My A.. Off",
    "SK8": "Skate",
    "STATS": "Your sex and age",
    "ASL": "Age, Sex, Location",
    "THX": "Thank You",
    "TTFN": "Ta-Ta For Now!",
    "TTYL": "Talk To You Later",
    "U": "You",
    "U2": "You Too",
    "U4E": "Yours For Ever",
    "WB": "Welcome Back",
    "WTF": "What The F...",
    "WTG": "Way To Go!",
    "WUF": "Where Are You From?",
    "W8": "Wait...",
    "7K": "Sick:-D Laugher",
    "TFW": "That feeling when",
    "MFW": "My face when",
    "MRW": "My reaction when",
    "IFYP": "I feel your pain",
    "TNTL": "Trying not to laugh",
    "JK": "Just kidding",
    "IDC": "I don't care",
    "ILY": "I love you",
    "IMU": "I miss you",
    "ADIH": "Another day in hell",
    "ZZZ": "Sleeping, bored, tired",
    "WYWH": "Wish you were here",
    "TIME": "Tears in my eyes",
    "BAE": "Before anyone else",
    "FIMH": "Forever in my heart",
    "BSAAW": "Big smile and a wink",
    "BWL": "Bursting with laughter",
    "BFF": "Best friends forever",
    "CSL": "Can't stop laughing"
}

def replace_chat_words(text):
   words=text.split()
   for i,word in enumerate(words):
     if word.lower() in chat_words:
        words[i]=chat_words[word.lower()]
   return ' '.join(words)

df['Text']= df['Text'].apply(replace_chat_words)



'''
# Define the replace_chat_words function
def replace_chat_words(text):
    words = text.split()
    for i, word in enumerate(words):
        if word.lower() in chat_words:
            words[i] = chat_words[word.lower()]
    return ' '.join(words)

# Apply replace_chat_words function to 'Text' column
df['Text'] = df['Text'].apply(replace_chat_words)
'''

nltk.download('stopwords')

stop_words=set(stopwords.words('english'))

def remove_stopwords(text):
   words=text.split()
   filtered_words=[word for word in words if word.lower() not in stop_words]
   return ' '.join(filtered_words)

df['Text']=df['Text'].apply(remove_stopwords)

def remove_emoji(text):
  return emoji.demojize(text)

df['Text']=df['Text'].apply(remove_emoji)

def lemmatize(text):
   word_lemmatize=WordNetLemmatizer()

   df['Lemmatized Text']=df['Text'].apply(lambda x: ''.join([word_lemmatize.lemmatize(word,pos='v') for word in x.split()]))
   return ' '.join([word_lemmatize.lemmatize(word, pos='v') for word in text.split()])


df.head()

X=df['Text']
y=df['Label']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2,random_state=42)

tokenizer=Tokenizer(oov_token ='nothing')
tokenizer.fit_on_texts(X_train)
tokenizer.fit_on_texts(X_test)

tokenizer.document_count

X_train_sequences=tokenizer.texts_to_sequences(X_train)
X_test_sequences=tokenizer.texts_to_sequences(X_test)

maxlen=max(len(tokens) for tokens in X_train_sequences)
print("Maximum length of X_train_sequence:",maxlen)

X_train_padded=pad_sequences(X_train_sequences,maxlen=maxlen,padding='post')
X_test_padded=pad_sequences(X_test_sequences,maxlen=maxlen,padding='post')

print("X_train_padded\n",X_train_padded)
print("X_test_padded\n",X_test_padded)

size=np.max(X_train_padded) +1
print(size)

model=Sequential()
model.add(LSTM(128,input_shape=(37,1),return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(128))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dense(1,activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

history = model.fit(X_train_padded, y_train, epochs=5, batch_size=32, validation_data=(X_test_padded, y_test))

# Plotting the training and testing accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.show()

# Plotting the training and testing loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper right')
plt.show()

# Save the model
model.save("model_1.h5")

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load the model
loaded_model = load_model("model_1.h5")

# Example tweet
tweet = ""

word_lemmatizer = WordNetLemmatizer()

def lemmatize1(text):
    global word_lemmatizer  # Use the global WordNetLemmatizer

    # Lemmatize each word in the text and join them back
    return ' '.join([word_lemmatizer.lemmatize(word, pos='v') for word in text.split()])


# Preprocess the tweet
preprocessed_tweet = remove_html_tags(tweet)
preprocessed_tweet =remove_urls(tweet)
preprocessed_tweet =remove(tweet)
preprocessed_tweet =replace_chat_words(tweet)
preprocessed_tweet =remove_stopwords(tweet)
preprocessed_tweet =remove_emoji(tweet)
preprocessed_tweet=lemmatize1(tweet)

# Tokenize and pad the preprocessed tweet
tweet_sequence = tokenizer.texts_to_sequences([preprocessed_tweet])
tweet_padded = pad_sequences(tweet_sequence, maxlen=maxlen, padding='post')

# Make prediction
prediction = loaded_model.predict(tweet_padded)

print(prediction)

if prediction >= 0.5:
  print("Negative")
else :
  print("Positive")
