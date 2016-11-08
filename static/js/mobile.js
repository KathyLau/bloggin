function checkMobile() {
    var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    if (isMobile) {
	navmenu = document.getElementById("navmenu")
	navmenu.innerHTML = '<li class="menu"><a class="fa-bars" href="#menu">Menu</a></li>'
	menu = document.getElementById("menudiv");
	menu.innerHTML = '<section id="menu"><section><ul class="links"><li><a href="/yourstories/1"><h3>Your Stories</h3><p>View all the stories you\'ve contributed to</p></a></li><li><a href="/find/1"><h3>Find Stories</h3><p>Find and contribute to new stories</p></a></li><li><a href="/new"><h3>Create Story</h3><p>Start your own story</p></a></li></ul></section></section>'
    }
}

window.onload = checkMobile()
