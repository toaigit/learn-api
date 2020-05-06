#!/bin/bash

curl -d '{"productid":"3a3dc","productname":"iPhone 9","productdescription":"Apple iphone 9 Black","productcategory":"PHONE", "manufacturer":"APPL", "active":"yes"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1/products
curl -d '{"productid":"6a789","productname":"iPhone 11","productdescription":"Apple iphone 11 White","productcategory":"PHONE", "manufacturer":"APPL", "active":"yes"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1/products
curl -d '{"productid":"281b4","productname":"Samsung s20","productdescription":"Samsung Galaxy s20 BLue","productcategory":"PHONE", "manufacturer":"SAMS", "active":"yes"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1/products
curl -d '{"productid":"19ab7","productname":"Pixel 4","productdescription":"Google Pixel 4 Gray","productcategory":"PHONE", "manufacturer":"GOOL", "active":"yes"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/v1/products
