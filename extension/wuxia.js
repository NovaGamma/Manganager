console.log('Hello');

setTimeout(() => {
	document.addEventListener('keydown',(e)=>{
		if(e.key == 'ArrowRight'){
			let array = window.location.href.split('/')
			let temp = array[array.length - 1].split('-');
			temp[temp.length - 1] = parseInt(temp[temp.length - 1]) + 1;
			array[array.length - 1] = temp.join('-');
			window.location.href = array.join('/');
		}
	})
}, 2000);
