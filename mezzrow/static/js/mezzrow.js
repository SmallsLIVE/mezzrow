$(function() {
	$(".event").on("click", function() {
	  	var thisEventName = $(this).text(),
	  		thisEvent = $("div.event-details"),
	      	thisImg = $(this).attr("data-img"),
	      	thisDate = $(this).attr("data-date"),
	      	thisTime = $(this).attr("data-time"),
	      	thisPrice = $(this).attr("data-price");	      
	  $("dl").hide();
	  $("h2.frame-head").html(thisEventName);
	  $("img.event-img").attr("src", thisImg);
	  $("li.event-date").text("Date: " + thisDate);
	  $("li.event-time").text("Time: " + thisTime);
	  $("li.event-price").text("Price: " + thisPrice);
	  $("button.back").show();
	  $(thisEvent).attr("data-event", thisEventName)
	  $(thisEvent).show();
	});
	$(".back").on( "click", function() {
	  $("dl").show();
	  $("h2.frame-head").html("Performing this week");
	  $(".event-details").hide();
	  $("button.back").hide();
	});
});
