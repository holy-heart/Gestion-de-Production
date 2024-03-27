function addvar(){
    o++
    var cont = document.getElementById("var")
    var input = document.createElement("input")
    input.type= "text"
    input.name=String(i)
    cont.appendChild(input)
}

function addatt(){
    p++
    var cont = document.getElementById("att")
    var input = document.createElement("input")
    input.type= "text"
    input.name=String(i)
    cont.appendChild(input)
}