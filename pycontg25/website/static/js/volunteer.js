document.getElementById('volunteer-form').addEventListener('submit', function (e) {
    e.preventDefault();
    this.style.display = 'none';
    document.getElementById('volunteer-success').style.display = 'block';
    console.log('Volunteer form submitted');
});