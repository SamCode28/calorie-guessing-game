fatSecretHeader = new Headers();
fatSecretHeader.append("Content-Type", "application/json")

document.getElementById('play-game-1').addEventListener('click', () => {
  fetch('/get-food', {
  method: 'GET',
  headers: fatSecretHeader})
  .then(response => response.text())
  .then(response_text =>{
    document.getElementById('img-container-1').setAttribute("src",response_text)
    document.getElementById('img-container-2').setAttribute("src",response_text)
    hideClass('main-menu-container')
    removeHideClass("game-grid-container")
    //removeHideClass('card-2')
  })
  .catch(error => {
    console.error('API error:', error);
  });
});

function hideClass(id){
  document.getElementById(id).classList.add('hidden')
}

function removeHideClass(id){
  document.getElementById(id).classList.remove('hidden')
}

