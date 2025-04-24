document.addEventListener("DOMContentLoaded", function () {
    // Auto-dismiss alerts after 3 seconds
    const alerts = document.querySelectorAll('.alert');
    if (alerts) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.classList.remove('show');
                alert.classList.add('fade');
            });
        }, 3000);
    }

    // You can add form validation or confirmation here later
});
