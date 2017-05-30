function put(command) {
  fetch(`/${command}`, {
    method: 'put'
  })
}
