var DOWN_CLASS = 'down';

function down(element) {
  if (!element) {
    return;
  }
  if (element.classList.contains(DOWN_CLASS)) {
    return;
  }
  element.classList.add(DOWN_CLASS);
  put(element.id);
}

function up(element) {
  if (!element) {
    return;
  }
  command = element.id;
  element.classList.remove(DOWN_CLASS);
  put('stop');
}

function put(command) {
  fetch(`/${command}`, {
    method: 'put'
  })
}

var key2command = {
  37: "left",
  38: "forward",
  39: "right",
  40: "backward"
};

function getElement(key) {
  var command = key2command[key];
  if (!command) {
    return null;
  }
  return document.getElementById(command);
}

document.addEventListener('keydown', function(event) {
  var element = getElement(event.keyCode)
  down(element);
});

document.addEventListener('keyup', function(event) {
  var element = getElement(event.keyCode)
  up(element);
});
