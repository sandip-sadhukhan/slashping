const REMOVE_TOAST_DELAY = 5000;

const removeToastAfterDelay = (element, delay) => {
    setTimeout(function () {
        if (element) {
            element.remove();
        }
    }, delay);
};

document.addEventListener("htmx:load", function (event) {
    if (event.target && event.target.classList.contains('toast')) {
        removeToastAfterDelay(event.target, REMOVE_TOAST_DELAY);
    } else {
        event.target.querySelectorAll('.toast').forEach(function (element) {
            removeToastAfterDelay(element, REMOVE_TOAST_DELAY);
        });
    }

    // Close toast
    document.querySelectorAll('[data-toast="close"]').forEach(function (element) {
        element.addEventListener('click', function () {
            this.closest('.toast').remove();
        });
    });
});