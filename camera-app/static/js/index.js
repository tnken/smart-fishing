const url = "http://192.168.249.1:5000"
const duraion = "2000"

async function startHandler() {
  const ele = document.getElementById('mode-status');
  if (ele.textContent == 'Video') {
    endpoint = url + '/start_video'
  } else {
    endpoint = url + '/start_picture'
  }
  const response = await fetch(endpoint);
  await response.json();
}

async function stopHandler() {
  const response = await fetch(url + '/stop');
  await response.json();
}

async function transferHandler() {
  const response = await fetch(url + '/pictures');
  const data = await response.json();
  for (const img of data['pictures']) {
    img_ele = document.createElement('img');
    img_ele.src = 'data:image/jpeg;base64,' + img
    img_ele.width = 400;
    document.getElementById('pictures').prepend(img_ele);
  }
  p_ele = document.createElement('p');
  p_ele.textContent('Timestamp: ' + data['picture_mode_timestamp'])
  document.getElementById('pictures').prepend(p_ele);
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

function modePictureHandler() {
  const ele = document.getElementById('mode-status');
  ele.textContent = 'Picture';
  document.getElementById('picture-button').classList.add('pure-button-active');
  document.getElementById('video-button').classList.remove('pure-button-active');
}

function modeVideoHandler() {
  const ele = document.getElementById('mode-status');
  ele.textContent = 'Video';
  document.getElementById('picture-button').classList.remove('pure-button-active');
  document.getElementById('video-button').classList.add('pure-button-active');
}

setInterval(currentStatus, 2000);
