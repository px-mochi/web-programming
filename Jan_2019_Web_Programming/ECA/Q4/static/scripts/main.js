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

// For video buttons and pop ups (ID will overlap with profile if it is not seprated)
$('.popup-video-detail-buttons').each(function() {
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


$(document).ready(function() {
	$(document).on('click', '.bannerAd', function() { 
	    var adPath = $(this).attr("src");

	    adBannerViews.forEach(function(item){
	    	if (item['path'] === adPath) {
	    		item['views'] = item['views'] + 1;
	    		console.log(adBannerViews);
	    		var path = item['path'];
	    		var views = item['views'];
	    		var data = {"path":path,"views":views}
	    		console.log(data)

	    		$.ajax({
	    			type: "POST",
	    			url: "/get-views",
	    			data: JSON.stringify({"path":path,"views":views}),
	    			dataType: "json",
	    			contentType: "application/json"
	    		});
	    	}
	    })
	});
})