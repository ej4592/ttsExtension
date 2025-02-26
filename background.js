// Create context menu item
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "readText",
    title: "Read text out loud",
    contexts: ["selection"]
  });
});

// Listen for context menu clicks
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId === "readText" && info.selectionText) {
    // Send the selected text to your backend
    try {
      const response = await fetch("http://localhost:5000/tts", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: info.selectionText })
      });
      if (!response.ok) {
        throw new Error("TTS API error");
      }
      // Convert the response into a Blob and create an object URL
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);

      // Play the audio
      const audio = new Audio(audioUrl);
      audio.play();
    } catch (error) {
      console.error("Error during TTS:", error);
    }
  }
});
