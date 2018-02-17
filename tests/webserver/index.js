#!/usr/bin/node

const express = require("express");
const app = express();
const server = require("http").Server(app);
const io = require("socket.io")(server);

server.listen(3000,function(){
    console.log("Server started");

    app.use(express.static("./public"));

    io.on("connection",function(socket){
        const socketid = socket.id;
        console.log(`Connected : ${socketid}`);
        
        socket.on("stream",function(str){
            socket.broadcast.emit("stream",str);
        });

        socket.on("muka", function(nama){
            console.log(`Terdeteksi : ${nama}`);
            socket.broadcast.emit("muka", nama);
        });

        socket.on("denied",function(names){
            console.log(`Ditolak`);
            socket.broadcast.emit("denied", names);
        });

        socket.on("netral", function(name){
            console.log(`Netral`)
            socket.broadcast.emit("netral", name);
        })

        socket.on("lock", function(lock){
            console.log(`Lock`)
            socket.broadcast.emit("lock", lock)
        })
        
        socket.on("disconnect", function(){
			console.log(`Disconnected : ${socketid}`);
		});
		
    });

});
