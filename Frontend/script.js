const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const colorPicker = document.getElementById('colorPicker');
const brushSize = document.getElementById('brushSize');
const darkModeToggle = document.getElementById('darkModeToggle');
const predictionBox = document.getElementById('prediction');
let painting = false;

// Initialize background white
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

canvas.addEventListener('mousedown', () => painting = true);
canvas.addEventListener('mouseup', () => {
    painting = false;
    ctx.beginPath();
});
canvas.addEventListener('mousemove', draw);

function draw(e) {
    if (!painting) return;
    const color = document.getElementById('colorPicker').value;
    const size = document.getElementById('brushSize').value;
    ctx.lineWidth = size;
    ctx.lineCap = 'round';
    ctx.strokeStyle = color;

    const rect = canvas.getBoundingClientRect();
    ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
}

function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = darkModeToggle.checked ? "#333" : "white";  // add this
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
}

function predict() {
    const imgData = canvas.toDataURL('image/png');

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imgData })
    })
    .then(response => response.json())
    .then(data => {
        predictionBox.innerText = data.prediction;
    })
    .catch(err => {
        console.error(err);
        predictionBox.innerText = "Error";
    });
}
// Dark mode logic
darkModeToggle.addEventListener('change', () => {
    document.body.classList.toggle('dark');
    clearCanvas(); // also update canvas background
});

