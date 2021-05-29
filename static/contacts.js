const first_name = document.getElementById('contact-first_name');
const last_name = document.getElementById('contact-last_name');
const email = document.getElementById('contact-email');
const phone = document.getElementById('contact-phone');
const save_btn = document.getElementById('save-contact');
const delete_btn = document.getElementById('delete-contact');

let data = {
  first_name,
  last_name,
  email,
  phone
}

// add contact
document.querySelector('#add-contact').addEventListener('click', () => {

  fetch("/api/contact", {
    method: 'post',
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify(data)
  })

  .then(Response => Response.json())
  .then(data => console.log('add contact'))
})

// search
document.querySelector('#search').addEventListener('click', () => {
  console.log('search')
})

// update contact row
document.querySelector('#save-contact').addEventListener('click', () => {
  fetch("/api/contact", {
    method: 'put',
    headers:{
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify(data) // include new data
  })

  .then(Response => Response.json())
  .then(data => console.log('save contact'))
})

// delete contact row
document.querySelector('#delete-contact').addEventListener('click', () => {
  fetch("api/contact", {
    method: 'delete',
    headers:{
      "Content-Type": "application/json",
      "Accept": "application/json"
    } // find and delete data 
  })
  .then(Response => Response.json())
  .then(data => console.log('delete contact'))

})
