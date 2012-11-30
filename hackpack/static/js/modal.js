$(document).ready(function() {
	$('#windowTitleDialog').bind('show', function () {
		document.getElementById ("xlInput").value = document.title;
		});
	});
function closeDialog () {
	$('#windowTitleDialog').modal('hide'); 
	};
function okClicked () {
	document.title = document.getElementById ("xlInput").value;
	closeDialog ();
	};
