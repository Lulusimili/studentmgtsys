$("#search-bar-input").keyup(function() {

    if (!this.value) {
    	if ($('#viewStudents').hasClass('active')){
        	$('#viewStudents').trigger('click');
    	} else {
    		$('#viewModules').trigger('click');
    	}
    }
});



$('#student-btn').show();
// Navigation Bar
$(document).ready(function() {
	$('#viewModules').click(function() {
		$('#module-header').show();
		$('#student-list-container').hide();
		location.reload();
		$('#student-btn').hide();
		$('#student-btn').html('HIDE');
	});
});

$(document).ready(function() {
	$('#dashboard').click(function() {
		location.reload();
	});
});

$(document).ready(function() {
	$('#viewStudents').removeClass('active');
	$(this).addClass('active');
	// $('#module-header').show();
	// $('#student-list-container').hide();
	// $('#module_container').css('min-height', 'calc(100vh - 450px)');
})


$(document).ready(function() {
	$('#viewStudents').click(function() {
		$('#student-list-container').load(document.URL +  ' #student-list', () => {
			$('#viewModules').removeClass('active');
			$(this).addClass('active');
			$('#module-header').hide();
			$('#student-list-container').show();
			$('#student-btn').show();
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
});

$(document).on('click', '#student-btn', function(e) { 
	console.log('click')
	$('#registerStudentForm').attr('action', '/register-student');
	$('#delete-student').hide();
	$('#studentID').removeAttr('readonly', '');
	$('#student-modal-button').html('Register Student');
	$('#student-options-modal-title').html('Register New Student');

	$('#studentID').val('');
	$('#studentName').val('');
	$('#studentEmail').val('');

	$('.selectpicker').selectpicker('deselectAll');
	$('.filter-option-inner-inner').html('No Modules Selected');
});


$('#delete-student').click(function() {
	let selectedDeleteStudentID;
	$('.fullStudentList').each(function() {
		if ($(this).hasClass('activeStudentRow')) {
			selectedDeleteStudentID = $(this).attr('data');
			return selectedDeleteStudentID
		}	

	});
	console.log(selectedDeleteStudentID)
	$.ajax({
		type: 'post',
		url: '/delete-student',
		contentType: 'application/json; charset=utf-8',
		data: JSON.stringify({'id': selectedDeleteStudentID}),
		success: function (data) {
			$("#student-modal-close").trigger('click');
			alert('Student has been deleted.');
			$('.fullStudentList').each(function() {
				if ($(this).hasClass('activeStudentRow')) {
					$(this).remove();
				}	

			});

		}
	});		
})

$(document).ready(function(){

	$('#registerStudentForm').on('submit',function (e) {
		action = $(this).attr('action');
		console.log(action)
		$.ajax({
			type: 'post',
			url: action,
			data: $('#registerStudentForm').serialize(),
			success: function (data) {
	   			if (data['status'] == 'AlreadyExists') {
	   				alert('Student ID Already Exists.')
	   			}

	   			$('#student-modal-close').trigger('click');
	   			 if (data.length > 0) {
					$('#body-container').load(document.URL +  ' .rejected-items', function() {
						$('#rejectedModulesToggle').trigger('click');
					});


	   			}

				$('#student-list-container').load(document.URL +  ' #student-list', () => {
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
			}
		});
		
		e.preventDefault();

	});

});

//Search Ajax
$(document).ready(function(){

	$('#search-bar').on('submit',function (e) {
		let action;

		if ($('#viewStudents').hasClass('active')) {
			$('#search-bar').attr('action', '/search-students');
			action = '/search-students'
		} 

		if ($('#viewModules').hasClass('active'))  {
			$('#search-bar').attr('action', '/search-modules');
			action = '/search-modules'
		}

		$.ajax({
			type: 'post',
			url: action,
			data: $('#search-bar').serialize(),
			success: function (data) {
				console.log(data);

	   			$('.list-group-item-action').each(function() {
   					$(this).removeClass('search-result');
   					$(this).show();
	   			})

	   			$('.fullStudentList').each(function() {
   					$(this).removeClass('search-result');
   					$(this).show();
	   			})

				if (action == '/search-modules' && Object.keys(data).length > 0 ) {
					Object.keys(data).forEach(function(key,index) {
			   			$('.list-group-item-action').each(function() {
			   				if ($(this).attr('data-moduleid') == key) {
			   					$(this).addClass('search-result');
			   				}
			   			}) 
					});
		   			$('.list-group-item-action').each(function() {
		   				if ($(this).hasClass('search-result')) {
		   					
		   				} else {
		   					$(this).hide();
		   				}
			   		}) 					
				} else {
					Object.keys(data).forEach(function(key,index) {
			   			$('.fullStudentList').each(function() {
			   				if ($(this).attr('data') == key) {
			   					$(this).addClass('search-result');
			   				}
			   			}) 
					});
		   			$('.fullStudentList').each(function() {
		   				if ($(this).hasClass('search-result')) {
		   					
		   				} else {
		   					$(this).hide();
		   				}
			   		}) 					
				}
			}
		});
		e.preventDefault();
	});
});

$('#rejectedModules-close').click(function() {
	$('#student-list-container').load(document.URL +  ' #student-list', () => {
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
})

//Selected Student on Student List
$(document).on('click', '.studentEnrollmentList', function(e) { 
	
	$('.studentEnrollmentList').not($(this)).removeClass('activeStudentRow');
	$(this).addClass("activeStudentRow");
	selectedStudentID = $(this).attr('data');
	$('.student-option-btn').attr('disabled', 'disabled');
	$(this).find("button").removeAttr('disabled');
	$('.student-option-btn').css('background-color', '#6c757d');
	$(this).find("button").css('background-color', 'orange');
	$(this).find("button").addClass('active')

	$(this).find("button").click(function() {

		console.log(selectedStudentID);
		let getStudentsModuleID = '';
		$('.list-group-item').each(function() {
			if ($(this).hasClass('active')) {
				getStudentsModuleID = $(this).data('moduleid');
				return getStudentsModuleID
			}
		})

		if (getStudentsModuleID.length == 0 ) {
			console.log(getStudentsModuleID.length, 'LENGTH OF ID');
			alert('Please select a module.');
		} else {
			$.ajax({
				type: 'post',
				url: '/remove-student-from-module',
				contentType: 'application/json; charset=utf-8',
				data: JSON.stringify({'moduleID': getStudentsModuleID, 'studentID': selectedStudentID}),
				success: function (data) {
					$('.studentEnrollmentList').each(function() {
						if ($(this).hasClass('activeStudentRow')) {
							$(this).remove();
						}	

					});
				}
			});
		}
	})

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
	$(this).find("button").attr('data-target', '#registerStudent');
	$(this).find("button").attr('data-toggle', 'modal');

	$('#registerStudentForm').attr('action', '/edit-student');
	$('#studentID').attr('readonly', 'readonly');
	$('#student-modal-button').html('Edit Student');
	$('#student-options-modal-title').html('Edit Student');
	$('#delete-student').show();

	$(this).find("button").attr('data-toggle', 'modal').click(function() {

		console.log('clickedddd')
		$.ajax({
			type: 'post',
			url: '/select-edit-students',
			contentType: 'application/json; charset=utf-8',
			data: JSON.stringify({'id': selectedStudentID}),
			success: function (data) {
				console.log(data);
				$('#studentID').val(selectedStudentID);
				$('#studentName').val(data[0]);
				$('#studentEmail').val(data[1]);
				$('.selectpicker').selectpicker('val', data[2]);
				// data[2].forEach(function(item) {
				// 	$('.selectpicker').selectpicker('val', item);
				// });
			}
		});	
	})
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
