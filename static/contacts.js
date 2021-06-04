const first_name = document.getElementById('contact-first_name');
const last_name = document.getElementById('contact-last_name');
const email = document.getElementById('contact-email');
const phone = document.getElementById('contact-phone');
const search = document.getElementById('search');
const errorNode = document.querySelector('#error');

async function addContact() {
  if (!first_name.value || !last_name.value || !email.value || !phone.value) return

  const data = {
    first_name: first_name.value,
    last_name: last_name.value,
    email: email.value,
    phone: phone.value
  }

  const res = await fetch("/api/contact", {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
      'Authorization': `Bearer ${getCookie('token')}`
      
    },
    body: JSON.stringify(data)
  })
  const j = await res.json()
  if (!res.ok) {
    errorNode.style.display = 'block'
    errorNode.textContent = j.detail
  } else {
    errorNode.style.display = 'none'
    window.location.reload()
  }
}

async function addRowHandlers() {
  const table = document.getElementById('table')

  const buttons = table.querySelectorAll('tr td button')
  for (i = 0; i < buttons.length; i++) {
    if (i % 2 == 0) { // save
      // console.log(buttons[i])
    } else { // delete
      const createClickHandler = (btn) => {
        return function() {
          const row = btn.parentElement.parentElement
          delContact({
            first_name: row.children[1].children[0].value,
            last_name: row.children[2].children[0].value,
            email: row.children[3].children[0].value,
            phone: row.children[4].children[0].value,
          })
        }
      }  
      buttons[i].onclick = createClickHandler(buttons[i]);
    }
  }
}
window.onload = addRowHandlers();

async function delContact(data) {
  const jwt = getCookie('token');

  const res = await fetch("api/contact", {
    method: 'DELETE',
    headers:{
      "Content-Type": "application/json",
      "Accept": "application/json",
      'Authorization': `Bearer ${jwt}`
    },
    
    body: JSON.stringify(data)
  })

  if (res.ok) {
    window.location.reload()
  }
}

// search
document.querySelector('#search').addEventListener('click', () => {
  const jwt = getCookie('token');

  fetch("/api/search", {
    method: 'get',
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json",
      "Authorization": `Bearer ${jwt}`
    },
    body: JSON.stringify(search.innerText)
  })

  .then(Response => Response.json())
  .then(search => console.log(search['contacts']))
})

// update contact row
document.querySelector('#save-contact').addEventListener('click', () => {

  const jwt = getCookie('token');
  
  const data = {
    first_name: first_name.innerText,
    last_name: last_name.innerText,
    email: email.innerText,
    phone: phone.innerText
  }
  
  fetch("/api/contact", {
    method: 'put',
    headers:{
      "Content-Type": "application/json",
      "Accept": "application/json",
      'Authorization': `Bearer ${jwt}`
    },
    body: JSON.stringify(data)
  })

  .then(Response => Response.json())
  .then(data => console.log('save contact'))
})
