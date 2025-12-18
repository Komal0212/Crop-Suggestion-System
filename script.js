
async function loadData() {
    try {
        let s = await fetch("http://localhost:5000/sensor");
        let sensor = await s.json();

        document.getElementById("temp").innerText = sensor.temperature.toFixed(1);
        document.getElementById("hum").innerText = sensor.humidity.toFixed(1);
        document.getElementById("soil").innerText = sensor.soil;
        document.getElementById("light").innerText = sensor.light;
        document.getElementById("rain").innerText = sensor.rain;
        
        let p = await fetch("http://localhost:5000/prediction");
        let pred = await p.json();
        document.getElementById("crop").innerText = pred.crop;
        let cropPic = document.getElementById("crop-pic");
        if (cropPic) {
            cropPic.src = `http://localhost:5000/static/images/${pred.image}`;
        }

            // Update graph
        let graphImg = document.getElementById("trend-img");
        if (graphImg) {
            graphImg.src = "http://localhost:5000/graph?" + new Date().getTime();
        }
    } catch (err) {
        console.error("Error:", err);
    }
}

loadData();
setInterval(loadData, 3000);
