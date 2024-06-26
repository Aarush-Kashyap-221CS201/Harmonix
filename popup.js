function buildPopupDom(divName, song) {
  //get the name+by and pic div
  let popupDiv = document.getElementById(divName);

  console.log("SONG: ");
  console.log(song);

  //create the name of song element
  let elementNode = document.createElement('p');  //<p> tag
  let attributeNode = document.createAttribute('class'); //create a class attribute
  let textNode = document.createTextNode(song[0]);   //create a text 
  attributeNode.value = 'song_name';                 //name the class
  elementNode.appendChild(textNode);                 //put the text in <p>
  elementNode.setAttributeNode(attributeNode);       //assign the class to <p>

  //create the author name element (same concept as above)
  let elementNode1 = document.createElement('p');
  let attributeNode1 = document.createAttribute('class');
  let textNode1 = document.createTextNode("By " + song[1]);
  attributeNode1.value = "song_artist";
  elementNode1.appendChild(textNode1);
  elementNode1.setAttributeNode(attributeNode1);

  //configure the click on link part (entire name+by+pic)
  let songlink = document.getElementById("songlink");
  songlink.href = song[2];  //put the href as spotify url

  //creating the image element
  let imgNode = document.createElement('img');
  let imgClass = document.createAttribute('class');
  let imgSrc = document.createAttribute('src'); //for src of image
  imgClass.value = 'songcover';
  imgSrc.value = song[3];  //setting the src
  imgNode.setAttributeNode(imgClass);
  imgNode.setAttributeNode(imgSrc); //putting src in image


  let containerNode = document.createElement('div');   //separate container for name+by
  let containerClass = document.createAttribute('class');
  containerClass.value = 'container';
  containerNode.setAttributeNode(containerClass);

  //configure what happens when link clicked
  songlink.addEventListener('click',(e)=>{   //e is the event handler object 
    e.preventDefault();   //prevent default behaviour of event (opening in same tab in this case)
    chrome.tabs.create({url:song[2], active: true}); //create a new tab with link as spotify url and make it active tab (open it)
  });

  containerNode.appendChild(elementNode);  //put name and by in separate div
  containerNode.appendChild(elementNode1);
  popupDiv.appendChild(containerNode);    //put both the separate div(with name and by) and div in the big div
  popupDiv.appendChild(imgNode);
}

function buildTypedUrlList(divName) {
  
  let microsecondsperDay = 1000 * 60 * 60 * 24;
  let oneDayAgo = new Date().getTime() - microsecondsperDay;  //get the timestamp of one day ago
  let urlToCount = [];    //list to store urls

  chrome.history.search(  //use the chrome history API to get history items
    {
      text: "",    //no parameters means all history items considered. if u wrote something here, only the urls with that text in title or url would be considered
      startTime: oneDayAgo,   //only search from one day ago
    },
    function (historyItems) {   //list of dictionary items, each item is {url:..,title:..,....}
     
      for (let i = 0; i < historyItems.length; ++i) {  //store all urls in the list
        let url = historyItems[i].url;
        urlToCount.push(url);
        console.log(url);
        console.log(historyItems[i].title);
      }
      onAllVisitsProcessed();   

    }
  );

  const onAllVisitsProcessed = () => {

    let urlArray = urlToCount;

    let data = urlArray.slice(0,5);  //take the recently 5 visited webpages (chrome history API gives url in descending order of visit time - recent first)
    for(let i=0; i<data.length; i++)
    {
      console.log(data[i]);
    }

    let song = [" "," "," ", " "];

    fetch('http://127.0.0.1:5000/' , {   //fetch sends a HTTP request to backend. this is the home address route
      method: 'POST',   //POST request as sent to backend
      headers: { 'Content-Type': 'application/json' },  //body is JSON object
      body: JSON.stringify(data)   //converts recent 5 urls to JSON object and sends to backend

    }).then(response=>response.json())   //parses the received response (which is again JSON)
      .then(res=>{                       //this is the result after parsing the JSON object received
        console.log(res); 
        song = res;                       //make song variable same as response. ['name of song','name of author','spotify link','image link']
        buildPopupDom(divName,song);
      })
      .catch(error=>console.log(error));


    
  };
}

document.addEventListener("DOMContentLoaded", function () {   //loaded when the HTML doc is initially loaded (without the stylesheets,images etc.) due to clicking on extension so that no error because an element not created
  buildTypedUrlList("typedUrl_div");                          //give the name of div which holds name,by and image 

  
});


