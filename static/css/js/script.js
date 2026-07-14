
const navbar = document.getElementById("navbar");

const navbar = document.getElementById("navbar");

// Check if we are on the home page
const isHomePage = window.location.pathname === "/";

if (isHomePage) {

    window.addEventListener("scroll", function () {

        if (window.scrollY > 50) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }

    });

} else {

    // For prediction and other pages
    navbar.classList.add("scrolled");

}



function animateValue(id, target, suffix) {

    const element = document.getElementById(id);

    let current = 0;

    const increment = target / 100;

    function update() {

        current += increment;

        if (current >= target) {
            current = target;
        }

        if (suffix === "%") {
            element.textContent = current.toFixed(2) + "%";
        } else {
            element.textContent = current.toFixed(2);
        }

        if (current < target) {
            requestAnimationFrame(update);
        }

    }

    update();

}

document.addEventListener("DOMContentLoaded", function () {

    animateValue("accuracy-number", 85.85, "%");
    animateValue("roc-number", 0.91, "");

});



const observer = new IntersectionObserver((entries)=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.classList.add("show");

        }

    });

});

document.querySelectorAll(".timeline-item").forEach(item=>{

    item.classList.add("hidden");

    observer.observe(item);

});


