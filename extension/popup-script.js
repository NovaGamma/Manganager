console.log("Hello it's working");
var query = { active: true, currentWindow: true };
chrome.tabs.query(query, async function(tabs){
  var currentTab = tabs[0]
  let url = currentTab.url;

  let response = await fetch("http://192.168.1.80:5000/url_check",{
    method:'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({'url':url})
  })

  container = document.getElementById('container');

  let answer = await response.json();
  if(answer == 'OK'){
    button = document.createElement('button');
    button.className = "button";
    button.innerHTML = "Download"
    button.addEventListener('click', () => {
      fetch("http://192.168.1.80:5000/request",{
        method:'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({'url':url}),
        }
      );
    });
    container.appendChild(button);
  }
  else{
    text = document.createElement('p');
    text.innerHTML = "This site is not currently supported";
    container.appendChild(text);
  }
});
