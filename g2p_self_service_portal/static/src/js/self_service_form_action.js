function getQueryParams(url) {
  const paramArr = url.slice(url.indexOf('?') + 1).split('&');
  const params = {};
  paramArr.map(param => {
      const [key, val] = param.split('=');
      params[key] = decodeURIComponent(val);
  })
  return params;
}

function showToast(message) {
  const toastMessage = document.querySelector('#toast-message');
  toastMessage.textContent = message;
  const toastContainer = document.querySelector('#toast-container');
  toastContainer.style.display = "block"
}

function hide_toast() {
  const toastContainer = document.querySelector('#toast-container');
  toastContainer.style.display = "none"
}


function form_submit_action(){

  //URL Change
  var test = $('.s_website_form')
  var form = test.find('form')
  var url = form[0].baseURI
  
  param = getQueryParams(url)['program_name'].split('#')[0]

  form[0].action = '/selfservice'
  form[0].action = form[0].action.concat('/submitted?program_name='+ param)


  // Validation's //
  count = 0;
  var required_fields = $('.s_website_form_required')

  for(let i=0; i<required_fields.length; i++){
    var required_input_field = required_fields.find($('.s_website_form_input'))[i]

    if(required_input_field.value == ''){
      var field_name = "Please enter " + required_input_field.name.toLowerCase()
      var error_message = '<div class="input-field-error-message">' + field_name + '</div>'
      required_input_field.style.borderColor = '#D32D2D'
      count = 1;
      showToast('Please update all mandatory fields');

      if(!required_fields.find($('.input-field-error-message'))[i]){
        required_input_field.insertAdjacentHTML('afterend', error_message);
      }
    }
    else{
      required_input_field.style.borderColor = '#E3E3E3';
      required_fields.find($('.input-field-error-message'))[i].style.display = "none"
    }
  }

  if(count == 0){
    form.submit()
  }

}
