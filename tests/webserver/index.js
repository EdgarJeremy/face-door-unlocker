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
			console.log(str);
            socket.broadcast.emit("stream",str);
        });
        
        socket.on("disconnect", function(){
			console.log(`Disconnected : ${socketid}`);
		});
		
    });

});
