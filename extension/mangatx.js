
let url = window.document.URL;
console.log(url);
chrome.runtime.sendMessage({'url': url}, function(response) {
});
