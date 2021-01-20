var video = $("#videoUpload")[0];
var spaceLeft = $("#remaining-storage").html() * 1024 * 1024;
var errorFlash = 
`<div class="form-row">
	<ul class="flashes">
		<li class="error">
		You have reached your maximum upload limit of 50MB, and this video cannot be uploaded.
		</li>
	</ul>
</div>`


$('#videoUpload').bind('change', function() {
	console.log('Video size: ' + this.files[0].size);
	console.log('Space Left: ' + spaceLeft)
	if (this.files[0].size > spaceLeft) {
		$('#video-upload-form').prepend(errorFlash);
		$('#submit-btn', this).attr('disabled', 'disabled');
		$('#video-upload-form').bind('submit',function(e){e.preventDefault();});
	} else {
		$('.flashes').remove();
		$('#submit-btn', this).removeAttr('disabled', 'disabled');
		$('#submit-btn').attr('disabled', false);
		$('#video-upload-form').unbind('submit');
	}
});