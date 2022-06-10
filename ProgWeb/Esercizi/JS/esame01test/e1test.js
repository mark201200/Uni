function get(url) {
    let req = new XMLHttpRequest;
    req.open("GET", url, false);
    req.send(null);
    return req.responseText;
}

document.onreadystatechange = function () {
    if (document.readyState == 'complete') {

        let btn = document.getElementById("btn");
        btn.onclick = function () {
            document.getElementById("overlay").style.display = 'none';
        }

        let links = JSON.parse(get("e1test.json"));
        let menu = document.getElementById("menu-entry");
        for (var link of links) {
            let entry = document.createElement("li");
            entry.innerHTML = "<a href=" + link.link + ">" + link.desc + "</a>";
            menu.appendChild(entry);
        }

        if (window.innerWidth < 600) {
            let btn = document.getElementById("menu-txt");
            let menu = document.getElementById("menu-entry");
            btn.onclick = function () {
                if (menu.style.display != 'none')
                    menu.style.display = 'none';
                else menu.style.display = 'block';
            }
        }
    }
}