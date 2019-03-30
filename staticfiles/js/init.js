$(document).ready(function(){
    $('.sidenav').sidenav();
    $('#notification-sidenav').sidenav({edge:'right'});
    $('#course-sidenav').sidenav();
    $('.dropdown-trigger').dropdown({
        coverTrigger:false
    });
    $('.modal').modal();
});

function closeNotificationSidenav() {
    $('#notification-sidenav').sidenav('close');
};

