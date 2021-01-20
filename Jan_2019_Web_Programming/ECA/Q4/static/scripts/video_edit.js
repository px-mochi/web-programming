// For video buttons and pop ups (ID will overlap with profile if it is not seprated)
$('.popup-edit-buttons').each(function() {
	var buttonid = $(this).attr('id');
	var button = $(this);
	var popupID = buttonid.replace('btn-edit-','');
	button.click(function() {
		var windowID = "#"+popupID
		$(windowID).css("display","block");
		$(windowID).focus();
		$(windowID).find('#videoid').val(popupID);
	})
})


$(document).ready(function() {
	// Hover to play video seems to only work correctly on Chrome.
	$(document).on('mouseover', 'video', function() { 
	    var playPromise = $(this).get(0).play(); //Chrome returns a promise
	    if (playPromise !== undefined) {
			playPromise.then(function() {
		    // Video has already started playing
		  }).catch(function(error) {
		    // Automatic playback failed. Insert error message for ECA:
		    var errorFlash = 
		    	`<ul class="flashes absolute" id="autoplayError">
	      			<li class="error">ECA Note: This browser blocks the autoplaying of video via JS without user interaction. Click anywhere to activate it.</li>
	    	    </ul>`;
	    	var flashAlone = 
	    		`<li class="error">ECA Note: This browser blocks the autoplaying of video via JS without user interaction. Click anywhere to activate it.</li>`
	    	if ($("#autoplayError").length){
	    		// Error message already on screen.
	    	} if (($(".flashes").length) && !($("#autoplayError").length)){
	    		$(".flashes").prepend(flashAlone);
	    	} else {
	    		$(".body-container").prepend(errorFlash);
	    	}
		    console.log("ECA Note: Click anywhere to trigger the autoplaying on mouseover if on Chrome")
		  });
}

	}); 
	$(document).on('mouseleave', 'video', function() { 
	    $(this).get(0).pause(); 
	});
})


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