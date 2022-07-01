chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    console.log("There was a request")
    if (request.question === "title"){
      let title = document.getElementsByClassName('breadcrumb')[0].children[0].children[2].children[0].title
      console.log(title);
      sendResponse({'title':title})
    }
    return true;
  }
);

console.log("Injected on Site");
let url = window.document.URL;
let title = document.getElementsByClassName('breadcrumb')[0].children[0].children[2].children[0].title
let chapterName = document.getElementsByClassName('breadcrumb')[0].children[0].children[4].children[0].children[0].innerHTML
chrome.runtime.sendMessage({'question':'url', 'title':title, 'url': url, 'chapterName':chapterName}, function() {
});
