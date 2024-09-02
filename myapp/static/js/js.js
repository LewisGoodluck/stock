document.addEventListener("DOMContentLoaded",function(){
    const searchInput = document.getElementById("search-input")
    const suggestionList = document.getElementById("suggestion")

    searchInput.addEventListener("input",function(){
        const query = searchInput.value;

        if (query.length < 2){
            suggestionList.innerHTML = ''
            return
        }
        fetch(`/searchSuggestion/q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            suggestionList.innerHTML = '';
            data.foreach(product=>{
                const li = document.createElement("li");
                li.textContent = product.name;
                suggestionList.appendChild(li)
            })
        })
        .catch(err=>console.log(err))
    })
})