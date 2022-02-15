document.addEventListener('keydown',(e)=>{
	if(e.key == 'ArrowRight'){
		window.location.href = document.getElementsByClassName("btn-navigation-chap")[0].children[1].href
	}
})
