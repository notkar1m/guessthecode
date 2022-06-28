
var trueLang = ""
var trueLangId = ""
var lost = false
function hide(id){
    document.getElementById(id).style.display = "none"
}
function show(id){
    document.getElementById(id).style.display = "block"
}
function requestApi(){
    fetch(`/api`, {
        method: "GET"
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`);
        }
        return response.json()
      })
      .then((data) => {
        for(i in [0,1,2,3]){
            document.getElementById(i).disabled = false
        }
        trueLang = data['c']
        for(i in data['langs']){
            if(data['langs'][i] == trueLang){
                trueLangId = `${i}`
            }
            document.getElementById(`${i}`).innerText = data['langs'][i]
        }
        let container = document.getElementById("code-block")
        container.className = "language-" + data['c']
        container.textContent = data['code']
        if(data['c'] != "JSON"){
            hljs.highlightAll()
        }

    })
      .catch(error => {
        console.log("ERROR: " + error)
      });
}
function checkLang(arg, clickId){
    if(arg.toLowerCase() == trueLang.toLowerCase()){
        document.getElementById("points").innerText = parseInt(document.getElementById("points").innerText) + 1
        // document.getElementById(clickId).className = "btn btn-success"
        document.getElementById(clickId).className = "btn-correct"
        document.getElementById("next-btn").style.display = "block"
        
    }else{
        // document.getElementById("results").innerText = `You got ${document.getElementById("points").innerText} points!\nTake screenshot to show it to Kar1m!`
        // document.getElementById(clickId).className = "btn btn-danger"
        document.getElementById(clickId).className = "btn-fail"
        // document.getElementById(trueLangId).className = "btn btn-success"
        let data = new FormData()
        data.append("pts", document.getElementById("points").innerText)
        fetch('/endgame', {
            method: "POST",
            body: data
            })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error ${response.status}`);
                }
                return response.json()
            })
            .then((data) => {
                console.log(data)
            }
            )
        document.getElementById(trueLangId).className = "btn-correct"
        document.getElementById("next-btn").style.display = "block"
        alertify.error("You lost, You got " + document.getElementById("points").innerText + " Points!")
        lost = true
        document.getElementById("next-btn").innerText = "Retry"
    }
    for(i in [0,1,2,3]){
        document.getElementById(i).disabled = true
    }

}
window.onload = () => {
    for(i in [0,1,2,3]){
        document.getElementById(i).disabled = true
    }
    requestApi()

}
function next(){
    if(lost == true){
        window.location.reload()
    }else{
        document.getElementById("next-btn").style.display = "none"
        for(i in [0,1,2,3]){
            document.getElementById(i).disabled = false
            document.getElementById(i).innerText = "Loading"
            document.getElementById(i).disabled = true
            document.getElementById(i).className = "btn"
        }
        document.getElementById("code-block").innerText = "Loading..."
        requestApi()
    }
}

window.addEventListener("load", () => {
    document.body.onkeydown = function(e) {
        if(document.getElementById("game").style.display == "block"){
            if(e.key == "1" || e.key == "2" || e.key == "3" || e.key == "4"){
                document.getElementById(e.key-1).click()
            }if(e.key == "Enter"){
                if(document.getElementById("next-btn").style.display == "block"){
                    document.getElementById("next-btn").click()
                }
            }
        }
    
    }
})

function settings(){
    document.getElementById("settings").style.display = "block"
    document.getElementById("overlay").style.display = "block"
}

function changeTheme(theme){
    var formdata = new FormData()
    formdata.append("theme", theme)
    fetch(`/change-theme`, {
        method: "POST",
        body: formdata
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
            }
            return response.json()
        }
        )
        .then((data) => {
            console.log(data)
            window.location.href = '/'
        }
        )
}