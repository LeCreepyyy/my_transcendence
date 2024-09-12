let pp = document.getElementById("pp-id");
let inputFile = document.getElementById("input-file");

inputFile.onchange = function(){
    pp.src = URL.createObjectURL(inputFile.files[0]);
}