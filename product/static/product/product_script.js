 // ============= Delte SEO items 

 var globalId = '';
 var globalOperation = '';
 var isError = false;
 
   function showDeleteModal(paramId, paramOperation) {
     $('#delete_modal').appendTo("body").modal('show');
     console.log('insdie the showDeleteModal');
     console.log(paramId);
     console.log(paramOperation);
     globalId = paramId;
     globalOperation = paramOperation;
   }
 
   function submitDeleteConfirmation() {
     $('#delete_modal').appendTo("body").modal('hide');
     var theTable = $('#' + globalOperation + '_table1').DataTable();
     console.log('value of csrftoken')
     console.log(csrftoken)
     console.log('valeu fo arguments')
     console.log(globalId);
     console.log(globalOperation);
     console.log('//////')
     console.log(theUrl);
 
     if (globalId == '' || globalId == null || globalOperation == '' || globalOperation == null) {
       isError = true
     } else {
       isError = false
     }
 
     if (isError) {
       console.log('yes there is error');
       isError = false;
       // $('#add_custom_schedule_button').text('Save Changes');
     } else {
       const fd = new FormData();
       fd.append('csrfmiddlewaretoken', csrftoken);
       fd.append('the_id', globalId);
       fd.append('operation', globalOperation);
       $.ajax({
         type: 'POST',
         url: theUrl,
         data: fd,
         success: function(response) {
           console.log('value of response');
           console.log(response);
           if (!response.is_error) {
             theTable.row($('#' + globalOperation + '_' + globalId)).remove().draw();
               globalId = '';
               globalOperation = '';
           } else {
             console.log('do not do anything');
           }
           $('#delete_modal').appendTo("body").modal('hide');
         },
         error: function(error) {
           console.log('error submitting by modal ================', error);
           $('#delete_modal').appendTo("body").modal('hide');
         },
         cache: false,
         contentType: false,
         processData: false,
       });
     }
   }