document.getElementById('settingsBtn').addEventListener('click', () => {
  chrome.runtime.openOptionsPage();
});

document.getElementById('extractBtn').addEventListener('click', async () => {
  const query = document.getElementById('query').value.trim();
  const schemaStr = document.getElementById('schema').value.trim();
  const statusDiv = document.getElementById('status');
  const resultPre = document.getElementById('result');
  const extractBtn = document.getElementById('extractBtn');
  
  if (!query) {
    statusDiv.textContent = "Please enter an extraction query.";
    return;
  }
  
  let schema = null;
  if (schemaStr) {
    try {
      schema = JSON.parse(schemaStr);
    } catch (e) {
      statusDiv.textContent = "Invalid JSON schema format.";
      return;
    }
  }

  statusDiv.textContent = "Checking API Key...";
  resultPre.style.display = 'none';
  extractBtn.disabled = true;

  chrome.storage.sync.get(['apiKey'], async (result) => {
    const apiKey = result.apiKey;
    if (!apiKey) {
      statusDiv.textContent = "API Key missing. Click 'Open Settings' to configure.";
      extractBtn.disabled = false;
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
      
      statusDiv.textContent = "Extracting with Vision AI...";
      
      const payload = {
        image_base64: dataUrl,
        extraction_query: query,
        response_schema: schema
      };

      const response = await fetch('https://opticparse-api.onrender.com/api/vision-scrape', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API Error ${response.status}: ${errorText}`);
      }

      const data = await response.json();
      
      statusDiv.textContent = "Extraction complete!";
      resultPre.textContent = JSON.stringify(data, null, 2);
      resultPre.style.display = 'block';

    } catch (err) {
      statusDiv.textContent = `Error: ${err.message}`;
    } finally {
      extractBtn.disabled = false;
    }
  });
});
