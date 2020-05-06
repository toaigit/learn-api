#!/bin/bash
curl -d '{"username":"toai1","password":"toai1pass"}' -H "Content-Type: application/json" -X POST http://debtest4:5000/api/v1/users
curl -d '{"username":"toai2","password":"toai2pass"}' -H "Content-Type: application/json" -X POST http://debtest4:5000/api/v1/users

