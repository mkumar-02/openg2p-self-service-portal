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
  var test = $('.s_website_form')
  var form = test.find('form')
  var url = form[0].baseURI
  
  param = getQueryParams(url)['id']

  form[0].action = '/selfservice'

  form[0].action = form[0].action.concat('/submitted?id='+ param)

  console.log(form[0].action)
  form.submit()
}

function cancel_action(){
  let msg = confirm("The entered data will not be saved. Are you sure you want to discard the form?")
  if(msg){
    location.href = ("/selfservice/home")
  }
}


