

document.onreadystatechange = function () {
    if (document.readyState === 'complete') {

        function ranWidth() {
            let w = window.innerWidth;
            return Math.floor(Math.random() * w);
        }

        function ranHeight() {
            let h = window.innerHeight;
            return Math.floor(Math.random() * h);
        }

        console.log(ranWidth());

        let divs = document.getElementsByTagName("div");
        for (var div of divs) {
           div.onclick = function () {
                alert("div!");
           }
        }

        window.setInterval(function(){
           for (var div of divs) {
               div.style.position = "absolute";
               div.style.top = ranHeight() + "px";
               div.style.left = ranWidth() + "px";
               if (div.style.backgroundColor === "black") {
                   div.style.backgroundColor = "red";
               } else {
                   div.style.backgroundColor = "black";
               }
            }
           }, 5000);
    }
}

