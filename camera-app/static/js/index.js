const url = "http://192.168.249.1:5000"
const duraion = "2000"

async function startHandler() {
  const response = await fetch(url + '/start');
  const data = await response.json();
}

async function stopHandler() {
  const response = await fetch(url + '/stop');
  const data = await response.json();
}

async function currentStatus() {
  const response = await fetch(url + '/status');
  const data = await response.json();
  const ele = document.getElementById('camera-status');
  ele.textContent = data['status'];
}

setInterval(currentStatus, 2000);
