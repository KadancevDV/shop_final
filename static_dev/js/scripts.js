(function () {
	
	var addToCart = function() {
		var xhr = new XMLHttpRequest();
		xhr.open('GET', '/cart_action?action=add&id=' + this.getAttribute("data-id"), false);
		xhr.send();
		
		if (xhr.status != 200) {
			alert( xhr.status + ': ' + xhr.statusText );
		} else {
			document.getElementById('cart-qty-container').innerHTML = xhr.responseText;
		}
		
		return false;
	};
	
	var deleteFromCart = function() {
		var xhr = new XMLHttpRequest();
		xhr.open('GET', '/cart_action?action=delete&id=' + this.getAttribute("data-id"), false);
		xhr.send();
		
		if (xhr.status != 200) {
			alert( xhr.status + ': ' + xhr.statusText );
		} else {
			location.reload();
		}
		
		return false;
	};
	
	var addToCartButtons = document.getElementsByClassName("action-add-to-cart");
    var deleteFromCartButtons = document.getElementsByClassName("action-delete-from-cart");

	for (var i = 0; i < addToCartButtons.length; i++) {
		addToCartButtons[i].addEventListener('click', addToCart, false);
	}
	
	for (var i = 0; i < deleteFromCartButtons.length; i++) {
		deleteFromCartButtons[i].addEventListener('click', deleteFromCart, false);
	}
})();


