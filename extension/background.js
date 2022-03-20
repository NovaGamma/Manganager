
var up;

async function check_up(){
  try{
    let response = await fetch("http://127.0.0.1:4444/API/uptime");
    console.log(response);
    up = true;
  } catch(TypeError) {
    up = false;
  }
}

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    await check_up();
    if(up){
      fetch("http://127.0.0.1:4444/API/url",{
        method:'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({'url':request.url})
      })
    }
    else{
      console.log("Not implemented yet")
    }
    if (request.greeting === "hello")
      sendResponse({farewell: "goodbye"});
    return true;
  }
);
