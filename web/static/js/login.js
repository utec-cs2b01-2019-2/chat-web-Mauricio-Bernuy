function login() {
    console.log("User Login");
    var username = $('#username').val();//getting username by id
    var password = $('#password').val();//getting password by id
    console.log("DATA input>", username, password);
    var credentials = { 'username': username, 'password': password };
    $.post({
        url: '/authenticate',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify(credentials),
        success: function (data) {
            var url = 'http://' + document.domain + ':' + location.port + '/';
            $(location).attr('href', url);
            console.log("Authenticated!");
            alert("Authenticated");
        },
        data: JSON.stringify(credentials)
    });
}