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