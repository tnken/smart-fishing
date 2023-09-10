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

async function transferHandler() {
  const response = await fetch(url + '/pictures');
  const data = await response.json();
  console.log(data)
  for (const img of data['pictures']) {
    img_ele = document.createElement('img');
    img_ele.src = 'data:image/jpeg;base64,' + img
    img_ele.width = 400;
    document.getElementById('pictures').appendChild(img_ele);
  }
}

async function currentStatus() {
  try {
    const response = await fetch(url + '/status');
    if (!response.ok) throw await response.json()
    const data = await response.json();
    current = data['status']
  } catch (e) {
    console.log(e)
    current = 'offline'
  }
  const ele = document.getElementById('camera-status');
  ele.textContent = current;
}

setInterval(currentStatus, 2000);
