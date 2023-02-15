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


n =  new Date();
const month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
];

y = n.getFullYear();
m_name = month_names[n.getMonth()];
m = n.getMonth()+1;
d = n.getDate();

function modify_number(x){
  x = x.toString();
  if(x.length == 1){
    return ('0'+ x);
  }
  else{
    return x;
  }
}

document.getElementById("date").innerHTML = modify_number(d) + "-" + m_name + "-" + y;

document.getElementById("application_id").innerHTML = modify_number(d)+ modify_number(m)+ y.toString()[2]+ y.toString()[3]+ (Math.floor(Math.random() * 100000) + 1);