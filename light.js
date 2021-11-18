


// Manual list of apetures, speeds and ISOs at 1/3 stop increments.
var fstops = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.5, 2.8, 3.2, 3.5, 4, 4.5, 5.0, 5.6, 6.3, 7.1, 8, 9, 10, 11, 13, 14, 16, 18, 20, 22, 27, 32, 38, 45, 54, 64, 76, 91, 108];
var shutterSpeeds = [1/8000, 1/6400, 1/5000, 1/4000, 1/3200, 1/2500, 1/2000, 1/1600, 1/1250, 1/1000, 1/800, 1/640, 1/500, 1/400, 1/320, 1/250, 1/200, 1/160, 1/125, 1/100, 1/80, 1/60, 1/50, 1/40, 1/30, 1/25, 1/20, 1/15, 1/13, 1/10, 1/8, 1/6, 1/5, 1/4, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.3, 1.6, 2, 2.5, 3.2, 4, 5];
var isos = [50, 100, 125, 160, 200, 250, 320, 400, 500, 640, 800, 1000, 1250, 1600, 2000, 2500, 3200, 4000, 5000, 6400, 12800, 25600];


var locked = false;
var exposureValue = 0;
var lockEl = byId('lock');

lockEl.addEventListener('click', toggleLocked, false);
document.body.addEventListener('change', change, false);
document.body.addEventListener('click', selectInput, false);
document.body.addEventListener('keydown', handleKey, false);

change();


function change(e) {
  var values = getValues();
  if (!locked) {
    calculateEv(values);
  } else {
    switch (e && e.target.id) {
      case 'n': updateSpeedToFit(values); break;
      case 't': updateApertureToFit(values); break;
      case 's': updateSpeedToFit(values); break;
    }
  }
}

function selectInput(e) {
  if (e.target.tagName == 'INPUT') e.target.select();
}

function toggleLocked(e) {
  lockEl.innerHTML = locked ? '<u>L</u>ock' : 'Un<u>l</u>ock';
  locked = !locked;
}

function handleKey(e) {
  switch (e.keyCode) {
    case 65: focus('n'); break;        // A
    case 84: focus('t'); break;        // T
    case 83: focus('s'); break;        // S
    case 76: toggleLocked(); break;    // L
    case 38:                           // Up
      arrow(e.target.id, 1);
      break;
    case 40:                           // Down 
      arrow(e.target.id, -1);
      break; 
    case 13:                           // Enter
      change(e);
      e.target.select();
      break;
    default: return;
  }
  e.preventDefault();
}

function arrow(id, dir) {
  var array;
  switch (id) {
    case 'n': array = fstops; break;
    case 't': array = shutterSpeeds; break;
    case 's': array = isos; break;
    default: return;
  }
  
  var values = getValues();
  var val = roundToArray(values[id], array);
  if (values[id] == val ||
      dir == 1 && values[id] > val ||
      dir == -1 && values[id] < val) {
    val = array[array.indexOf(val) + dir];
  }
  
  if (!val) return;
  
  values[id] = val;
  
  if (!locked) {
    calculateEv(values);
  } else {
    switch (id) {
      case 'n': updateSpeedToFit(values); break;
      case 't': updateApertureToFit(values); break;
      case 's': updateSpeedToFit(values); break;
    }
  }
}

function focus(id) {
  byId(id).focus();
  byId(id).select();
}

// Find an aperture to match the other values. 
function updateApertureToFit(v) {
  v.n = Math.sqrt(v.t * Math.pow(2, exposureValue + log2(v.s / 100)));
  updateDisplay(v);
}

// Change time to account for changes in the other values.
function updateSpeedToFit(v) {
  v.t = (v.n * v.n) / Math.pow(2, exposureValue + log2(v.s / 100)); 
  updateDisplay(v);
}

// Calculate the EV100 for the aperture, speed and ISO.
function calculateEv(v) {
  var ev = log2(v.n * v.n / v.t);
  exposureValue = ev - log2(v.s / 100);
  updateDisplay(v);
}

function updateDisplay(v) {
  if (byId('round').checked) {
    roundValues(v);
  }
  
  // Convert speed to a fraction, a decimal if it's less than 5, or else a whole number.
  var t = v.t < 1 ? decimalToFraction(v.t) : v.t < 5 ? Math.round(v.t * 10) / 10 : Math.round(v.t);

  byId('n').value = Math.round(v.n * 10) / 10;
  byId('t').value = t;
  byId('s').value = Math.round(v.s);

  if (v.t > 120) {
    byId('tm').innerHTML = '(' + Math.round(v.t / 6) / 10 + ' mins)';
  } else {
    byId('tm').innerHTML = '';
  }

  byId('ev').innerHTML = Math.round(exposureValue, 2);
  
  var v1 = Math.round(exposureValue);
  if (v1 > 22) v1 = 22;
  else if (v1 > 17) v1 = 17;
  else if (v1 < -6) v1 = -6;
  var description = levels[v1];
  if (!description) description = 'Bad inputs.';
  byId('desc').innerHTML = description;
}

function getValues() {
  var n = Number(byId('n').value);
  var s = Number(byId('s').value);
  var t = byId('t').value;

  if (/1\/[0-9]+/.test(t)) {
    t = eval(t);
  } else {
    t = Number(t);
  }

  var v = {n: n, s: s, t: t};

  if (byId('round').checked) {
    roundValues(v);
  }

  return v;
}

function roundValues(v) {
  v.t = roundToArray(v.t, shutterSpeeds);
  v.n = roundToArray(v.n, fstops);
  v.s = roundToArray(v.s, isos); 
}

function roundToArray(val, array) {
  // Short-circuit extremes. 
  if (val < array[0] || val > array[array.length - 1]) return val;
  var best = val;
  var bestDiff = Infinity;
  for (var i = 0; i < array.length; i++) {
    var diff = Math.abs(array[i] - val);
    if (diff <= bestDiff) {
      best = array[i];
      bestDiff = diff;
    } else {
      return best;
    }
  }
  return best;
}

function log2(x) {
  return Math.log(x) / Math.LN2;
}

function decimalPlaces(num) {
  var str = num.toString();
  var idx = str.indexOf('.');
  return idx >= 0 ? str.length - idx - 1 : 0;
}

function decimalToFraction(value) {
  var n = decimalPlaces(value);
  var m = Math.pow(10, n);
  var numerator = value * m;
  var denominator = Math.round(numerator ? m / numerator : 0);
  var numerator = numerator ? numerator / numerator : 0;
  if (denominator > 8000) {
    denominator = Math.round(denominator / 1000) * 1000;
  }
  return numerator ? numerator + '/' + denominator : '0';
}

function byId(id) {
  return document.getElementById(id);
}

