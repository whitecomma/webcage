$(document).ready(function() {
	$('#arch').click(function() {
		$('#navul li').removeClass('active');
		$(this).addClass('active');
		$.get('/archive.ajax', function(data) {
			$('main section').html(data);
		});
		//window.location = '/archive.ajax'
	});

	$('#about').click(function() {
		$('#navul li').removeClass('active');
		$(this).addClass('active');
		$.get('/about.ajax', function(data) {
			$('main section').html(data);
		});
	});

	$('#upf').click(function() {
		$('#navul li').removeClass('active');
		$(this).addClass('active');
		$.get('/upfile.ajax', function(data) {
			$('main section').html(data);
		});
	});

	//$('#eva').click(function() {
	//	$('#navul li').removeClass('active');
	//	$(this).addClass('active');
	//	$.get('/eval.ajax', function(data) {
	//		$('main section').html(data);
	//	});
	//});
	
	$('#frm_upf').submit(function(e) {
		e.preventDefault();
		var formdata = new FormData(this);
		$.ajax({
			type: 'POST',
			url: '/upfile.ajax',
			data: formdata,
			contentType: false,
			processData: false
		}).then(function(data) {
			$('main section').html(data);
		});
	});



	
});