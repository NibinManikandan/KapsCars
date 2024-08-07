document.addEventListener('DOMContentLoaded', function () {
    const sidebarItems = document.querySelectorAll('.sidebar-item');

    sidebarItems.forEach(item => {
        item.addEventListener('mouseenter', function () {
            item.style.backgroundColor = '#e0d4e4';
        });

        item.addEventListener('mouseleave', function () {
            item.style.backgroundColor = '#f3e8f0';
        });
    });
});
