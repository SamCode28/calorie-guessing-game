document.getElementById('play-game-1').addEventListener('click', () => {
  fetch('/get-token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action: 'generate_token' })
  })
  .then(res => res.json())
  .then(data => {
    console.log('Response:', data);
    // Update the DOM here
  });
});