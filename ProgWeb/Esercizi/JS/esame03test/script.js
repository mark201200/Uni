window.onload = function () {

    let contentdiv = document.getElementById("content");

    document.getElementById("menutxt").addEventListener("click", function () {
        if (window.innerWidth < 1000)
            document.getElementById("menu").classList.toggle("hidden");
    });

    document.getElementById("articolitxt").addEventListener("click", function () {
        let arr = [1, 2, 3];
        let i = 0;
        arr.sort(() => Math.random() - 0.5);
        sections = contentdiv.getElementsByTagName("section");
        for (section of sections) {
            section.style.order = arr[i++];
        }
    });

    fetch("data.json")
        .then(response => {
            return response.json()
        })
        .then(data => {
            for (element of data) {
                let section = document.createElement("section");
                section.innerHTML = "<h2>" + element.titolo + "</h2> " + element.contenuto;
                contentdiv.appendChild(section);
            }
        })
}