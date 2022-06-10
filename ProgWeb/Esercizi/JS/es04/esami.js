function get(url){
    let req = new XMLHttpRequest();
    req.open("GET",url,false);
    req.send(null);
    return req.responseText
}

document.onreadystatechange = function() {
    if (document.readyState === 'complete'){
        let esami = JSON.parse(get("esami.json"));
        let tabella = document.getElementById("t1");
    
        for (var esame of esami){
            let row = document.createElement("tr");
            row.insertCell(0).innerHTML = esame.esame;
            row.insertCell(1).innerHTML = esame.voto;
            tabella.appendChild(row);
        }
    
    }
}