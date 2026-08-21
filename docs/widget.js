(function() {
  const css = `
    .pv-widget-btn {
      position: fixed; bottom: 20px; right: 20px; z-index: 999999;
      background: linear-gradient(135deg, #06b6d4, #0284c7);
      color: white; border: none; padding: 12px 24px; border-radius: 50px;
      font-family: system-ui, -apple-system, sans-serif; font-weight: bold;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15); cursor: pointer; transition: transform 0.2s;
    }
    .pv-widget-btn:hover { transform: scale(1.05); }
    .pv-modal-overlay {
      position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5);
      z-index: 1000000; display: none; align-items: center; justify-content: center; backdrop-filter: blur(4px);
    }
    .pv-modal {
      background: white; border-radius: 16px; padding: 24px; width: 90%; max-width: 400px;
      font-family: system-ui, -apple-system, sans-serif; text-align: center; color: #111;
      box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    .pv-modal h3 { margin-top: 0; margin-bottom: 8px; }
    .pv-modal p { color: #666; font-size: 14px; margin-bottom: 20px; }
    .pv-modal input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 12px; box-sizing: border-box; }
    .pv-modal button { width: 100%; padding: 12px; background: #06b6d4; color: white; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
    .pv-close { margin-top: 12px; color: #999; font-size: 12px; cursor: pointer; text-decoration: underline; background: none; border: none; }
  `;
  const style = document.createElement('style');
  style.innerHTML = css;
  document.head.appendChild(style);

  const btn = document.createElement('button');
  btn.className = 'pv-widget-btn';
  btn.innerHTML = '🛡️ Scan Page for Phishing';
  document.body.appendChild(btn);

  const modalOverlay = document.createElement('div');
  modalOverlay.className = 'pv-modal-overlay';
  modalOverlay.innerHTML = `
    <div class="pv-modal">
      <h3>PhishVision Security Check</h3>
      <p>Scan the current page for phishing threats using AI Vision.</p>
      <input type="text" id="pv-url" value="${window.location.href}" readonly />
      <button id="pv-submit">Scan Now</button>
      <div id="pv-result" style="margin-top: 16px; font-weight: bold; display: none;"></div>
      <button class="pv-close" id="pv-close">Close</button>
      <a href="https://opticparse.com/pricing" style="display: block; margin-top: 16px; font-size: 11px; color: #06b6d4;">Powered by PhishVision. Get 100 free scans/month.</a>
    </div>
  `;
  document.body.appendChild(modalOverlay);

  btn.addEventListener('click', () => { modalOverlay.style.display = 'flex'; });
  document.getElementById('pv-close').addEventListener('click', () => { modalOverlay.style.display = 'none'; });

  document.getElementById('pv-submit').addEventListener('click', async () => {
    const resDiv = document.getElementById('pv-result');
    const submitBtn = document.getElementById('pv-submit');
    submitBtn.innerText = 'Scanning...';
    resDiv.style.display = 'none';

    try {
      // Calls PhishVision Node Backend directly
      const response = await fetch('https://opticparse-1opticparse-node-sg.onrender.com/api/phish-check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: window.location.href })
      });
      const data = await response.json();
      resDiv.style.display = 'block';
      if (data.verdict === 'SAFE') {
        resDiv.style.color = '#10b981';
        resDiv.innerText = '✅ SAFE';
      } else {
        resDiv.style.color = '#f43f5e';
        resDiv.innerText = '🚨 ' + data.verdict;
      }
    } catch (e) {
      resDiv.style.display = 'block';
      resDiv.style.color = '#f59e0b';
      resDiv.innerText = '⚠️ Scan Failed. Server unreachable.';
    } finally {
      submitBtn.innerText = 'Scan Now';
    }
  });
})();
