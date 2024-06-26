from flask import Flask, request, render_template   #Flask-web application start. request- handle web request from frontend
from flask_cors import CORS     #CORS- Cross Origin Resource sharing - allows requests and responses from diff domains and ports - NECESSARY FOR SPOTIFY API
import call   #imports call.py
import requests   #for webscraping part
from bs4 import BeautifulSoup  #for web scraping
from happytransformer import HappyTextClassification  #use models for text classification


app = Flask(__name__)  #initiate the Flask app
CORS(app)    #make it CORS


@app.route('/', methods=['POST'])   #the 5 urls are sent here via POST request (home address route)
def handle_data():
    data = request.get_json()   #parse the json object and get the list back
    print(data)

    """
    import a distilbert model - lightweight (lesser parameters and size) and efficient (faster) version of BERT (Bidirectional Encoder Representations from Transformers) 
    max 512 tokens allowed for a BERT model 
    can classify text quickly into 6 labels (sadness,joy,love,anger,fear,surprise)
    """
    happy_model=HappyTextClassification(model_type='Distilbert',model_name='bhadresh-savani/distilbert-base-uncased-emotion',num_labels=6)

    
    finaltext = ""
    for url in data:
        r = requests.get(url) #sends a get request to URL
        html_doc = r.text     #gets the HTML content of URL
        soup=BeautifulSoup(html_doc,"html.parser")  #parses the HTML content and stores it into BeautifulSoup object
        text=soup.get_text()     #get the text inside the HTML content
        finaltext=finaltext+text  
  
    words = finaltext.split()  
    finaltext = ' '.join(words[:100])   #get the first 100 words only (to bypass the 512 tokens limit)

    pred = happy_model.classify_text(finaltext)   #get the prediction object
    usermood =  pred.label                        #get the mood
    
    token = call.get_token()

    seedTracks = []
    seedArtists = []

    call.get_seeds(token, usermood, seedTracks, seedArtists)

    song = call.get_recommendation(token,seedTracks,seedArtists)

    print(song)

    return song

    

if __name__ == '__main__':
    app.run(debug=True)
