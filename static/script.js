fatSecretHeader = new Headers();
fatSecretHeader.append("Content-Type", "application/json")

document.getElementById('play-game-1').addEventListener('click', () => {
  fetch('/get-token', {method: 'POST',})
});


document.getElementById('play-game-2').addEventListener('click', () => {
  fetch('/get-food', {
  method: 'GET',
  headers: fatSecretHeader})
  .then(response => response.text())
  .then(response_text => document.getElementById('play-game-1').innerText=response_text)
  .catch(error => {
    console.error('API error:', error);
  });
});

