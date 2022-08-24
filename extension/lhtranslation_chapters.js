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
  
function check(){
    for(let name of names){
        title = name.outerText;
        chrome.runtime.sendMessage({"question":'isRead', 'title':title});
    }
}
    
let names = document.getElementsByClassName('post-title font-title')
let el = document.getElementById("navigation-ajax")
el.addEventListener('click', ()=>{
  setTimeout(() => {check()}, 1000);
})
console.log("Chapters injected");
check();