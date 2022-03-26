
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
  chrome.storage.local.get(['data_manganager'],function(result) {
    fetch("http://127.0.0.1:4444/API/synchro",{
      method:'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(result.data_manganager)
    })
  })
}

chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    let change = await check_up();
    if(up){
      console.log(request);
      fetch("http://127.0.0.1:4444/API/url",{
        method:'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          'title':request.title,
          'url':request.url,
          'chapterName':request.chapterName
        })
      })
    }
    else{
      chrome.storage.local.get('data_manganager', function(result){
        let value = result.data_manganager
        if (value == undefined){
          console.log("was undefined");
          value = {[request.title]: [request.url]};
        }
        else{
          console.log("was defined");
          if (value[[request.title]] == undefined){
            console.log("series undefined"),
            value[[request.title]] = [request.url];
          }
          else{
            console.log("series defined");
            value[[request.title]].push(request.url);
          }
        }
        console.log("set value");
        chrome.storage.local.set({'data_manganager':value}, function() {
          console.log('Value is set to ' + value);
        });
      })
    }
    if (change && up==true){
      await synchro_request();
    }
    if (request.greeting === "hello")
      sendResponse({farewell: "goodbye"});
    return true;
  }
);
