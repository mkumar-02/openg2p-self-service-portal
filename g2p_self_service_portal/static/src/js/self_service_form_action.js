function getQueryParams(url) {
  const paramArr = url.slice(url.indexOf('?') + 1).split('&');
  const params = {};
  paramArr.map(param => {
      const [key, val] = param.split('=');
      params[key] = decodeURIComponent(val);
  })
  return params;
}

function submit_action(){

  // csrf token //
  const input_element = document.createElement("input");
  document.getElementsByClassName("o_mark_required")[0].appendChild(input_element)

  const type_attr = document.createAttribute("type")
  const name_attr = document.createAttribute("name")
  const value_attr = document.createAttribute("t-att-value")

  type_attr.value= "hidden"
  name_attr.value= "csrf_token"
  value_attr.value= "request.csrf_token()"

  var total_input_fields= document.getElementsByClassName("o_mark_required")[0].length

  document.getElementsByClassName("o_mark_required")[0][total_input_fields-1].setAttributeNode(type_attr)
  document.getElementsByClassName("o_mark_required")[0][total_input_fields-1].setAttributeNode(name_attr)
  document.getElementsByClassName("o_mark_required")[0][total_input_fields-1].setAttributeNode(value_attr)

  ///

  var test = $('.s_website_form')
  var form = test.find('form')
  var url = form[0].baseURI
  
  param = getQueryParams(url)['id']

  form[0].action = '/selfservice'

  form[0].action = form[0].action.concat('/submitted?id='+ param)

  ///

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


