function checkPrediction()
{

  $.get('/predict_one_hand', '', function(data, textStatus, jqXHR)
  {
  	return class_name;

  });
  
}




$(window).on('load',function()
{

    $( "#button" ).click(function()
    {
    
        var name = checkPrediction();
        if (name == undefined) 
        	name = "주륵";
        document.getElementById("answer").innerHTML = name;
        document.getElementById("answer").style.fontSize = "40px";
        document.getElementById("answer").style.position = "relative";
        document.getElementById("answer").style.top = "-1430px";



    });

});






