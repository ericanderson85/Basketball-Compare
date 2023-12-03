// Cache the selected elements
const searchButton = document.getElementById('search-button');
const searchPath = document.getElementById('search-path');
const textBox = document.getElementById('text-box');

// Attach event listeners for searchButton
searchButton.addEventListener('mouseover', function () {
    searchPath.style.fill = '#FF1744';
});

searchButton.addEventListener('mouseout', function () {
    searchPath.style.fill = 'black';
});

textBox.addEventListener('focus', function () {
    this.placeholder = '';
});

textBox.addEventListener('blur', function () {
    this.placeholder = 'Search for a player';
});