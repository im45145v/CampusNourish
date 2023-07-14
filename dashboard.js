document.getElementById('logoutForm').addEventListener('submit', function(event) {
    event.preventDefault();

    fetch('/logout', {
        method: 'POST'
    })
    .then(response => {
        window.location.href = '/login';
    })
    .catch(error => {
        console.error(error);
    });
});
