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

export function setCookie(cname, cvalue, exdays) {
  if (typeof window != 'undefined') {
    let d = new Date()
    d.setTime(d.getTime() + (exdays*24*60*60*1000))
    const expires = 'expires='+ d.toUTCString()

    if (process.env.NEXT_PUBLIC_STATUS == 'dev')
      document.cookie = `${cname}=${cvalue};${expires};samesite=strict;path=/`
    else
      document.cookie = `${cname}=${cvalue};${expires};secure;samesite=strict;path=/`
  }
}

export function getCookie(cname) {
  if (typeof window != 'undefined') {
    let name = cname + '='
    let decodedCookie = decodeURIComponent(document.cookie)
    let ca = decodedCookie.split(';')
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i]
      while (c.charAt(0) == ' ') {
        c = c.substring(1)
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length)
      }
    }
  }
  return null
}