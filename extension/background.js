function get_site(url){
  if (url.match(/https:\/\/mangatx\.com\/manga\/.+\/.+\//)){
    return 'mangatx'
  }
  else if(url.match(/https:\/\/readmanganato\.com\/manga.+\/chapter-.+/)){
    return 'readmanganato'
  }
  else return 'undefined'
}

chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
      console.log(request);
      fetch("http://127.0.0.1:4444/API/url",{
        method:'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          'title':request.title,
          'url':request.url,
          'chapterName':request.chapterName,
          'site':get_site(request.url)
        })
      })
    if (request.greeting === "hello")
      sendResponse({farewell: "goodbye"});
    return true;
  }
);
