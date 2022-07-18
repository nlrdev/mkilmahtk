$(function () {
  $("#auth_form").on("submit", function (event) {
    event.preventDefault();
    email =  $('input[name="email"]').val();
    password =  $('input[name="password"]').val();
    if (email == "" || password == "") {
      alert("Please fill out all the fields");
    } else {
      $.ajax({
        type: "POST",
        data: {
          email:  email,
          password: password,
          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').attr(
            "value"
          ),
        },
        dataType: "json",
        error: function (request, error) {
          console.log(arguments);
          console.log(" Can't do because: " + error);
        },
        success: function (data) {
          if (data.authenticated == 'True'){
            window.location.replace("http://silimasoftware.localhost/dashboard/");   
          }
          else if(data.blocked == "True"){
            window.location.replace("http://silimasoftware.localhost/auth/");
          }
          else{
            $("#msg_queue").append(data.msg_list);
          }
        },
      });
    }
  });
});