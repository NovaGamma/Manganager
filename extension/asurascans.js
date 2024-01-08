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

(async () => {
  await new Promise(r => setTimeout(r, 5000));
  console.log("Injected on Site");
  let url = window.document.URL;
  let title = document.getElementsByClassName('allc')[0].children[0].text
  if(!title) return;
  console.log("found title !", title)
  let chapterName = document.getElementsByClassName('entry-title')[0].innerHTML.split(' ').slice(-2)
  console.log("chapterName", chapterName);
  chrome.runtime.sendMessage({'question':'url', 'site':'asurascans', 'title':title, 'url': url, 'chapterName':chapterName.join(" ")}, function() {
  });
})()
  