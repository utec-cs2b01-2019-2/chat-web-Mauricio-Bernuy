// JavaScript source code

function sendMessage()
{
    alert("send message");

};

function get_current() {
    console.log("getting currently logged USER");
    $.ajax({
        url: '/current',
        type: 'GET',
        contentType: 'application/json',
        dataType: 'json',
        success: function (response) {
            var name = response['name'] + " " + response['fullname'];
            currentUserId = response['id']
            e = '<div class="alert alert-primary font-weight-bold" role="alert">';
            e = e + name + '<br>';
            e = e + '<a href="/logout" class="alert-link">-logout</a>'
            e = e + '</div>';
            $('#currentuser').append(e);
            get_all_users();
        },
        error: function (response) {
            alert(JSON.stringify(response))
        }
    });
}

function getMessages(user_from_id, user_to_id) {
    alert("getting messages")

}
function get_all_users(user_from_id) {
    console.log("voy a traer todos los usuarios");
    $.ajax({
        url: '/users',
        type: 'GET',
        contentType: 'application/json',
        dataType: 'json',
        success: function (response) {
            var i = 0;
            $.each(response, function () {
                f = '<div class="alert alert-secondary" role="alert" onclick=loadMessages(' + currentUserId + ',' + response[i].id + ') >';
                f = f + response[i].username;
                f = f + '</div>';
                i = i + 1;
                $('#users').append(f);
            });
        },
        error: function (response) {
            alert(JSON.stringify(response));
        }
    });

}