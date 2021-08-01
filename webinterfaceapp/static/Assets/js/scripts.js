$(document).ready(function () {
    var timer, delay = 5000; //5000 milisec.
    myFunction();
    $('#crawl').click(function () {
        alert("Reached Here")
        myFunction();
        // setInterval(function ()
        // {
        //     $.ajax({
        //         url: 'GetWebCrawlerStatus/',
        //         success: function (data) {
        //             alert("In");
        //             var res = data;
        //             console.log("data: " + data);
        //             //alert("data: " + data);
        //
        //         }
        //     });
        //
        // }, delay);
    });

    function myFunction() {
        setInterval(function () {
            $.ajax({
                url: 'GetWebCrawlerStatus/',
                success: function (data) {
                    //alert("In");
                    var res = data;
                    console.log("data: " + data);
                    //Appending to table...................
                    //alert("data: " + data);
                    //StopCrawler(bool);
                }
            });
            console.log("Hello");
        }, 5000);
    }

    $('#btnCrawlStop').click(function () {
        clearInterval(timer);
        //StopCrawler(bool);
    });

    function StopCrawler(checker)
    {
        if(!checker)
            clearInterval(timer);
    }

    function SelectCheck(nameSelect)
    {
        var OptionValue = document.getElementById("select_box").value;
        console.log(nameSelect);
        console.log(OptionValue);


        if(OptionValue == 1){
             document.getElementById("twitter-selected").style.display = "block";
        }
        else{
             document.getElementById("twitter-selected").style.display = "none";
         }
    }


});



