chrome.runtime.onMessage.addListener(
  async function(request, sender, sendResponse) {
    if(request.read == 1){
      console.log(request)
      let names = document.getElementsByClassName("post-title")
      for(let name of names){
        if(name.children[0].getElementsByTagName('a')[0].outerText == request.title){
          //put the text blue
          name.children[0].getElementsByTagName('a')[0].style.color = "blue"
        }
      }
    }
  }
);

function check(){
  let names = document.getElementsByClassName("post-title")
  for(let name of names){
    title = name.children[0].getElementsByTagName('a')[0].outerText
    chrome.runtime.sendMessage({"question":'isRead', 'title':title});
  }
}

let el = document.getElementById("navigation-ajax")
el.addEventListener('click', ()=>{
  setTimeout(() => {check()}, 1000);
})
console.log("Chapters injected");
check();
