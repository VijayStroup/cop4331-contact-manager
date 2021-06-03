const usernameInput = document.querySelector('#username')
const passwordInput = document.querySelector('#password')
const errorNode = document.querySelector('#error')

// on register
async function register() {
  if (!usernameInput.value || !passwordInput.value) return

  const res = await fetch('http://localhost:8000/api/user', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: usernameInput.value,
      password: passwordInput.value
    })
  })

  const j = await res.json()
  if (!res.ok) {
    errorNode.textContent = j.detail
  } else {
    console.log('all good')
    window.location.replace('/login')
  }
}
