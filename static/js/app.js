// Fade animation
document.addEventListener("DOMContentLoaded", () => {

    document.body.classList.add("loaded");

});

// Loading Screen
const forms = document.querySelectorAll("form");

forms.forEach(form => {

    form.addEventListener("submit", () => {

        const loader = document.getElementById("loader");

        if(loader){

            loader.style.display="flex";

        }

    });

});

// Ripple Effect

document.querySelectorAll("button").forEach(button=>{

button.addEventListener("click",function(e){

const circle=document.createElement("span");

const diameter=Math.max(this.clientWidth,this.clientHeight);

const radius=diameter/2;

circle.style.width=circle.style.height=`${diameter}px`;

circle.style.left=`${e.clientX-this.offsetLeft-radius}px`;

circle.style.top=`${e.clientY-this.offsetTop-radius}px`;

circle.classList.add("ripple");

const ripple=this.getElementsByClassName("ripple")[0];

if(ripple){

ripple.remove();

}

this.appendChild(circle);

});

});
function showSection(sectionId) {

    // Hide all sections
    document.getElementById("home").style.display = "none";
    document.getElementById("features").style.display = "none";
    document.getElementById("about").style.display = "none";
    document.getElementById("contact").style.display = "none";

    // Show the selected section
    document.getElementById(sectionId).style.display = "block";
}