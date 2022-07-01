chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    if(request.read == 1){
      console.log(request)
      for(let name of names){
        if(name.outerText == request.title){
          name.style.backgroundColor = "blue"
        }
      }
    }
  }
);


let names = document.getElementsByClassName('item-title')
for(let name of names){
  title = name.outerText;
  chrome.runtime.sendMessage({"question":'isRead', 'title':title});
}
