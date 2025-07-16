const video = document.getElementById('camera');
const canvas = document.getElementById('snapshot');
const result = document.getElementById('result');

navigator.mediaDevices.getUserMedia({ video: true })
  .then(stream => {
    video.srcObject = stream;
  });

function capture() {
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataURL = canvas.toDataURL('image/png');

  fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: 'image=' + encodeURIComponent(dataURL)
  })
  .then(response => response.text())
  .then(html => {
    result.innerHTML = html;
  });
}
