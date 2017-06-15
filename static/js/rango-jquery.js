$(document).ready(function(){
  // JQuery код
  $("#about-btn").click(function(event){
    alert("You clicked the button using JQuery!");
  });
  // для лайков в category.html
  $('#likes').click(function(){
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/rango/like_category/', {category_id: catid}, function(data){
      $('#like_count').html(data);
      $('#likes').hide();
      });
  });
});
