// on register
document.querySelector('#register-btn').addEventListener('click', () => {
  console.log('register')

  const usernameInput = document.querySelector('#username').value;
  const passwordInput = document.querySelector('#password').value;

  fetch('/api/user', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: usernameInput, 
      password: passwordInput
    })
  })
  
  .then(res => res.json)
  .then(data => console.log('Success')) 
  .catch(error => console.error('Error'))
})
