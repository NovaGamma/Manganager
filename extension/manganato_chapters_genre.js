chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    if(request.read == 1){
      console.log(request)
      for(let name of names){
        if(name.children[0].outerText == request.title){
          name.children[0].style.backgroundColor = "blue"
        }
      }
    }
  }
);


let names = document.getElementsByClassName('genres-item-info')
for(let name of names){
  title = name.children[0].outerText;
  chrome.runtime.sendMessage({"question":'isRead', 'title':title});
}
