var result;
var initialize = function(param) {
	result = param.toString();
};
var reloadPage = function() {
	location.reload();
};
var getAnswer = function(trueorfalse) {
	if (trueorfalse == result) {
		document.getElementById("answer").innerHTML = "Correct!";
		document.getElementById("True").disabled = true;
		document.getElementById("False").disabled = true;
		document.getElementById("Retry").style.visibility = "visible";
	}
	else {
		document.getElementById("answer").innerHTML = "Incorrect!";
		document.getElementById("True").disabled = true;
		document.getElementById("False").disabled = true;
		document.getElementById("Retry").style.visibility = "visible";
	}
};