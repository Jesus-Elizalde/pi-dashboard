async function update() {
  try {
    const res = await fetch('/api/data');
    if (!res.ok) throw new Error(res.statusText);
    const data = await res.json();
    document.getElementById('date').textContent = data.date;
    document.getElementById('day').textContent  = data.day;
    document.getElementById('time').textContent = data.time;
    document.getElementById('temp').textContent = `${data.temp}°F`;
    document.getElementById('desc').textContent = data.desc;
  } catch (err) {
    console.error('Update failed:', err);
  }
}

// initial + repeat
update();
setInterval(update, 60_000);  // every minute is enough for clock + weather
