function getQueryParams(url) {
  const paramArr = url.slice(url.indexOf('?') + 1).split('&');
  const params = {};
  paramArr.map(param => {
      const [key, val] = param.split('=');
      params[key] = decodeURIComponent(val);
  })
  return params;
}

function form_submit_action(){

  var test = $('.s_website_form')
  var form = test.find('form')
  var url = form[0].baseURI
  
  param = getQueryParams(url)['program_name'].split('#')[0]

  form[0].action = '/selfservice'
  form[0].action = form[0].action.concat('/submitted?program_name='+ param)

  count = 0;
  var required_field= $('.s_website_form_required')

  for(let i=0; i<required_field.length; i++){
    var required_input_field= required_field.find($('.s_website_form_input'))[i]

    if(required_input_field.value == ''){
      alert("Please update all mandantory fields");
      required_input_field.style.borderColor= '#D32D2D'
      required_input_field.reportValidity();
      count = 1;
      break;
    }
  }
  if(count==0){
    form.submit()
  }

}


