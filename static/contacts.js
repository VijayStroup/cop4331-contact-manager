const first_name = document.getElementById('contact-first_name')
const last_name = document.getElementById('contact-last_name')
const email = document.getElementById('contact-email')
const phone = document.getElementById('contact-phone')
const searchIn = document.getElementById('search')
const errorNode = document.querySelector('#error')

async function addContact() {
  if (!first_name.value || !last_name.value || !email.value || !phone.value) return

  const data = {
    first_name: first_name.value,
    last_name: last_name.value,
    email: email.value,
    phone: phone.value
  }

  const res = await fetch('/api/contact', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
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
    const createClickHandler = (btn) => {
      const row = btn.parentElement.parentElement
      if (i % 2 == 0) { // save
        return function() {
          updateContact(row.children[0].innerHTML, {
            first_name: row.children[1].children[0].value,
            last_name: row.children[2].children[0].value,
            email: row.children[3].children[0].value,
            phone: row.children[4].children[0].value
          })
        }
      } else { // delete
        return function() {
          delContact({
            first_name: row.children[1].children[0].value,
            last_name: row.children[2].children[0].value,
            email: row.children[3].children[0].value,
            phone: row.children[4].children[0].value
          })
        }
      }
      
    }
    buttons[i].onclick = createClickHandler(buttons[i]);
  }
}
window.onload = addRowHandlers();

async function delContact(data) {
  const c = confirm('Are you sure you want to delete?')
  if (c) {
    const jwt = getCookie('token')
  
    const res = await fetch('/api/contact', {
      method: 'DELETE',
      headers:{
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': `Bearer ${jwt}`
      },
      body: JSON.stringify(data)
    })
  
    if (res.ok) {
      window.location.reload()
    }
  }
}

async function updateContact(id, data) {
  if (!data.first_name || !data.last_name || !data.email || !data.phone) return

  const jwt = getCookie('token')

  const res = await fetch(`/api/contact?contact_id=${id}`, {
    method: 'PUT',
    headers:{
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': `Bearer ${jwt}`
    },
    body: JSON.stringify(data)
  })

  const j = await res.json()

  if (res.ok) {
    errorNode.style.display = 'none'
    window.location.reload()
  } else {
    errorNode.style.display = 'block'
    errorNode.textContent = j.detail
  }
}

async function search() {
  if (!searchIn.value)
    window.location.replace(`/contacts?search=`)

  window.location.replace(`/contacts?search=${searchIn.value}`)
}
