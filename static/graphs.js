$(document).ready(function() {
    // get reactor data from local storage, add heading and call functions 
    // to add charts and html elements 
    var reactors = localStorage.getItem('data');
    reactors = JSON.parse(JSON.parse(reactors));
    var dates = reactors[0].dates;
    $("#title").append(dates);
    for (var i = 0; i < reactors.length; i++) {
        var reactor = reactors[i];
        addTags(reactor.reactor);
        addCharts(reactor);
    }

    // Add html tags for reactor charts and titles 
    function addTags(reactorID) {
        var link = "<a href='#head'" + reactorID + ">" + reactorID +
            "</a>&emsp;"
        $("#chartLink").append(link);

        // TODO: fix streching
        var chartTag = "<h2 id='head'" + reactorID + ">" + reactorID + "</h2>" +
            "<canvas id='" + reactorID + "' width=\"100\" height=\"200\"></canvas>";
        $("#charts").append(chartTag);
    }

    // Add Chartjs chart to page for each of the reactors
    function addCharts(reactor) {
        ctx = document.getElementById(reactor.reactor);

        ctx.width = ctx.height *
            (ctx.clientWidth / ctx.clientHeight);

        chart = new Chart(ctx, {
            // The type of chart we want to create
            type: 'bar',
            yAxes: [{
                type: 'logarithmic'
            }],
            // The data for our dataset
            data: {
                labels: reactor.label,
                datasets: [{
                    backgroundColor: 'rgb(40, 166, 99)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: reactor.data
                }]
            },
            // Configuration options go here
            options: {
                legend: {
                    display: false,
                },
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            fontSize: 30,
                            display: true,
                            labelString: 'No. anitneutrinos per MeV per second'
                        },
                        ticks: {
                            fontSize: 20,
                            callback: function(value, index, values) {
                                return value.toExponential();
                            }
                        }
                    }],
                    xAxes: [{
                        scaleLabel: {
                            fontSize: 30,
                            display: true,
                            labelString: 'Energy level [MeV]'
                        },
                        ticks: {
                            fontSize: 15
                        }
                    }],
                }
            }
        });
    }
});