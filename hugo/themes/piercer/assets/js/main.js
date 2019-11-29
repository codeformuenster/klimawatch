// Header
const header = document.querySelector('header');

window.addEventListener("load", () => {
    document.body.style.paddingTop = `${header.offsetHeight}px`;
});
