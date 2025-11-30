const toggle = document.getElementById('qr-toggle');
const emailContainer = document.getElementById('email-container');

toggle.addEventListener('change', function() {
    if (this.checked) {
        emailContainer.style.display = 'block';
        document.getElementById('email').required = true;
    } else {
        emailContainer.style.display = 'none';
        document.getElementById('email').required = false;
    }
});