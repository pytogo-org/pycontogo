
function selectFormat(element, format) {
    const formatCards = document.getElementsByClassName('format-card');
    for (let i = 0; i < formatCards.length; i++) {
        formatCards[i].classList.remove('selected');
    }

    element.classList.add('selected');
    document.getElementById('talk-format').value = format;
    document.getElementById('talk-format').required = true;
}

document.getElementById('s-technical').addEventListener('change', function () {
    const technicalDetails = document.getElementById('technical-details');
    if (this.checked) {
        technicalDetails.style.display = 'block';
    } else {
        technicalDetails.style.display = 'none';
    }
});

