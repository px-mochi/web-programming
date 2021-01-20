$(document).ready(function() {
	if (window.location.pathname.split('?')[0] === "/data-chart") {
		createDataChart()
	} else if (window.location.pathname.split('?')[0] === "/stack-chart") {
		createStackChart()
	} else if (window.location.pathname.split('?')[0] === "/chart-filters") {
		createChartFilters()
	} else {
		console.log("No chart link was selected.")
	}

})

function loadData(header,by,grouping,groupAgg) {
	return fetch("/api?header="+header+"&by="+by+"&grouping="+grouping+"&groupAgg"+groupAgg)
		.then(function(data) {
				return data.json(); }).then(function(value) {
				var responseValue = value;
				var country = responseValue.country;
				var continent = value.continent;
				var year = value.year.map(parseFloat);
				var lifeExp = value.lifeExp.map(parseFloat);
				var population = value.population.map(parseFloat);
				var gdpPercap = value.gdpPercap.map(parseFloat);

				//Return all values
				var array = {'country':country,'continent':continent,
				'year':year,'lifeExp':lifeExp,'population':population,
				'gdpPercap':gdpPercap};

				return array
			})

		.catch(function(error){
			console.log(error);
		});
};

function createDataChart() {
	var params = (new URL(document.location)).searchParams;
	var header = params.get('header'); 
	var by = (params.get('by'));
	if (by === "pop") {
		by = "population"}

	loadData(header,by).then(function(serverData){
	var country = serverData.country;
	var continent = serverData.continent;
	var year = serverData.year;
	var lifeExp = serverData.lifeExp;
	var population = serverData.population;
	var gdpPercap = serverData.gdpPercap;
	//actual chart portion
	var ctx = document.getElementById("dataChart");
	var myLineChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: year,
			datasets: [
				{
					data: lifeExp,
					label: 'lifeExp',
					borderColor: '#f2c95a',
					backgroundColor: '#f9e8b8',
					fill: false,
					yAxisID: 'left',
					pointRadius: 0
				},
				{
					data: population,
					label: 'population',
					borderColor: '#c45850',
					backgroundColor: '#e6b6b3',
					fill: false,
					yAxisID: 'right',
					pointRadius: 0					
				},
				{
					data: gdpPercap,
					label: "gdpPercap",
					borderColor: "#5accf2",
					backgroundColor: '#a1e2f7',
					fill: false,
					yAxisID: 'left',
					pointRadius: 0
				}]
		},
		options: {
			title: [{
				display: 'true',
				position: 'top',
				fontSize: 12,
				text: by
			}],
			scales: {
				yAxes: [{
					id: 'left',
					type: 'linear',
					position: 'left'
				}, {
					id: 'right',
					type: 'linear',
					position: 'right'
				}]
			},
			tooltips: [{
				mode: 'nearest',
				enabled: true,
				backgroundColor: "#000000",
				borderWidth: 1
			}]
		}
	})

})};

function createStackChart() {
	var params = (new URL(document.location)).searchParams;
	var header = params.get('header'); 
	var by = (params.get('by')); //Not gonna use this cos I need to do this 3 times
	var grouping = (params.get('grouping'));
	var groupAgg = (params.get('groupAgg'));
	if (by === "pop") {
		by = "population"};

	loadData(header,by,grouping,groupAgg).then(function(serverData){
		return serverData
	});
	asiaData = loadData(header,'Asia',grouping,groupAgg);
	americaData = loadData(header,'Americas',grouping,groupAgg);
	europeData = loadData(header,'Europe',grouping,groupAgg);


	Promise.all([asiaData,americaData,europeData]).then(function(values){
		var asiaYear = values[0].year;
		var asiaPop = values[0].population.map(parseFloat);
		var americaYear = values[1].year;
		var americaPop = values[1].population.map(parseFloat);
		var europeYear = values[2].year;
		var europePop = values[2].population.map(parseFloat);

		var ctx = document.getElementById("stackChart");
		var stackedBar = new Chart(ctx, {
			type: 'bar',
			data: {
				labels: asiaYear,
				datasets:[
					{
						data: asiaPop,
						label: 'Asia',
						borderColor: "#ffc34d",
						backgroundColor: "#ffe6b3"
					},
					{
						data: americaPop,
						label: 'America',
						borderColor: "#42c4f0",
						backgroundColor: "#a1e2f7"						
					},
					{
						data: europePop,
						label: 'Europe',
						borderColor: "#ff333",
						backgroundColor: "#ff9999"
					}]
			},
			options: {
				scales: {
					xAxes: [{stacked: true}],
					yAxes: [{stacked: true}]
				}
			}
		})
	})
};

function createChatFilters() {}