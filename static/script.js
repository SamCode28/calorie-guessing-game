fatSecretHeader = new Headers();
fatSecretHeader.append("Content-Type", "application/json")

document.getElementById('play-game-2').addEventListener('click', () => {
  fetch('/get-food', {
  method: 'GET',
  headers: fatSecretHeader})
  .then(response => response.text())
  .then(response_text => document.getElementById('src-container').setAttribute("src",response_text))
  .catch(error => {
    console.error('API error:', error);
  });
});

