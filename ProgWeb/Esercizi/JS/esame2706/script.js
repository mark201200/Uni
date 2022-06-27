

window.onload = function () {
    let colorchg = document.querySelector("#colorchg");
    colorchg.addEventListener("click", async function (e) {
        e.preventDefault();
        let res = await fetch("data.json");
        let res_json = await res.json();
        document.querySelector("body").style.backgroundColor = res_json.background;
        let as = document.querySelectorAll("a");
        for (a of as)
            a.style.color = "#ACC18A";

    });

    let confa = document.querySelector("#confa");
    confa.addEventListener("click", function (e) {
        e.preventDefault();
        document.querySelector(".menu").classList.toggle("rshift");
    });

    let confb = document.querySelector("#confb");
    confb.addEventListener("click", function (e) {
        e.preventDefault();
        let title = document.querySelector("header h1");
        title.style.margin = "auto auto auto 50%"
        let timer = setInterval(function () {
            title.style.margin = "0";
        }, 3000);

    });
}