/* outdated, uso fetch
function get(url) {
    let req = new XMLHttpRequest;
    req.open("GET", url, false);
    req.send(null);
    return req.responseText;
}
*/


document.onreadystatechange = async function () {
    if (document.readyState == 'complete') {

        let btn = document.getElementById("btn");
        let overlay = document.getElementById("overlay");
        
        btn.addEventListener("click", function (){
            overlay.classList.add("hidden");
        })
        
        let links = fetch("e1test.json");
        links = await (await links).json();
        let menu = document.getElementById("menu-entry");
        for (var link of links) {
            let entry = document.createElement("li");
            entry.innerHTML = "<a href=" + link.link + ">" + link.desc + "</a>";
            menu.appendChild(entry);
        }

        
        let textbtn = document.getElementById("menu-txt");
        textbtn.addEventListener("click", function () {
            if (window.innerWidth < 600)
                menu.classList.toggle("hidden");
        })
    }
}