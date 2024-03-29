window.onload = function () {

    let btn = document.getElementById("btn");
    let overlay = document.getElementById("overlay");

    btn.addEventListener("click", function () {
        overlay.classList.add("hidden");
    })

    fetch("e1test.json")
        .then(links => {
            return links.json()
        })
        .then(links => {
            let menu = document.getElementById("menu-entry");
            for (var link of links) {
                let entry = document.createElement("li");
                entry.innerHTML = "<a href=" + link.link + ">" + link.desc + "</a>";
                menu.appendChild(entry);
            }
        })

    let textbtn = document.getElementById("menu-txt");
    textbtn.addEventListener("click", function () {
        if (window.innerWidth < 600)
            menu.classList.toggle("hidden");
    })
}