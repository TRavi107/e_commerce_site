$(document).ready(function(){
    $('.like-form').submit(function(e){
      e.preventDefault()
      const post_id = $(this).attr('id')
      const likebtn = $(`.like-btn${post_id}`)
      const url = $(this).attr('action')
      $.ajax({
        type:'POST',
        url:url,
        data:{
          'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
          'id':post_id
        },
        success:function(response){
          likebtn.html(response.data.likes)
        },
        error:function(error){
          
        }
      })
    })

    
  })