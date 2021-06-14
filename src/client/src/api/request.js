// Node MCU host
const baseUrl = 'http://192.168.0.28/'

export async function fetch_nodemcu(request_type) {
  // Fetches the request from the client to the nodeMCU
  // PARAM: request_type (string) request to trigger the nodeMCU
  //        to perform an action 

  const url = baseUrl + request_type
  const method = { method: 'GET' }

  await fetch(url, method)
}
