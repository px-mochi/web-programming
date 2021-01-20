var ctx = document.getElementById('chart1').getContext('2d');
var cty = document.getElementById('chart2').getContext('2d');

var videoPosts = chartData['videoPosts'];
var storageUsed = chartData['storageUsed'];
var userList = chartData['userList'];

console.log(videoPosts);
console.log(storageUsed);
console.log(userList);

function createChart1() {
	var chart1 = new Chart(ctx, {
		type: 'line',
		data: {
			labels: userList,
			datasets: [{
				label: 'Video Posts',
				backgroundColour: 'rgb(255, 99, 132)',
				borderColor: 'rgb(255, 99, 132)',
            	data: videoPosts
			}]
		},
}

)}

function createChart2() {
	var chart2 = new Chart(cty, {
		type: 'line',
		data: {
			labels: userList,
			datasets: [{
				label: 'Storage Used',
				backgroundColour: 'rgb(255, 99, 132)',
				borderColor: 'rgb(255, 99, 132)',
            	data: videoPosts
			}]
		},
}

		)
}


$(document).ready(function() {
	createChart1();
	createChart2();
})