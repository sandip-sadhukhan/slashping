document.addEventListener('DOMContentLoaded', function () {
    // Close toast
    document.querySelectorAll('[data-toast="close"]').forEach(function (element) {
        element.addEventListener('click', function () {
            this.closest('.toast').remove();
        });
    });
});