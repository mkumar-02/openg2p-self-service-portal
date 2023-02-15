function func(){
  var test = $('.s_website_form')
  var form = test.find('form')

  form.submit()
}

function cancel_action(){
  let msg = confirm("The entered data will not be saved. Are you sure you want to discard the form?")
  if(msg){
    location.href = ("/")
  }
}