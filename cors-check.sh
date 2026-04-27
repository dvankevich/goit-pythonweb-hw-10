#!/bin/bash

echo "request from allowed domain"
curl -I -X OPTIONS http://localhost:8000/ \
     -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: GET"

echo "request from BAD domain"
curl -i -X OPTIONS http://localhost:8000/ \
     -H "Origin: https://mydomain.example.com" \
     -H "Access-Control-Request-Method: GET"
