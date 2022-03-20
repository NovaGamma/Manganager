chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log(sender.tab ?
                "from a content script:" + sender.tab.url :
                "from the extension");
    fetch("http://127.0.0.1:4444/API/url",{
      method:'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({'url':request.url})
    })
    if (request.greeting === "hello")
      sendResponse({farewell: "goodbye"});
    return true;
  }
);
