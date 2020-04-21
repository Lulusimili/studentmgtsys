$('.list-group-item').click(function() {
    $('.active').not($(this)).removeClass('active');
	$(this).toggleClass("active");
});