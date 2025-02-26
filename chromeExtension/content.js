chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.audioData) {
    // Reconstruct the Uint8Array from the received array
    const uint8Array = new Uint8Array(message.audioData);
    // Create a Blob from the array
    const blob = new Blob([uint8Array], { type: "audio/wav" });
    // Create a URL for the Blob
    const audioUrl = URL.createObjectURL(blob);
    // Play the audio
    const audio = new Audio(audioUrl);
    audio.play();
  }
});
