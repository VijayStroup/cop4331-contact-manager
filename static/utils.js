function setCookie(cname, cvalue, exdays) {
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

function getCookie(cname) {
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

function delCookie(cname) {
  if (typeof window != 'undefined')
    document.cookie = cname + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'
}
