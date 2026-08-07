// Load saved API key on startup
chrome.storage.sync.get(['apiKey'], (result) => {
  if (result.apiKey) {
    document.getElementById('apiKey').value = result.apiKey;
  }
});

// Save API key
document.getElementById('saveBtn').addEventListener('click', () => {
  const apiKey = document.getElementById('apiKey').value.trim();
  const statusDiv = document.getElementById('status');

  if (!apiKey.startsWith('op_live_')) {
    statusDiv.textContent = 'Invalid API key format. Must start with op_live_';
    return;
  }

  chrome.storage.sync.set({ apiKey: apiKey }, () => {
    statusDiv.style.color = '#00ffcc';
    statusDiv.textContent = 'Settings saved successfully!';
    setTimeout(() => {
      statusDiv.textContent = '';
      statusDiv.style.color = '#ffaa00';
    }, 3000);
  });
});
