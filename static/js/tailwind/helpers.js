document.addEventListener('DOMContentLoaded', function () {
    // Close toast
    document.querySelectorAll('[data-toast="close"]').forEach(function (element) {
        element.addEventListener('click', function () {
            this.closest('.toast').remove();
        });
    });

    // After 5 seconds toasts should remove from DOM
    document.querySelectorAll('.toast').forEach(function (element) {
        setTimeout(function () {
            if (element) {
                element.remove();
            }
        }, 5000);
    })
});