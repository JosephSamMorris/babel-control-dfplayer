function vol() {
    local ip; ip=$1
    local level; level=$2

    curl -X POST http://$ip/sound/volume -d "$level" -H 'Content-Type: text/plain'
}

function light() {
    local ip; ip=$1
    local level; level=$2

    curl -X POST http://$ip/light/brightness -d "$level" -H 'Content-Type: text/plain'
}

function light_limit() {
    local ip; ip=$1
    local level; level=$2

    curl -X POST http://$ip/light/limit -d "$level" -H 'Content-Type: text/plain'
    curl -X POST http://$ip/light/limit/confirm -d "$level" -H 'Content-Type: text/plain'
}

function test_sound() {
    local ip; ip=$1

    vol "$ip" 100
    sleep 2
    vol "$ip" 0
}

function set_id() {
    local ip; ip=$1
    local id; id=$2

    curl -X POST http://$ip/control/offset -d "$id" -H 'Content-Type: text/plain'
}
