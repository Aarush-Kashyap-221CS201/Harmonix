# Harmonix
This project is an easy-to-use Chrome Extension which recommends you song based on the 'mood' of your recent search history

## Working

1. The extension uses the manifest.json file which refers to popup.html as its HTML document and popup.js as its JS file
2. The icon of the extension is the ivon.png file
3. As soon as the extension is clicked, the Chrome History API is used to get the recent 5 URLs in the search history of the user
4. The URLs are sent to backend flask server running on server.py via the Fetch API
5. The webpages corresponding to the 5 URLs are scrapped and the text is used to get the mood using a Happy Transformer Model
6. Now, we get the Spotify access token using call.py file
7. The access token and the mood is used to get certain seed artists and seed tracks corresponding to the mood
8. A random combination of an artist and track is used to get a recommendation from Spotify
9. That exact recommended song is sent back to JS which populates the extension, providing the name, singer, cover pic and the link to Spotify page

## How to Use

1. Download all files and put into a directory
2. Make an .env file and put your Client ID and Secret (obtained from the Spotify Dev Dashboard)
3. Run the server.py file
4. Click on the extension to get a recommendation
