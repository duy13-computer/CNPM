document.addEventListener("DOMContentLoaded", function() {
    const btn = document.getElementById("alertButton");
    if (btn) {
        btn.addEventListener("click", function() {
            alert("Hello! Flask static JS is working 🚀");
        });
    }
});