import axios from 'axios'

export function fetchData() {
  var offset = -( new Date().getTimezoneOffset()/60 )
  var headers = { headers: { offset: offset } }
  return axios.get('/nginx_status/', headers).then(response => { return response.data }).catch(error => { /* console.error(error); */ return Promise.reject(error) })
}

export function fetchSearchData(keyword) {
  return axios.get('/nginx_status/' + keyword).then(response => { return response.data }).catch(error => { /* console.error(error); */ return Promise.reject(error) })
}
