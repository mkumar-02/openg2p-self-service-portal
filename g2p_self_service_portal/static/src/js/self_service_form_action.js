function get_query_params(url) {
  const paramArr = url.slice(url.indexOf('?') + 1).split('&');
  const params = {};
  paramArr.map(param => {
      const [key, val] = param.split('=');
      params[key] = decodeURIComponent(val);
  })
  return params;
}

function show_toast(message) {
  const toast_message = document.querySelector('#toast-message');
  toast_message.textContent = message;
  const toast_container = document.querySelector('#toast-container');
  toast_container.style.display = "block"
}

function hide_toast() {
  const toast_container = document.querySelector('#toast-container');
  toast_container.style.display = "none"
}

function validate_email(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function validate_url(url) {
  const urlRegex = /^(ftp|http|https):\/\/[^ "]+$/;
  return urlRegex.test(url);
}


function form_submit_action(){

  //URL Change
  var test = $('.s_website_form')
  var form = test.find('form')
  var url = form[0].baseURI
  
  param = get_query_params(url)['program_name'].split('#')[0]

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
      show_toast('Please update all mandatory fields');

      if(!required_fields.find($('.input-field-error-message'))[i] == true){
        if(required_input_field.classList.contains('datetimepicker-input')){
          required_input_field.parentElement.insertAdjacentHTML('afterend', error_message);
        }
        else{
          required_input_field.insertAdjacentHTML('afterend', error_message);
        }
      }
      else{
        if(!required_fields.find($('.input-field-validation-message'))[i] == false){
          required_fields.find($('.input-field-validation-message'))[i].style.display = 'none'
        }
        required_fields.find($('.input-field-error-message'))[i].style.display = 'block'
        
      }
    }
    else{
      if(!required_fields.find($('.input-field-error-message'))[i] == false){
        required_input_field.style.borderColor = '#E3E3E3';
        required_fields.find($('.input-field-error-message'))[i].style.display = 'none'
      }
      if(required_input_field.type == 'email'){
        if(validate_email(required_input_field.value) == false){
          validation_message = '<div class="input-field-validation-message">Please enter a valid email address</div>'
          count = 1;
          required_input_field.style.borderColor = '#D32D2D';
          show_toast('Please update all mandatory fields');
          if(!required_fields.find($('.input-field-validation-message'))[i] == true){
            required_input_field.insertAdjacentHTML('afterend', validation_message);
          }
        }
      }
      else if(required_input_field.type == 'radio'){
        var radio_field_name = required_input_field.name;
        if(form[0].elements[radio_field_name].value == ''){
          field_name = "Please select " + required_input_field.name.toLowerCase()
          error_message = '<div class="input-field-error-message">' + field_name + '</div>'
          field_name = "Please enter " + required_input_field.name.toLowerCase()
          count = 1;
          required_input_field.style.borderColor = '#D32D2D';
          show_toast('Please update all mandatory fields');

          if(!required_fields.find($('.input-field-error-message'))[i] == true){
            required_fields[i].insertAdjacentHTML('beforeend', error_message);
          }
          else{
            required_fields.find($('.input-field-error-message'))[i].style.display = 'block'
          }
        }
      }

      else if(required_input_field.type == 'url'){
        if(validate_url(required_input_field.value) == false){
          validation_message = '<div class="input-field-validation-message">Please enter a valid url</div>'
          count = 1;
          show_toast('Please update all mandatory fields');
          required_input_field.style.borderColor = '#D32D2D';
          if(!required_fields.find($('.input-field-validation-message'))[i] == true){
            required_input_field.insertAdjacentHTML('afterend', validation_message);
          }
        }
      }
    }
  }

  if(count == 0){
    form.submit()
  }

}

function toggle_chat_bot(){
  var box = document.getElementById("chat-bot");
  if (box.style.display === "none") {
    box.style.display = "block";
  } else {
    box.style.display = "none";
  }
}
