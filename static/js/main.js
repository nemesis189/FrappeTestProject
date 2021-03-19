
$(document).ready(function () {
  
  var dataTable = $('#book_table').DataTable();
  var dataTable1 = $('#member_data').DataTable();
  
  });


  $('.chosen-select').chosen({width: "95%"});

  function del(ID, title, pg){
    if ( confirm("Are you sure you want to delete '" + title + "'")){
      
        window.location.href = '/delete'+pg+'/' + ID;
    }
}
 


$(document).on('click', '#edit_but', function() {

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
     });



