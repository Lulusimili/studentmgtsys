
// Get students for who are enrolled in selected module
$(document).ready(function() {
	$('.list-group-item').click(function() {
	    $('.active').not($(this)).removeClass('active');
		$(this).toggleClass("active");

		$("#edit-module").removeAttr('disabled');
		$("#remove-module").removeAttr('disabled');

		let getStudentsModuleID = $(this).data('moduleid');
		console.log(getStudentsModuleID)

		//Send Selected Module ID to fetch students enrolled in module
		$.ajax({
			type: 'post',
			url: '/get-selected-students',
			contentType: 'application/json; charset=utf-8',
			data: JSON.stringify({'id': getStudentsModuleID}),
			success: function (data) {
				$('#student-list-container').load(document.URL +  ' #student-list');

			}	
		});
	});
});


//Add Module
$('#add-module').click(function() {
	$('#addModuleForm').attr('action', '/add_module');
	$('#moduleID').removeAttr('disabled');
	$('#moduleID').val('');
	$('#moduleName').val('');
	$('#moduleLecturer').val('');
	$('#moduleCapacity').val('');
	$('#modal-submit-btn').html('Add Module');
	$('#staticBackdropLabel').html('Add Module');
}); 


//Delete Module
$(document).ready(function() {
    $("#remove-module").click(function(){
    	$("#remove-module").attr('disabled', 'disabled');
    	$("#edit-module").attr('disabled', 'disabled');
    	$('.list-group-item').each(function(){
	    	if ($(this).hasClass('active')) {
		     	let moduleID = $(this).data('moduleid');
				console.log(moduleID)

		    	$.ajax({
					type: 'post',
					url: '/module-remove',
					contentType: 'application/json; charset=utf-8',
					data: JSON.stringify({'id': moduleID}),
					success: function (data) {
				    	$('.list-group-item').each(function(){
	    					if ($(this).hasClass('active')) { 
	    						$(this).remove();
	    					}
	    				});
					}
				});   		
	    	}
	    }); 
	});
});

//Edit Module
$(document).ready(function() {
    $("#edit-module").click(function(){

    	$('#addModuleForm').attr('action', '/module_edit');
    	$('#moduleID').attr('readonly', 'readonly');
		$('#modal-submit-btn').html('Edit Module');
		$('#staticBackdropLabel').html('Edit Module');	
    	$('.list-group-item').each(function(){
	    	if ($(this).hasClass('active')) {
		     	let editModuleID = $(this).data('moduleid');
				console.log(editModuleID)

		    	$.ajax({
					type: 'post',
					url: '/select-module-edit',
					contentType: 'application/json; charset=utf-8',
					data: JSON.stringify({'id': editModuleID}),
					success: function (data) {
						$('#moduleID').val(editModuleID);
						$('#moduleName').val(data[0]);
						$('#moduleLecturer').val(data[1]);
						$('#moduleCapacity').val(data[2]);				
					}
				});   		
	    	}
	    }); 
	});
});