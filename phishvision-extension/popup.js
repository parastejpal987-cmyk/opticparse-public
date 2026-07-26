document.getElementById('settingsBtn').addEventListener('click', () => {
  chrome.runtime.openOptionsPage();
});

document.getElementById('scanBtn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  const resultDiv = document.getElementById('result');
  const detailsDiv = document.getElementById('details');
  const scanBtn = document.getElementById('scanBtn');
  
  statusDiv.textContent = "Checking API Key...";
  resultDiv.style.display = 'none';
  resultDiv.className = '';
  detailsDiv.textContent = '';
  scanBtn.disabled = true;

  chrome.storage.sync.get(['apiKey'], async (result) => {
    const apiKey = result.apiKey;
    if (!apiKey) {
      statusDiv.textContent = "API Key missing. Click 'Settings' to configure.";
      scanBtn.disabled = false;
      return;
    }

    try {
      statusDiv.textContent = "Capturing active tab...";
      const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tabs.length === 0) {
        throw new Error("No active tab found");
      }

      const activeTab = tabs[0];
      const dataUrl = await chrome.tabs.captureVisibleTab(activeTab.windowId, { format: 'png' });
      
      const base64Image = dataUrl.split(',')[1] || dataUrl;

      statusDiv.textContent = "Analyzing with PhishVision AI...";
      
      const response = await fetch('https://opticparse-api.onrender.com/api/phish-detect', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey
        },
        body: JSON.stringify({ 
          url: activeTab.url,
          image_base64: base64Image 
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API Error ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      statusDiv.textContent = "Analysis complete.";
      
      resultDiv.style.display = 'block';
      if (data.is_malicious || data.threat_level === "HIGH") {
        resultDiv.textContent = "⚠️ MALICIOUS PAGE DETECTED";
        resultDiv.classList.add('malicious');
      } else {
        resultDiv.textContent = "✅ PAGE APPEARS SAFE";
        resultDiv.classList.add('safe');
      }

      if (data.analysis) {
        detailsDiv.textContent = `Analysis: ${data.analysis}`;
      }

    } catch (err) {
      statusDiv.textContent = `Error: ${err.message}`;
    } finally {
      scanBtn.disabled = false;
    }
  });
});
