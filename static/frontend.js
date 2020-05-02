
// Navigation Bar
$(document).ready(function() {
	$('#viewModules').click(function() {
		$('#viewStudents').removeClass('active');
		$(this).addClass('active');
		$('#module-header').show();
		$('#student-list-container').hide();
		$('#module_container').css('min-height', 'calc(100vh - 450px)');
	});
});

$(document).ready(function() {
	$('#dashboard').click(function() {
		location.reload();
	});
});


$(document).ready(function() {
	$('#viewStudents').click(function() {
		$('#viewModules').removeClass('active');
		$(this).addClass('active');
		$('#module-header').hide();
		$('#student-list-container').show();
		$('#student-btn').html('Register New Student');

		$('.fullStudentList').each(function() {
			$(this).show();
		});
		

		$('.studentEnrollmentList').hide();
		$('.fullStudentList').css('display', 'all');



		$('.student-option-btn').each(function() {
			$(this).html('Edit Student');
		});

	});
});



//Selected Student on Student List
$(document).on('click', '.studentEnrollmentList', function(e) { 
	
	$('.studentEnrollmentList').not($(this)).removeClass('activeStudentRow');
	$(this).addClass("activeStudentRow");
	selectedStudentID = $(this).attr('data');
	$('.student-option-btn').attr('disabled', 'disabled');
	$(this).find("button").removeAttr('disabled');
	$('.student-option-btn').css('background-color', '#6c757d');
	$(this).find("button").css('background-color', 'orange');

});

//Selected Student on Student List
$(document).on('click', '.fullStudentList', function(e) { 
	
	$('.fullStudentList').not($(this)).removeClass('activeStudentRow');
	$(this).addClass("activeStudentRow");
	selectedStudentID = $(this).attr('data');
	$('.student-option-btn').attr('disabled', 'disabled');
	$(this).find("button").removeAttr('disabled');
	$('.student-option-btn').css('background-color', '#6c757d');
	$(this).find("button").css('background-color', 'orange');

});


// Get students for who are enrolled in selected module
$(document).ready(function() {
	$('.list-group-item').click(function() {
	    $('.active').not($(this)).removeClass('active');
		$(this).addClass("active");

		$("#edit-module").removeAttr('disabled');
		$("#remove-module").removeAttr('disabled');

		$('#student-btn').html('Add Student');
		$('#student-option-btn').html('Remove');


		$('#module_container').css('min-height', '420px');
		$('#student-list-container').show();

		let getStudentsModuleID = $(this).data('moduleid');
		console.log(getStudentsModuleID)
		$('#small-moduleID').html(getStudentsModuleID);

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
	    						$('.list-group-item').each(function(index){
    							    if (index === $('.list-group-item').length - 1) {
		    							$(this).trigger('click');
		    							$(this).addClass('active');
									}
	    						});
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