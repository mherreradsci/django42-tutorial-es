// This code activates flatpickr on fields with the 'datetimefield' class
// when the document has loaded
window.addEventListener("DOMContentLoaded", function () {
    flatpickr(".datetimefield", {
        enableTime: true,
        enableSeconds: true,
        dateFormat: "Y-m-d H:i:S",
        time_24hr: true
    });
});
