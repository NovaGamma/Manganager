chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    console.log("There was a request")
    if (request.question === "title"){
      let title = document.getElementsByClassName("breadcrumb")[0].children[1].children[0].innerHTML.trim();
      console.log(title);
      sendResponse({'title':title})
    }
    return true;
  }
);

console.log("Injected on Site");
let url = window.document.URL;
let title = document.getElementsByClassName("breadcrumb")[0].children[1].children[0].innerHTML.trim();
let chapterName = document.getElementsByClassName('active')[0].innerHTML.trim();
chrome.runtime.sendMessage({'question':'url', 'site': 'mangatx', 'title':title, 'url': url, 'chapterName':chapterName}, function() {
});
