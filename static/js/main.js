
$(document).ready(function () {
  
  var dataTable = $('#book_table').dataTable({"autoWidth":false});
  var dataTable1 = $('#member_data').dataTable({"autoWidth":false});


$(document).on('click', '#delete_but', function() {
  if (confirm("Are you sure you want to delete '" + $(this).data('name') + "'"))
  {
      $.ajax({
        url: '/'+ $(this).data('class'),
        type: 'DELETE',
        data:{
          'id':$(this).data('id'),
        },
        success:function(response) {
          window.location.href = response.redirect
      }
        
    });
  }
});
});

$('.chosen-select').chosen({width: "95%"});

$(document).ready(function(){
setTimeout(function() {
    $('#flash-mess').delay(3200).fadeOut('fast');
}, 1000);
});

$(document).on('click','#import-frappe',function(){
  $('.loader').addClass('loader-active');
});

$(document).on('click', '#edit_but', function() {
if($(this).data('id')){
    var id1 = $(this).data('id');
    var author1 = $(this).data('author');
    var title1 = $(this).data('title');
    var isbn1 = $(this).data('isbn');
    var pages1 = $(this).data('page');
    var publisher1 = $(this).data('publisher');
    var stock1 = $(this).data('stock');
    
    $('.modal-body #updtxtidOLD').val(id1) ;
    $('.modal-body #updtxtid').val(id1) ;
    $('.modal-body #updtxtauthor').val(author1);
    $('.modal-body #updtxttitle').val(title1);
    $('.modal-body #updtxtisbn').val (isbn1);
    $('.modal-body #updtxtstock').val (stock1);
    $('.modal-body #updtxtpagenum').val(pages1);
    $('.modal-body #updtxtpubl').val (publisher1);
  }

if($(this).data('memid')){     
    var id1 =$(this).data('memid');
    var name1 =$(this).data('name');
    var email1 =$(this).data('email');
    var phone1 =$(this).data('phone');
    var fine1 =$(this).data('fine');

    $('.modal-body #updtxtmemIDOLD').val(id1) ;
    $('.modal-body #updtxtmemID').val(id1) ;
    $('.modal-body #updtxtname').val(name1);
    $('.modal-body #updtxtphone').val(phone1);
    $('.modal-body #updtxtemail').val(email1);
    $('.modal-body #updtxtfine').val (fine1);
  }

if($(this).data('transid')){     
    var id1 =$(this).data('transid') + '-ret';
    var title =$(this).data('title');
    var member =$(this).data('member');
    var radios = $('input:radio[name=transtype]');
    var query = '.modal-body select option[value="' + member + '"]'

    $('.modal-body #txtid').val(id1) ;
    $('.modal-body #txttitle').val(title) ;
    $(query).attr("selected",'selected');
    $(".modal-body #txtmember").trigger("chosen:updated");
    radios.filter('[value=return]').prop('checked', true);
    }



});



