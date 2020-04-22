//Add Module
$(document).ready(function() {
	$('.list-group-item').click(function() {

	    $('.active').not($(this)).removeClass('active');
		$(this).toggleClass("active");

		let moduleID = $(this).data('moduleid');


		//Send Selected Module ID
		$.ajax({
			type: 'post',
			url: '/module-selected',
			data: moduleID,
			success: function (data) {
				console.log('posted');
			}	
		});
	});
});


//Delete Module
$(document).ready(function() {
    $("#remove-module").click(function(){

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

    	$('.list-group-item').each(function(){
	    	if ($(this).hasClass('active')) {
		     	let moduleID = $(this).data('moduleid');
				console.log(moduleID)

		    	$.ajax({
					type: 'post',
					url: '/module-edit',
					contentType: 'application/json; charset=utf-8',
					data: JSON.stringify({'id': moduleID}),
					success: function (data) {
						$('#moduleID').val(moduleID);
						$('#moduleName').val(data[0]);
						$('#moduleLecturer').val(data[1]);
						$('#moduleCapacity').val(data[2]);
					}
				});   		
	    	}
	    }); 
	});
});