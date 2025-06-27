document.getElementById('play-game-1').addEventListener('click', () => {
  fetch('/get-token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action: 'generate_token' })
  })
});

document.getElementById('play-game-2').addEventListener('click', () => {
  fetch('/get-food', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ search_expression: 'apple' })
  })
  .then(response => response.json())
  .then(data => {
    console.log('Search results:', data);
  })
  .catch(error => {
    console.error('API error:', error);
  });
});

