var THRESHOLD = .7;
var movie_list = "";
var good_movies_json = "";
var bad_movies_json = "";
var recent_movies_json = "";
var sum = 0;
var count = 0;

function evaluateReviews(oldListJSON) {
	//extract each review
	// if review has high enough probability and is not neutral, then contribute it to the total
	// to contribute to totol: three coounts: # positive, # negative, total #
	var listJSON2 = oldListJSON.replace(/u'/g, "\'");
	var listJSON = listJSON2.replace(/'/g,"\"");
	var list = JSON.parse(listJSON);
	var num_positive_reviews=0;
	var num_negative_reviews=0;
	var num_neutral_reviews=0;
  for(var i = 0; i < list.length; i++) {
  	var review = list[i];
    var probability = review.probability;
	var label = review.label;
	var tweets = document.getElementById("tweets");
	var row = tweets.insertRow(i);
	var cell1 = row.insertCell(0);
	var cell2 = row.insertCell(1);
	var cell3 = row.insertCell(2);
	cell1.innerHTML = review.user_value;
	cell2.innerHTML = probability;
	cell3.innerHTML = label;
	if (probability > THRESHOLD) {
		if (label === '1') {
			row.classList.add("danger");
			num_negative_reviews++;
		} else if (label === '5') {
			row.classList.add("success");
			num_positive_reviews++;
		} else if (label === '3') {
			num_neutral_reviews++;
		}
	}
	}
if(num_positive_reviews!=0 && num_negative_reviews != 0) {
  var percent_positive = num_positive_reviews/(num_positive_reviews+num_negative_reviews);
	//console.log("" + (percent_positive * 100) + "%");
	curr = Math.round(percent_positive * 100);
	document.getElementById("twitter_rating").innerHTML = "Twitter Score: " + Math.round(percent_positive * 100) + "%";
} else {
	document.getElementById("twitter_rating").innerHTML = "Not enough twitter reviews to determine score :/";
}
	var salesData=[
	{label:"Blue", color:"#3366CC"},
	{label:"Red", color:"#DC3912"},
	{label:"Green", color:"#109618"}
	];

	var svg = d3.select("#sentiwordnet_rating").append("svg").attr("width", 250).attr("height", 250);

	svg.append("g").attr("id","salespie");
		
	gradPie.draw("salespie", randomData(), 130, 130, 100);

	function changeData(){
		gradPie.transition("salespie", randomData(), 160);
	}

	function randomData(){
		return salesData.map(function(d){ 
			if (d.label === "Blue"){
				return {label:d.label, value:num_neutral_reviews, color:d.color};
			} else if (d.label === "Red") {
				return {label:d.label, value:num_negative_reviews, color:d.color};
			} else if (d.label === "Green"){
				return {label:d.label, value:num_positive_reviews, color:d.color};
			}
		});
	}
}

function evaluateReview(review) {
	var probability = review.probability;
	var label = review.label;
	if (probability > THRESHOLD) {
		if (label === '1') {
			num_negative_reviews++;
		} else if (label === '5') {
			num_positive_reviews++;
		}
	}
}

//myFunction('[{"probability":".8","label":"1"},{"probability":".8","label":"5"}]');
//is there an api call to get json?
//how to display data besides a percent? Look like rotten tomatoes?


function loadJSON(callback, fileName) {

	var xobj = new XMLHttpRequest();
	xobj.overrideMimeType("application/json");
	xobj.open('GET', fileName, true);
	xobj.onreadystatechange = function () {
		if (xobj.readyState == 4 && xobj.status == "200") {

			// .open will NOT return a value but simply returns undefined in async mode so use a callback
			callback(xobj.responseText);

		}
	}
	xobj.send(null);

}



function loadJSONAverages(callback, fileName, movieName, score) {
	var xobj = new XMLHttpRequest();
	xobj.overrideMimeType("application/json");
	xobj.open('GET', fileName, true);
	xobj.onreadystatechange = function () {
		if (xobj.readyState == 4 && xobj.status == "200") {
			console.log("dfd" + xobj.responseText);

			// .open will NOT return a value but simply returns undefined in async mode so use a callback
			callback(xobj.responseText, movieName, score);

		}
	}
	xobj.send(null);

}

function evaluateReviewsAverages(oldListJSON, movieName, score) {
	//extract each review
	// if review has high enough probability and is not neutral, then contribute it to the total
	// to contribute to totol: three coounts: # positive, # negative, total #
	var listJSON2 = oldListJSON.replace(/u'/g, "\'");
	var listJSON = listJSON2.replace(/'/g,"\"");
	console.log("hello " + listJSON);
	var list;
	try{
        list=JSON.parse(response);
    }catch(e){
        //alert(e); //error in the above string(in this case,yes)!
    }
	var num_positive_reviews=0;
	var num_negative_reviews=0;
  for(var i = 0; i < list.length; i++) {
  	var review = list[i];
    var probability = review.probability;
	var label = review.label;
	if (probability > THRESHOLD) {
		if (label === '1') {
			num_negative_reviews++;
		} else if (label === '5') {
			num_positive_reviews++;
		}
	}
	}
if(num_positive_reviews!=0 && num_negative_reviews != 0) {
  var percent_positive = num_positive_reviews/(num_positive_reviews+num_negative_reviews);
	//console.log("" + (percent_positive * 100) + "%");
	twitter_score = Math.round(percent_positive * 100);
	document.getElementById("twitter_rating").innerHTML = "Twitter Score: " + Math.round(percent_positive * 100) + "%";
	console.log(movieName, score, twitter_score);
	sum = sum + Math.abs(score - twitter_score);
	count = count + 1;
	console.log("Avg diff: " + sum/count);
} 
}


function showAverages(json, movieName) {

}

function setGoodMovieList(moviesJSON) {
	good_movies_json = JSON.parse(moviesJSON);
}

function setBadMovieList(moviesJSON) {
	bad_movies_json = JSON.parse(moviesJSON);
}

function setRecentMovieList(moviesJSON) {
	recent_movies_json = JSON.parse(moviesJSON);
}

//returns rotten tomato score if exists, else -1
function checkContains(query) {

//getAveragesBad();

	for(var i = 0; i < good_movies_json.movies.length; i++) {
    	if(good_movies_json.movies[i].movie == query) {
    		return "good";
    	}
	}
	for(var i = 0; i < bad_movies_json.movies.length; i++) {
    	if(bad_movies_json.movies[i].movie == query) {
    		return "bad";
    	}
	}
	for(var i = 0; i < recent_movies_json.movies.length; i++) {
    	if(recent_movies_json.movies[i].movie == query) {
    		return "recent";
    	}
	}

	return "empty";
}

// Movie folder says which folder to look in: good, bad, or recent?
function getRottenTomatoesScore(movieFolder, query) {
	if (movieFolder == "good") {
		for(var i = 0; i < good_movies_json.movies.length; i++) {
    		if(good_movies_json.movies[i].movie == query) {
    			return good_movies_json.movies[i].score;
    		}
		}
	} else if (movieFolder =="bad") {

		for(var i = 0; i < bad_movies_json.movies.length; i++) {
    		if(bad_movies_json.movies[i].movie == query) {
    			return bad_movies_json.movies[i].score;
    		}
		}
	} else if (movieFolder == "recent"){
		for(var i = 0; i < recent_movies_json.movies.length; i++) {
    		if(recent_movies_json.movies[i].movie == query) {
    			return recent_movies_json.movies[i].score;
    	}
	}
	}
}


function searchMovie() {
	var movieName = document.getElementById("movieInput").value;
	document.getElementById("movie_name").innerHTML = "Movie Name: " + movieName;
	console.log(movieName);
	var folder = checkContains(movieName);
	if(folder === "empty") {
		document.getElementById("rotten_tomatoes_rating").innerHTML = "We don't have this movie on file!";
		document.getElementById("twitter_rating").innerHTML = "";
		//document.getElementById()
	} else {
		var score = getRottenTomatoesScore(folder, movieName)
		document.getElementById("rotten_tomatoes_rating").innerHTML = "Rotten Tomatoes Score: " + (score * 10) + "%";
		// Evaluate the rating from tweets

		loadJSON(evaluateReviews, "classification_output/" + folder + "/tweets/" + movieName.replace(/ /g,"_") + ".json");
		var sentiScore = getSentiScore(movieName);
		document.getElementById("sentiwordnet_rating").innerHTML = "Sentiwordnet Score: " + sentiScore;
	}
}

function getSentiScore(movieName){
	var rawFile = new XMLHttpRequest();
	var score = 0;
    rawFile.open("GET","sentiwordnet.txt", false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                var lines = allText.split('\n');
                for (var line=0; line<lines.length;line++){
                	if (lines[line].split(',')[0] == movieName){
                		score = lines[line].split(',')[1];
                	}
                }
                
            }
        }
    }
    rawFile.send(null);
    return score;
}

function toTitleCase(str)
{
    return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
}

var curr = 0;

function getAverages() {
	for(var i = 0; i < good_movies_json.movies.length; i++) {
		var movie = good_movies_json.movies[i].movie;
    	var rottenTomatoesScore = good_movies_json.movies[i].score * 10;
    	var folder = "good";
    	console.log("classification_output/" + folder + "/tweets/" + movie.replace(/ /g,"_") + ".json");
		
    	loadJSONAverages(evaluateReviewsAverages, "classification_output/" + folder + "/tweets/" + movie.replace(/ /g,"_").replace(/:/,"") + ".json", movie, rottenTomatoesScore);
	}
}

function getAveragesBad() {
	for(var i = 0; i < bad_movies_json.movies.length; i++) {
		var movie = bad_movies_json.movies[i].movie;
    	var rottenTomatoesScore = bad_movies_json.movies[i].score * 10;
    	var folder = "bad";
    	console.log("classification_output/" + folder + "/tweets/" + movie.replace(/ /g,"_") + ".json");
		
    	loadJSONAverages(evaluateReviewsAverages, "classification_output/" + folder + "/tweets/" + movie.replace(/ /g,"_").replace(/:/,"") + ".json", movie, rottenTomatoesScore);
	}
}

loadJSON(setGoodMovieList, "/classification_output/good/movies.json");
loadJSON(setBadMovieList, "/classification_output/bad/movies.json");
loadJSON(setRecentMovieList, "/classification_output/recent/movies.json");

