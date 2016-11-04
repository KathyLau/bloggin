function checkMobile() {
    var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    if (isMobile) {
	navmenu = document.getElementById("navmenu")
	navmenu.innerHTML = '<li class="menu"><a class="fa-bars" href="#menu">Menu</a></li>'
	menu = document.getElementById("menudiv");
	menu.innerHTML = '<section id="menu"><section><ul class="links"><li><a href="#"><h3>Lorem ipsum</h3><p>Feugiat tempus veroeros dolor</p></a></li><li><a href="#"><h3>Dolor sit amet</h3><p>Sed vitae justo condimentum</p></a></li><li><a href="#"><h3>Feugiat veroeros</h3><p>Phasellus sed ultricies mi congue</p></a></li><li><a href="#"><h3>Etiam sed consequat</h3><p>Porta lectus amet ultricies</p></a></li></ul></section></section>'
    }
}

window.onload = checkMobile()
