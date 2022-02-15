
function getInfoMangakalot(){
  let raw = document.getElementsByClassName("panel-chapter-info-top");
  let info = raw[0].children[0].innerHTML;
  return info;
}

function getInfoMangatx(){
  let raw = document.getElementById("chapter-heading");
  let info = raw.innerHTML
  return info;
}

var url = document.URL;
let found = false;
/*if(url.startsWith("https://manganelo.com")){
  var info = getInfoMangakalot();
  found = true;
}*/
if(url.startsWith("https://mangatx.com")){
  var info = getInfoMangatx();
  found = true;
}
var sent = false;
if(found == true){
    sent = fetch("http://192.168.1.80:5000/url/"+info, {
      method: "POST",
      mode:"no-cors",
      body: info
    }).then(res => {
      console.log("Request complete! response:", res);
      return true;
    });
  if(sent == false){
    alert("Request wasn't able to be sent");
  }
}
