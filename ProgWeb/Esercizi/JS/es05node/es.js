var http = require('http');

var server = http.createServer(function (req, res) {
    let path = req.url;
    if (path === '/') {
        res.end("Home");
    } else if (path === '/contatti') {
        res.end("Contatti");
    } else if (path === '/about') {
        res.end("About");
    } else if (path === '/test') {
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end('<h1>Heading</h1> <p>How!</p> <h2>Subheading</h2> <p>How!</p>');
    } else {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end("<h1> 404- NOT FOUND!! </h1>");
    }
}
);

server.listen(3000);
console.log('Il server è attivo e in ascolto su http://localhost:3000/');

//hello world

