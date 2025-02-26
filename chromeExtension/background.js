chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "readText" && info.selectionText && tab.id) {
    try {
      // First, inject the content script into the active tab
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
      });

      // Then, send the message
      const response = await fetch("http://localhost:5001/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: info.selectionText })
      });

      if (!response.ok) {
        throw new Error("TTS request failed with status " + response.status);
      }

      // Convert response to an ArrayBuffer and then to an array
      const arrayBuffer = await response.arrayBuffer();
      const audioData = Array.from(new Uint8Array(arrayBuffer));

      // Send the audio data to the content script
      chrome.tabs.sendMessage(tab.id, { audioData });
    } catch (error) {
      console.error("Error while processing TTS request:", error);
    }
  }
});
