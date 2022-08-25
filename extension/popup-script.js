import get_site from './utils.js'

var query = { active: true, currentWindow: true };
chrome.tabs.query(query, async function(tabs){
  var currentTab = tabs[0]
  let url = currentTab.url;

  try{
    let response = await fetch("http://127.0.0.1:4444/API/uptime");
    console.log(response);
    var up = true;
  } catch(TypeError) {
    var up = false;
  }

  const site = get_site(url);
  if (site == undefined) return;

  var title;
  chrome.tabs.sendMessage(currentTab.id, {'question':'title'}, async function(response){
    console.log(response)
    if(response.title != undefined){
      title = response.title;
      console.log(title);
      if(up){
        let response = await fetch("http://127.0.0.1:4444/API/followed",{
          method:'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({'title':title, 'site':site})
        });
        let followed = await response.json()
        console.log(followed)
        let container = document.getElementById('container');
        let button = document.createElement('button');
        button.className = "button";
        if (!followed.followed){
          button.innerHTML = "Follow Series";
          button.addEventListener('click', () => {
            fetch("http://127.0.0.1:4444/API/follow",{
              method:'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({'title':title, 'site':site, 'url':url, 'site':site})
            });
          });
        }
        else{
          button.innerHTML = "Already followed";
        }
        container.appendChild(button);
      }
      else{
      container = document.getElementById('container');
      container.innerHTML = 'The server is not on';
      }
    }
  });


});
