$(function() {
    var url = "{% url 'home' %}"; 
    $("#search").autocomplete({
      source: url
    });
  });
  