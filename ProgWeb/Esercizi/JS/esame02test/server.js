
const http = require('http');
const fs = require('fs');
const PORT = 8080;

let server = http.createServer(function (req, res) {
    let path = req.url;
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.writeHead(200, { "Access-Control-Allow-Origin": "*" });
    if (path === '/data') {
        fs.readFile("lista.json", function (err, data) {
            res.end(data);
        });
    } else {
        fs.readFile("err.json", function (err, data) {
            res.end(data);
        });
    }

});

server.listen(PORT);
console.log("Server is up on port " + PORT);
