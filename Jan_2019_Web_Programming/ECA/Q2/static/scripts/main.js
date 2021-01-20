$(document).ready(function() {
	// Hover to play video seems to only work correctly on Chrome.
	$(document).on('mouseover', 'video', function() { 
	    $(this).get(0).play(); 
	}); 
	$(document).on('mouseleave', 'video', function() { 
	    $(this).get(0).pause(); 
	});
})

// Opens all pop ups when related button is clicked (Profile, about, terms)
$('.popup-detail-buttons').each(function() {
	var buttonid = $(this).attr('id');
	var button = $(this);
	var popupID = buttonid.replace('btn-','');
	button.click(function() {
		var windowID = "#"+popupID
		$(windowID).css("display","block");
		$(windowID).focus();
		closeWindow(windowID)
	})
})

// Closes popups on tab/click outside
function closeWindow(windowID) {
	$(windowID).focusout(function () {
		$(this).css("display","none");
	})
};

// Autoplaying banner advertisements
$(document).ready(function() {
	$("#advertisement-container > img:gt(0)").hide();

	setInterval(function() { 
	  $('#advertisement-container > img:first')
	    .hide()
	    .next()
	    .show()
	    .end()
	    .appendTo('#advertisement-container');
	},  2000);
})