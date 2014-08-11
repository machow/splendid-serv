$(document).ready(function(){

//Background spin 
  
  $('#enter').mouseenter(function(){
    $('#spinwrap').addClass('speedup');
    });
  
//Background stop spin

  $('#enter').mouseleave(function(){
    $('#spinwrap').removeClass('speedup');
  });

//get landing page
  $('#enter').click(function(){
    $.get( "/_/landing.html")
    .done(function( data ) {
      $('#boardframe').html(data );
    });
  });

//

//toggle p-lands display on .lands-container click
$('.lands-container').on('click',this,function(){
  
  $(this).next('p-lands').toggle();
  
  
})

  
});









