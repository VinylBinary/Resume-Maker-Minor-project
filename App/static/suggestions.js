let about = document.getElementById("aboutdiv");
let career = document.getElementById("careerdiv");
let education = document.getElementById("educationdiv");

function getSuggestions(event){
    const element = event.target;
    const text = element.innerText.trim();
    if(text !== "" && event.key !=="Tab"){
    fetchbody = {
        "field": element.id,
        "text": text
    }
    fetch('/generate-suggestions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(fetchbody)
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json()
    }).then((data)=>{
        suggest(element, data.request)
    }
    )}
    else{
        return
    }
}
function suggest(elem, text) {
    const existingSpan = elem.querySelector('span');
    
    if (existingSpan) {
        existingSpan.innerText = text;
    } else {
        elem.innerHTML += `<br><span>${text}</span>`;
    }
}

function useSuggestion(event){
    // elemid = event.target.id
    // elem = document.getElementById(elemid)
    elem = event.target
    console.log(elem)
    sp = elem.querySelector('span')
    if(sp){
    text = sp.innerText
    if (event.key === "Tab"){
        event.preventDefault();
        elem.innerText = text
        sp.remove()
    }}
    else{
        console.log("empty")
        return
    }
}
function updatetext() {
    el = [about, career, education];
    el.forEach((element) => {
        const divId = element.id;
        const textareaId = divId.replace('div', '');
        const textarea = document.getElementById(textareaId);
        console.log(textareaId)
        if (textarea) {
        textarea.value = element.innerText.trim();
        }
  })
}

function debounce(func, delay) {
    let timer;
    return function(event) {
        clearTimeout(timer);
        timer = setTimeout(() => func(event), delay);
    };
}

about.addEventListener("keyup", debounce(getSuggestions, 2000));
about.addEventListener("keydown", useSuggestion);
career.addEventListener("keyup", debounce(getSuggestions, 2000));
career.addEventListener("keydown", useSuggestion);
education.addEventListener("keyup", debounce(getSuggestions, 2000));
education.addEventListener("keydown", useSuggestion);