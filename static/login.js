const user_input = document.querySelector('#username');
const pass_input = document.querySelector('#password');
const errorNode = document.querySelector('#error');

async function login() {
  if (!user_input.value || !pass_input.value) return
  
  const params = new URLSearchParams({
    username: user_input.value,
    password: pass_input.value
  })

  const res = await fetch(`http://localhost:8000/api/login?${params}`, {
    headers: {
      'Content-Type': 'application/json'
    }
  })

  const j = await res.json()
  if (!res.ok) {
    errorNode.style.display = 'block'
    errorNode.textContent = j.detail
  } else {
    errorNode.style.display = 'none'
    setCookie('token', j.token, 30)
    window.location.replace('/')
  }
}
