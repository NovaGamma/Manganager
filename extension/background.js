
var up;

async function check_up(){
  let old = up;
  try{
    let response = await fetch("http://127.0.0.1:4444/API/uptime");
    console.log(response);
    up = true;
  } catch(TypeError) {
    up = false;
  }
  return old != up;
}

async function synchro_request(){
  chrome.storage.local.get('data_manganager',function(result) {
    fetch("http://127.0.0.1:4444/API/synchro",{
      method:'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(result)
    })
  })
}

chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    let change = await check_up();
    if(up){
      fetch("http://127.0.0.1:4444/API/url",{
        method:'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({'title':request.title, 'url':request.url})
      })
    }
    else{
      chrome.storage.local.get('data_manganager')
      .then(result => result.value)
      .then(value => {
        if (value == undefined){
          value = {[request.title]: [request.url]};
        }
        else{
          if (value[[request.title]] == undefined){
            value[[request.title]] = [request.url];
          }
          else{
            value[[request.title]].push(request.url);
          }
        }
        chrome.storage.local.set({'data_manganager':value})
      })
    }
    if (change && ){
      await synchro_request();
    }
    if (request.greeting === "hello")
      sendResponse({farewell: "goodbye"});
    return true;
  }
);
