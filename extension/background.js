import get_site from './utils.js'

chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
      console.log(request);
      if(request.question == "url"){
      fetch("http://127.0.0.1:4444/API/url",{
        method:'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          'title':request.title,
          'url':request.url,
          'chapterName':request.chapterName,
          'site':request.site,
        })
      })}
      else if(request.question == "isRead"){
        let res = await fetch("http://127.0.0.1:4444/API/read",{
          method:'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({'title':request.title})
        });
        let text = await res.text()
        var query = { active: true, currentWindow: true };
        chrome.tabs.query(query, async function(tabs){
          var currentTab = tabs[0]
          chrome.tabs.sendMessage(currentTab.id, {'title':request.title,'read':text});
        })
      }
    return true;
  }
);
