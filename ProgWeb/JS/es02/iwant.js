
document.onreadystatechange = function () {
    if (document.readyState === 'complete') {
        let n = 1;
        let button = document.getElementById('b1');
        let ul = document.getElementById('ul1');
        button.onclick = function () {
            let newElement = document.createElement('li');
            newElement.innerHTML = 'Elemento nuovo num ' + n ;
            n++;
            ul.appendChild(newElement);
        }
    }
};