
var left = function() {
  post('MOTOR1', {
    direction: 'forward',
    duration: 2
  });
}



function post(motor, command) {
  fetch(`/${motor}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        command
      })
    })
}
