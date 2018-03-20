
google.charts.load('current',{'packages':['corechart']});
google.charts.load('current', {'packages':['table']});


function drawFromRequest(request,options,cls, elid){
            request.then(function(response){
                google.charts.load('current', {'packages':['corechart']}) ;
                google.charts.setOnLoadCallback(drawChart);

                function drawChart(){
                    var dt = new google.visualization.DataTable(response.data);
                    var view = new google.visualization.DataView(dt);
                    var chart = new cls(document.getElementById(elid));

                    try {
                        google.visualization.events.addListener(chart, 'ready', function () {
                        var button = document.getElementById(elid).nextElementSibling ;
                        button.setAttribute("href",chart.getImageURI());
                        button.innerHTML='<button>Download as png</button>' ;

                        });
                    }
                    catch(e){
                        console.log(e);
                    }

                    chart.draw(view, options) ;
                }
            })
}

function drawWithoutPng(request,options,cls, elid){
            request.then(function(response){
                google.charts.load('current', {'packages':['corechart']}) ;
                google.charts.setOnLoadCallback(drawChart);

                function drawChart(){
                    var dt = new google.visualization.DataTable(response.data);
                    var view = new google.visualization.DataView(dt);
                    var chart = new cls(document.getElementById(elid));


                    chart.draw(view, options) ;
                }
            })
}