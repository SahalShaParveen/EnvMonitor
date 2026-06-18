async function updateData() {
    const response = await fetch("/api/latest")
    const data = await response.json()

    document.getElementById("temperature").innerText = data.esp32_1.temperature
    document.getElementById("humidity").innerText = data.esp32_1.humidity

    document.getElementById("cpu_temp").innerText = data.pi.cpu_temp
    document.getElementById("ram_usage").innerText = data.pi.ram_usage
    document.getElementById("disk_usage").innerText = data.pi.disk_usage
}

updateData();
setInterval(updateData, 5000);


let chart;
let currentPeriod = "24h";

async function loadChart(period = currentPeriod) {
    currentPeriod = period;
    const res = await fetch(`/api/history?metric=temperature&device=esp32_1&period=${period}`);
    const json = await res.json();

    const labels = json.data.map(x => x[0]);
    const values = json.data.map(x => x[1]);

    if (chart) chart.destroy();

    const ctx = document.getElementById("tempChart").getContext("2d");

    chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Temperature",
                data: values,
                borderWidth: 2,
                fill: false
            }]
        }
    });
}

loadChart("24h");
setInterval(() => loadChart(), 10000);