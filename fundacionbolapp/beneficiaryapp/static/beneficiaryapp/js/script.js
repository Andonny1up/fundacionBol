const searchSelect = document.getElementById("id_search_select");
const options = searchSelect.options;
const searchInput = document.getElementById("id_search_input");
const searchBtn = document.getElementById("id_btn_search")

console.log(options)

function confirmDelete() {
    return confirm('¿Esta seguro de que desea eliminar el registro?')
}

function confirmBaja() {
    return confirm('¿Esta seguro de que desea dar de baja a esta persona?')
}

function confirmFinalized() {
    return confirm('¿Dese cambiar el estado a finalizado?')
}
searchBtn.addEventListener("click",function () {
    searchInput.value = "";
    setTimeout(function() {
        searchInput.focus();
    }, 700);
})

searchSelect.addEventListener("focus", function(){
  searchInput.focus();
});


for (let i = 0; i < options.length; i++) {
  
}