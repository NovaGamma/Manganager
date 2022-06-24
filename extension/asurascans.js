chrome.runtime.onMessage.addListener(
    async function(request, sender, sendResponse) {
      console.log("There was a request")
      if (request.question === "title"){
        let title = document.getElementsByClassName('allc')[0].children[0].text
        console.log(title);
        sendResponse({'title':title})
      }
      return true;
    }
  );
  
console.log("Injected on Site");
let url = window.document.URL;
let title = document.getElementsByClassName('allc')[0].children[0].text
let chapterName = document.getElementsByClassName('entry-title')[0].innerHTML.split(' ').slice(-2)
chrome.runtime.sendMessage({'question':'url', 'title':title, 'url': url, 'chapterName':chapterName.join(" ")}, function() {
});
  