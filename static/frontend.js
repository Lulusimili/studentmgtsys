$("#search-bar-input").keyup( () => {

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
$(document).ready( () =>  {
	$('#viewModules').click( () => {
		$('#student-list-container').hide();
		$('#student-btn').hide();
		$('#student-list-container').load(document.URL +  ' #student-list', () => {
			$('#module-header').show()
			$('.list-group-item').each( () => {
				if ($(this).hasClass('active')) {
					$(this).trigger('click');	
				}
			})
		});
	});
});


$(document).ready( () => {
	$('#viewStudents').click( () => {
		$('#student-list-container').load(document.URL +  ' #student-list', () => {
			$('#viewModules').removeClass('active');
			$(this).addClass('active');
			$('#module-header').hide();
			$('#student-list-container').show();
			$('#student-btn').show();
			$('#student-btn').html('Register New Student');

			$('.fullStudentList').each( () => {
				$(this).show();
			});

			$('.studentEnrollmentList').hide();
			$('.fullStudentList').css('display', 'all');

			$('.student-option-btn').each( () => {
				$(this).html('Edit Student');
			});				
		});

	});
});

$(document).on('click', '#student-btn', (e) => { 

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


$('#delete-student').click( () => {
	let selectedDeleteStudentID;
	$('.fullStudentList').each( () => {
		if ($(this).hasClass('activeStudentRow')) {
			selectedDeleteStudentID = $(this).attr('data');
			return selectedDeleteStudentID
		}	

	});

	$.ajax({
		type: 'post',
		url: '/delete-student',
		contentType: 'application/json; charset=utf-8',
		data: JSON.stringify({'id': selectedDeleteStudentID}),
		success: (data) => {
			$("#student-modal-close").trigger('click');
			$('.fullStudentList').each( () => {
				if ($(this).hasClass('activeStudentRow')) {
					$(this).remove();
				}	
			});

		}
	});		
})

$(document).ready( () => {

	$('#registerStudentForm').on('submit', (e) => {
		action = $(this).attr('action');
		console.log(action)
		$.ajax({
			type: 'post',
			url: action,
			data: $('#registerStudentForm').serialize(),
			success: (data) => {

	   			if (data['status'] == 'AlreadyExists') {
	   				alert('Student ID Already Exists.')
	   			};

	   			$('#student-modal-close').trigger('click');

   			 	if (data.length > 0) {
					$('#body-container').load(document.URL +  ' .rejected-items', () => {
						$('#rejectedModulesToggle').trigger('click');
					});
	   			};

				$('#student-list-container').load(document.URL +  ' #student-list', () => {
					$('#viewModules').removeClass('active');
					$(this).addClass('active');
					$('#module-header').hide();
					$('#student-list-container').show();
					$('#student-btn').html('Register New Student');

					$('.fullStudentList').each( () => {
						$(this).show();
					});

					$('.studentEnrollmentList').hide();
					$('.fullStudentList').css('display', 'all');

					$('.student-option-btn').each( () => {
						$(this).html('Edit Student');
					});				
				});
			}
		});
		
		e.preventDefault();

	});

});

//Search Ajax
$(document).ready( () => {

	$('#search-bar').on('submit', (e) => {
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
			success: (data) => {
				console.log(data);

				if (action == '/search-modules' && Object.keys(data).length > 0 ) {
					Object.keys(data).forEach((key,index) => {

			   			$('.list-group-item-action').each( () => {

			   				if ($(this).attr('data-moduleid') == key) {
			   					$(this).addClass('search-result');
			   				}
			   			}) 
					});

		   			$('.list-group-item-action').each( () => {
		   				if ($(this).hasClass('search-result')) {
		   					
		   				} else {
		   					$(this).hide();
		   				}
			   		}) 					
				} else {
					Object.keys(data).forEach( (key,index) => {
			   			$('.fullStudentList').each( () => {
			   				if ($(this).attr('data') == key) {
			   					$(this).addClass('search-result');
			   				}
			   			}) 
					});
		   			$('.fullStudentList').each( () => {
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

$('#rejectedModules-close').click( () => {
	$('#student-list-container').load(document.URL +  ' #student-list', () => {
		$('#viewModules').removeClass('active');
		$(this).addClass('active');
		$('#module-header').hide();
		$('#student-list-container').show();
		$('#student-btn').html('Register New Student');

		$('.fullStudentList').each(() => {
			$(this).show();
		});
		
		$('.studentEnrollmentList').hide();
		$('.fullStudentList').css('display', 'all');

		$('.student-option-btn').each(() => {
			$(this).html('Edit Student');
		});				
	});
})

//Selected Student on Student List
$(document).on('click', '.studentEnrollmentList', (e) => { 
	
	$('.studentEnrollmentList').not($(this)).removeClass('activeStudentRow');
	$(this).addClass("activeStudentRow");
	selectedStudentID = $(this).attr('data');

	$(this).find("button").click(() => {

		console.log(selectedStudentID);
		let getStudentsModuleID = '';
		$('.list-group-item').each(() => {
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
				success: (data) => {
					$('.studentEnrollmentList').each(() => {
						if ($(this).hasClass('activeStudentRow')) {
							$(this).remove();
						}	

					});
				}
			});
		}
	});

	$('.student-option-btn').attr('disabled', 'disabled');
	$(this).find("button").removeAttr('disabled');
	$('.student-option-btn').css('background-color', '#6c757d');
	$(this).find("button").css('background-color', 'orange');
	$(this).find("button").addClass('active')

});



//Selected Student on Student List
$(document).on('click', '.fullStudentList', (e) => { 
	
	$('.fullStudentList').not($(this)).removeClass('activeStudentRow');
	$(this).addClass("activeStudentRow");
	selectedStudentID = $(this).attr('data');

	$(this).find("button").attr('data-toggle', 'modal').click( () => {

		$.ajax({
			type: 'post',
			url: '/select-edit-students',
			contentType: 'application/json; charset=utf-8',
			data: JSON.stringify({'id': selectedStudentID}),
			success: (data) => {
				$('#studentID').val(selectedStudentID);
				$('#studentName').val(data[0]);
				$('#studentEmail').val(data[1]);
				$('.selectpicker').selectpicker('val', data[2]);
			}
		});
	});

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
});


// Get students for who are enrolled in selected module
$(document).ready( () => {
	$('.list-group-item').click( () => {
	    $('.active').not($(this)).removeClass('active');
		$(this).addClass("active");

		let getStudentsModuleID = $(this).data('moduleid');
		//Send Selected Module ID to fetch students enrolled in module
		$.ajax({
			type: 'post',
			url: '/get-selected-students',
			contentType: 'application/json; charset=utf-8',
			data: JSON.stringify({'id': getStudentsModuleID}),
			success: (data) => {
				$('#student-list-container').load(document.URL +  ' #student-list', () => {
					$('#module_container').css('min-height', '420px');
				});

			}	
		});

		$("#edit-module").removeAttr('disabled');
		$("#remove-module").removeAttr('disabled');
		$('#student-option-btn').html('Remove');
		$('#student-list-container').show();

	});
});


//Add Module
$('#add-module').click( () => {
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
$(document).ready( () => {
    $("#remove-module").click( () => {
    	$("#remove-module").attr('disabled', 'disabled');
    	$("#edit-module").attr('disabled', 'disabled');
    	$('.list-group-item').each(() => {
	    	if ($(this).hasClass('active')) {
		     	let moduleID = $(this).data('moduleid');
				console.log(moduleID)

		    	$.ajax({
					type: 'post',
					url: '/module-remove',
					contentType: 'application/json; charset=utf-8',
					data: JSON.stringify({'id': moduleID}),
					success: (data) => {
				    	$('.list-group-item').each( () => {
	    					if ($(this).hasClass('active')) { 
	    						$(this).remove();
	    						$('.list-group-item').each((index) => {
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
$(document).ready( () => {
    $("#edit-module").click( () => {

    	$('#addModuleForm').attr('action', '/module_edit');
    	$('#moduleID').attr('readonly', 'readonly');
		$('#modal-submit-btn').html('Edit Module');
		$('#staticBackdropLabel').html('Edit Module');	
    	$('.list-group-item').each( () => {
	    	if ($(this).hasClass('active')) {
		     	let editModuleID = $(this).data('moduleid');
				console.log(editModuleID)

		    	$.ajax({
					type: 'post',
					url: '/select-module-edit',
					contentType: 'application/json; charset=utf-8',
					data: JSON.stringify({'id': editModuleID}),
					success: (data) => {
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
