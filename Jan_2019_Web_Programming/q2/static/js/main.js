var button = document.querySelector("#add-conversation");
var buttons = document.querySelector(".sticky-buttons");

//I have absolutely 0 idea why I need to put the function into the variable vs calling
button.onclick = function() {
	var form = document.querySelector(".adding-conversation");
	if (form.style.display === "none") {
		form.style.display = "block";
		buttons.style.display = "none";
	}
	else {
		form.style.display = "none";
		buttons.style.display = "block";
	}
};

//Question 1c)
var button3 = document.querySelector("#button3");
var button3_clicked = false; //Global variable to check if button3 has been clicked
button3.onclick = function() {

	var circle = 
		`<svg width="60" height="60">
			<circle cx="30" cy="30" r="30"></circle>
		</svg>`;

	var recentConvo = document.getElementsByClassName('recent-conversations');
	var circle_avatar = document.getElementsByTagName('svg');

	if (button3_clicked) {
		$("svg").remove();
		button3_clicked = false;
	} else { //If the button wasn't already active
	$(".recent-conversations").find(".avatar:odd").prepend(circle);
	$(".recent-conversations").find("circle").css({
		"fill":"Yellow",
		"fill-opacity":"0.6",
		"position":"absolute",  
		"z-index":"1", 
		"left":"0",
		"top":"0",
		"width":"100%",
		"height":"100%",
		});
	
	button3_clicked = true;
	}
};


//Question 2d) - Templates were not used because jQuery is easier to pull checkbox name and data
var checkStorage = window.sessionStorage; //A storage object to store checkbox data

$(document).ready(function() { //When page first loads or reloads
	$(".one-chat").each(function(){
		var checkbox = $(this).find("input:checkbox")
		var checkbox_name = checkbox.attr("name");
		var checked_status = checkStorage.getItem(checkbox_name);
		if (checked_status === "true") {
			checkbox.prop("checked", true); //checkbox is ticked
			$(this).find(".status").css("color","grey"); //Set status to grey
		} else {  //If checked_status is null (newly loaded page) or "false"
			checkbox.prop("checked", false); //checkbox is not ticked
			$(this).find(".status").css("color","blue");
		}
	})
});

$("input:checkbox").change(function() { //Checks if the status of any checkbox is changed
	//Note: No css colour changing is done here. It is done after reload.
	$("input:checkbox").each(function(){
		var checkbox_name = $(this).attr("name");
		if ($(this).prop("checked") !== true) { //If checkbox is checked
			checkStorage.setItem(checkbox_name,"false");
		} else {  //If checkbox is not checked
			checkStorage.setItem(checkbox_name,"true");
		}
		//After the checkbox check and setting of sessionStorage
		window.location.reload(); //Reloads window to show update
	})
})

// Making checkbox hidden for all pages that are not "/display-change"
$(document).ready(function() {
	if (window.location.pathname !== "/display-change") {
		$(":checkbox").css("display","none");
	}

	if (window.location.pathname === "/") {
		$(".status").css("color",""); //Do not show formatting on main page
	}
});