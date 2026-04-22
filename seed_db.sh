#!/bin/bash

# Базовий URL вашого API
API_URL="http://127.0.0.1:8000/contacts/"

TODAY=$(date +%Y-%m-%d)
NEXT_WEEK3=$(date -d "+3 days" +%Y-%m-%d)
NEXT_WEEK5=$(date -d "+5 days" +%Y-%m-%d)

contacts=(
    '{"first_name": "Fox", "last_name": "Mulder", "email": "mulder@fbi.gov", "phone": "555-78-09", "birthday": "1961-10-13", "additional_info": "The truth is out there"}'
    '{"first_name": "Dana", "last_name": "Scully", "email": "scully@fbi.gov", "phone": "555-78-10", "birthday": "1964-02-23", "additional_info": "Trust no one"}'
    '{"first_name": "Walter", "last_name": "Skinner", "email": "skinner@fbi.gov", "phone": "555-01-01", "birthday": "'$TODAY'", "additional_info": "Birthday is today!"}'
    '{"first_name": "Deep", "last_name": "Throat", "email": "dt@unknown.com", "phone": "000-00-00", "birthday": "'$NEXT_WEEK3'", "additional_info": "Birthday in 3 days"}'
    '{"first_name": "John", "last_name": "Doggett", "email": "doggett@fbi.gov", "phone": "555-99-88", "birthday": "'$NEXT_WEEK5'", "additional_info": "Birthday in 5 days"}'
)

for contact in "${contacts[@]}"; do
    echo "Додаємо: $(echo $contact | jq -r '.first_name') $(echo $contact | jq -r '.last_name')..."
    
    curl -X 'POST' \
        "$API_URL" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d "$contact" \
        -s -o /dev/null -w "Статус відповіді: %{http_code}\n"
done
