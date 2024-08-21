let main = document.querySelector('.main');
let test = document.querySelector('.test');
let profil = document.querySelector('#profil');
let back = document.querySelector('#back');

window.onload = function() {
    main.style.display = 'flex';
    test.style.display = 'none';
}

profil.addEventListener('click', function(event) {
    event.preventDefault();
    main.style.display = 'none';
    test.style.display = 'flex';
})

back.addEventListener('click', function() {
    event.preventDefault();
    main.style.display = 'flex';
    test.style.display = 'none';
})
