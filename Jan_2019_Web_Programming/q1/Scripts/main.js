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
}

$(".adding-conversation").submit(function(event) {
	//Stops the submit button from refreshing the html again
	event.preventDefault();

	//Get form values
	var name = document.getElementById("nameInput").value;
	var status = document.getElementById("statusInput").value;
	var message = document.getElementById("messageInput").value;
	
	//Finds the correct avatar based on name, or a placeholder if not an existing chat
	var avatar = "";
	if (name === "Finn") {
		avatar = "Avatars/001-man.png";
	} else if (name === "Han") {
		avatar = "Avatars/005-man-3.png";
	} else if (name === "Rey") {
		avatar = "Avatars/006-gentleman.png";
	} else if (name === "Luke") {
		avatar = "Avatars/008-man-4.png";
	} else if (name === "Poe") {
		avatar = "Avatars/009-punk.png";
	} else if (name === "Ben") {
		avatar = "Avatars/022-man-5.png";
	} else if (name === "Leia") {
		avatar = "Avatars/016-woman-8.png";
	} else {
		avatar = "Avatars/blank-avatar.png";
	}


	//html code to add
	var newConversation = 
		`<li class="one-chat clearfix">
		 	<div class="avatar"><img src="${avatar}" alt = "${name}-avatar"></div>
		 	<div class="text-container">
			 	<h1>${name}</h1>
			 	<span class="status">${status}</span>
			 	<br>
			 	<p class="last-message">${message}</p>
		 	</div>
		</li>`;

	//Adds new html to the top of "Recent Conversations"
	$("ul.recent-conversations").prepend(newConversation);

	//alert(newConversation);

	//Clears form for new input
	$('#conversation-form').trigger("reset");

	//Hides form, show original button
	var form = document.querySelector(".adding-conversation");
	var buttons = document.querySelector(".sticky-buttons");
	form.style.display = "none";
	buttons.style.display = "block";
});


//Question 1c)
var button2 = document.querySelector("#button2");
var button2_clicked = false

button2.onclick = function() {

	if (button2_clicked) { //If button was previously clicked
		$(".recent-conversations").find("h1").css("font-weight","");
		$(".recent-conversations").find(".status").css("color","")
		$(".recent-conversations").find("p").css("color","");
		button2_clicked = false
	} else { //Add css if button hasn't been clicked yet
	$(".recent-conversations").find("h1").css("font-weight","bold");
	$(".recent-conversations").find(".status").css("color","blue")
	//Change even numbered items in list - jQuery is 0 indexed.
	$(".recent-conversations").find("p:odd").css("color","LightGreen");
	button2_clicked = true
	}
};

//Question 1d)
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