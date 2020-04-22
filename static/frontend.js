// Toggle Selection between modules
$('.list-group-item').click(function() {

    $('.active').not($(this)).removeClass('active');
	$(this).toggleClass("active");

	let moduleID = $(this).data('moduleid');
	console.log(moduleID)

	$.ajax({
		type: 'post',
		url: '/module-selected',
		data: moduleID,
		success: function (data) {
			console.log('posted');
		}
	});

});