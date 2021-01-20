$('#passwordInput, #passwordInputRepeat').on('keyup', function () {
  if ($('#passwordInput').val() == $('#passwordInputRepeat').val()) {
    $('#form-message').html('Passwords Match').css('color', 'green');
  } else 
    $('#form-message').html('Passwords do not match').css('color', 'red');
});