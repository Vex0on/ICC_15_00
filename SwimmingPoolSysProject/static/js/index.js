const toTop = document.querySelector(".to-top");
const toBottom = document.querySelector(".to-bottom");

window.addEventListener("scroll", () => {
    if (window.pageYOffset > 400){
        toTop.classList.add("to-top-active");
        toBottom.classList.add("to-bottom-active");
    }
    else {
        toTop.classList.remove("to-top-active");
        toBottom.classList.remove("to-bottom-active");
    } 
})


const hamburger = document.querySelector(".hamburger");
const navBar = document.querySelector(".nav__list");
const nav = document.querySelector(".nav");

hamburger.addEventListener("click", () => {
    navBar.classList.toggle("nav__list__active");
    nav.classList.toggle("nav__active");
})