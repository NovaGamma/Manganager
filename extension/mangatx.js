
let url = window.document.URL;
console.log(url);
let title = 'temp';
chrome.runtime.sendMessage({'title':title, 'url': url}, function(response) {
  console.log(response.farewell);
});
