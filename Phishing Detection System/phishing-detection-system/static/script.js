document.getElementById("checkForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    
    const url = document.getElementById("urlInput").value;
    const resultDiv = document.getElementById("result");
    const resultContent = document.getElementById("resultContent");
    
    // Show loading
    resultContent.innerHTML = "<p>🔄 Analyzing URL...</p>";
    resultDiv.classList.remove("hidden");
    
    try {
        const response = await fetch("/check", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `url=${encodeURIComponent(url)}`
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultContent.innerHTML = `<p style="color: red;">❌ Error: ${data.error}</p>`;
        } else {
            const isPhishing = data.result.includes("PHISHING") || data.result.includes("SUSPICIOUS");
            const color = isPhishing ? "#dc3545" : "#28a745";
            const icon = isPhishing ? "🚨" : "✅";
            
            resultContent.innerHTML = `
                <div style="margin-bottom: 20px;">
                    <h4 style="color: ${color};">${icon} ${data.result}</h4>
                    <p><strong>URL:</strong> ${data.url}</p>
                    <p><strong>Confidence:</strong> ${(data.confidence * 100).toFixed(2)}%</p>
                </div>
                <div>
                    <h5>📈 Extracted Features:</h5>
                    <pre style="background: #f8f9fa; padding: 15px; border-radius: 5px; font-size: 14px;">${JSON.stringify(data.features, null, 2)}</pre>
                </div>
            `;
        }
    } catch (error) {
        resultContent.innerHTML = `<p style="color: red;">❌ Network error: ${error.message}</p>`;
    }
});
