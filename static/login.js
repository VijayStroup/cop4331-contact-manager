// on login
document.querySelector('#login-btn').addEventListener('click', () => {
  console.log('login')

  const user_input = document.querySelector('#username').value;
  const pass_input = document.querySelector('#password').value;

  const jwt = getCookie('token');
  
  fetch('/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify({
      username: user_input, 
      password: pass_input
    })
  })
  
  .then(res => {
    if (res.ok) {
      res.json().then(data => setCookie('token', data['token'], 30));
    } else {
      console.log('Incorrect username/password')
    }
  })

  .catch(error => console.error('Error', error))
})

function logout() {
  delCookie('token')
  window.location.replace('/')
}
