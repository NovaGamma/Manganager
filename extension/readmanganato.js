chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    console.log("There was a request")
    if (request.question === "title"){
      let title = document.getElementsByClassName("panel-breadcrumb")[0].children[2].title;
      console.log(title);
      sendResponse({'title':title})
    }
    return true;
  }
);

console.log("Injected on Site");
let url = window.document.URL;
let title = document.getElementsByClassName("panel-breadcrumb")[0].children[2].title;
let chapterName = document.getElementsByClassName("panel-breadcrumb")[0].children[4].title;
chrome.runtime.sendMessage({'title':title, 'url': url, 'chapterName':chapterName}, function() {
});
