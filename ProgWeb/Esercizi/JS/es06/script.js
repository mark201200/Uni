window.onload = function () {
    form = document.getElementById("myform");
    txtin = document.getElementById("txtin");
    dynlist = document.getElementById("dynlist");

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        let listEl = document.createElement("li");
        listEl.innerHTML = txtin.value;
        listEl.addEventListener("click", function (e) {
            e.target.remove();
        });
        dynlist.appendChild(listEl);
        txtin.value = "";
    });
}