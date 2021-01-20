// Specifically for the ECA note where chrome blocks video autoplay without user input
$(document).on('mouseover', 'video', function() {
	if ($('.flashes:visible').length) {
		hideFlash();
	}
});
$(document).on('mouseleave', 'video', function() {
	if ($('.flashes:visible').length) {
		hideFlash();
	}
});


function hideFlash() {
	console.log("Hiding flash")
	$(".flashes").fadeOut(5000, function() {
	});
}