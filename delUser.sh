#!/bin/bash
curl -d '{"username":"toai1"}' -H "Content-Type: application/json" -X DELETE http://debtest4:5000/api/v1/users
curl -d '{"username":"toaix"}' -H "Content-Type: application/json" -X DELETE http://debtest4:5000/api/v1/users

