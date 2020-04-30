$(document).ready(function() {
    var colours = ['rgb(169, 212, 161)', 'rgb(132, 163, 227)', 'rgb(143, 201, 194)', 'rgb(183, 169, 199)', 'rgb(106, 200, 150)', 'rgb(153, 177, 209)'];
    // get reactor data from local storage, add heading and call functions 
    // to add charts and html elements 
    var reactors = localStorage.getItem('data');
    reactors = JSON.parse(JSON.parse(reactors));
    var dates = reactors[0].dates;
    $("#title").append(dates);
    for (var i = 0; i < reactors.length; i++) {
        var reactor = reactors[i];
        addTags(reactor.reactor);
        var colour = colours[i % 6];
        addCharts(reactor, colour);
    }
    $(".chartjs-hidden-iframe").remove();

    // Add html tags for reactor charts and titles 
    function addTags(reactorID) {
        var link = "<a href='#head" + reactorID + "'>" + reactorID +
            "</a>&emsp;"
        $("#chartLink").append(link);

        // TODO: fix streching
        var chartTag = "<h2 id='head" + reactorID + "'>" + reactorID + "</h2>" +
            "<canvas id='" + reactorID + "' width='1100' height='800'></canvas>";
        $("#charts").append(chartTag);
    }

    // Add Chartjs chart to page for each of the reactors
    function addCharts(reactor, colour) {
        ctx = document.getElementById(reactor.reactor).getContext('2d');;

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
                    backgroundColor: colour,
                    borderColor: 'rgb(255, 99, 132)',
                    data: reactor.data
                }]
            },
            // Configuration options go here
            options: {
                legend: {
                    display: false,
                },
                responsive: false,
                maintainAspectRatio: true,
                scales: {
                    yAxes: [{
                        scaleLabel: {
                            fontSize: 20,
                            display: true,
                            labelString: 'No. anitneutrinos per MeV per second'
                        },
                        ticks: {
                            fontSize: 10,
                            callback: function(value, index, values) {
                                return value.toExponential();
                            }
                        }
                    }],
                    xAxes: [{
                        scaleLabel: {
                            fontSize: 20,
                            display: true,
                            labelString: 'Energy level [MeV]'
                        },
                        ticks: {
                            fontSize: 10
                        }
                    }],
                }
            }
        });
    }
});