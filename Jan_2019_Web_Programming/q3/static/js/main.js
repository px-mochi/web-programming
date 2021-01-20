var nextTen = document.querySelector("#nextTen");


nextTen.onclick = function () {
	// Get current max number of rows shown
	var currentRow = window.location.pathname.replace(/\//g,'');
	var newRow = Number(currentRow) + 10;
	// If the new max is > 3312, set it to 3312 as that is the last record.
	if (newRow <= 3312) {
		var newURL = "location.href='/" + (newRow).toString() + "';";
	} else {
		var newURL = "location.href = '/3312';";
	}
	// Reassign the hyperlink linked to the button
	$("#nextTen").attr("onclick", newURL);	
}

// Assign relevant URLs to the table headers and hide delete elements if in homepage
$(document).ready(function() {
	$("th a").each(function() {
		var currentPage = window.location.pathname;
		if (window.location.pathname === "/") {
			currentPage = "/10"
		}
		var headerName = $(this).text().trim();
		if (headerName === "pop") {
			headerName = "population"
		}
		var newLink = $(this).attr("href", currentPage+"?key="+headerName);
	});

	if  (window.location.pathname === "/") {
		$("#delete").hide();
		$(".delete-warning").hide();
		$(".checkbox-table-header").hide();
		$(".checkbox-table-row").hide();
	}
});

// Function that runs after delete is clicked
function deleteRow() {
	var pathName = window.location.pathname;
	var checked_collection = {}  //This is just a javascript object.
	$("input:checkbox").each(function () {
		var checkbox_id = $(this).attr("value");
		var checked_status = $(this).prop("checked"); //Check current attribute of check box
		checked_collection[checkbox_id] = checked_status;
	})
	var urlQuery = "?"
	for(var key in checked_collection) {
		var value = checked_collection[key];
		urlQuery += key + "=" + value + "&";
	}
	window.location.href = urlQuery;
}
