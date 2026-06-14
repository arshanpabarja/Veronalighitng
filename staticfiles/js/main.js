
document.addEventListener('DOMContentLoaded', function () {
    const dropdowns = document.querySelectorAll('.category-dropdown');
    dropdowns.forEach(dropdown => {
        const menu = dropdown.querySelector('.dropdown-menu');
        dropdown.addEventListener('click', e => {
            e.stopPropagation();
            menu.classList.toggle('hidden');
        });
    });


    document.addEventListener('click', () => {
        document.querySelectorAll('.dropdown-menu').forEach(menu => {
            menu.classList.add('hidden');
        });
    });
});