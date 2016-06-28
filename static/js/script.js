$(document).ready(function() {

	var isValid = function() {
		$(this).toggleClass('hascontent', $(this).val() != '');
	};
	$('#signup-page input').change(isValid);
	$('#signup-page input').keyup(isValid);
	$('#signup-page input').mouseup(isValid);
	$('#signup-page select').change(isValid);
	$('#signup-page select').keyup(isValid);
	$('#signup-page select').mouseup(isValid);

	// Center Login
	$(".main").css({
		'position' : 'absolute',
		'left' : '50%',
		'top' : '50%',
		'margin-left' : -$('.main').width()/2,
		'margin-top' : -$('.main').height()/2
	});
	// Center Forgot-card
	$(".forgot-card").css({
		'position' : 'absolute',
		'left' : '50%',
		'top' : '50%',
		'margin-left' : -$('.main').width()/2,
		'margin-top' : -$('.main').height()/2,
	});

	$('.signup-link').click(function() {
		$('.signup-link').removeClass('signup-inactive');
		$('.login-link').addClass('login-inactive');
		$('.login-view').hide();
		$('.signup-view').fadeIn('slow');
	});

	$('.login-link').click(function() {
		$('.signup-link').addClass('signup-inactive');
		$('.login-link').removeClass('login-inactive');
		$('.login-view').fadeIn('slow');
		$('.signup-view').hide();
	});
});

function animateCard(x){
	if (x == 0 ){
		$(".forgot-card").fadeIn();
		$(".black-overlay").fadeIn();
	} else if (x == 1){
		$(".sign-up-box").fadeIn();
		$(".black-overlay").fadeIn();
	}
}

function animateCardOut(x){
	if (x == 0){
		$(".forgot-card").fadeOut();
		$(".black-overlay").fadeOut();
	}
	if (x == 1) {
		$(".sign-up-box").fadeOut();
		$(".black-overlay").fadeOut();
	}
}
