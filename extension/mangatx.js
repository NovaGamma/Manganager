chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    let change = await check_up();

    if (request.question === "title"){
      let title = document.getElementsByClassName("breadcrumb")[0].children[1].children[0].innerHTML.trim();
      sendResponse({'title':title})
    }
    return true;
  }
);

console.log("Injected on Site");
let url = window.document.URL;
let title = document.getElementsByClassName("breadcrumb")[0].children[1].children[0].innerHTML.trim();
let chapterName = document.getElementsByClassName('active')[0].innerHTML.trim();
chrome.runtime.sendMessage({'title':title, 'url': url, 'chapterName':chapterName}, function(response) {
  console.log(response.farewell);
});
