
$(document).ready(function () {
    alerts = document.querySelectorAll('[id^="success-alert"]')
    for (let i = 0; i < alerts.length; i++) {
        a = alerts[i].id
        $(`#${a}`).fadeTo(5000, 500).slideUp(500, function () {
            $(`#${a}`).slideUp(500);
        });
    }
});
