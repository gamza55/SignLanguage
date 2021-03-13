function checkPrediction()
{
	$.get('/predict_two_hand', function(data) {
		var answer;
  		//setTimeout(function() {return temp;}, 6001);
  		if (data.hasData) {
  			answer=data.temp;
  		}
  		else
  			answer="왜이러는데"
  		alert(answer);
        });

}

  





$(window).on('load',function()
{

    $( "#button" ).click(function()
    {
        document.getElementById("answer").innerHTML = "입력 중 ...";
        document.getElementById("answer").style.fontSize = "40px";
        document.getElementById("answer").style.position = "relative";
        document.getElementById("answer").style.top = "-1430px";
        

    
        var name = checkPrediction();
        
        //alert(name);
        //setTimeout(function() {alert(name)}, 6500);
        setTimeout(function(){
        
        	if (name == undefined) 
        		name = "주륵";
        	else {
        		document.getElementById("answer").innerHTML = name;
        		document.getElementById("answer").style.fontSize = "40px";
        		document.getElementById("answer").style.position = "relative";
        		document.getElementById("answer").style.top = "-1430px";
        	}
        	
  
        }, 6500);


    });

});





