// JavaScript source code




function sendMessage()
{
    alert("send message");
};
function get_current() {
    console.log("getting current logged USER");
    $.getJSON("/current", function (data) {
        console.log("Current user is " + data['username'])
    });
}

function getMessages(user_from_id, user_to_id) {
    alert("getting messages")

}
function get_all_users() {
    console.log("voy a traer todos los usuarios");
    $.getJSON("/users", function (data){

        var i = 0;
        $.each(data, function () {

            user_to = data[i]['id'];
            e = '<div classs="alert" role="alert">';
            e = e + '<div>' + data[i]['username'] + '</div>';
            e = e + '</div>';
            i = i + 1;
            $("<div/>", { html: e }).appendTo("#users");
        });
    });

}