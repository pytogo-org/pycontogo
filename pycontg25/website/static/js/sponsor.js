document.getElementById('sponsorship-level').addEventListener('change', function () {
    const specialOption = document.getElementById('special-option');
    const inkindOption = document.getElementById('inkind-option');

    specialOption.style.display = 'none';
    inkindOption.style.display = 'none';

    if (this.value === 'special') {
        specialOption.style.display = 'block';
    } else if (this.value === 'inkind') {
        inkindOption.style.display = 'block';
    }
});

document.getElementById('sponsor-form').addEventListener('submit', function (e) {
    e.preventDefault();


    this.style.display = 'none';
    document.getElementById('sponsor-success').style.display = 'block';

    console.log('Sponsorship form submitted');
});
