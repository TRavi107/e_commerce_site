$(document).ready(function(){
    $("#like-count").click(function(e){
        e.preventDefault()
      const likes = document.getElementById('likes-text')
      $.ajax({
        url:$("#like-count").data('url'),
        method:'GET',
        success:function(response){
          likes.innerHTML =response.data.likes
        }
      })
    });
  })