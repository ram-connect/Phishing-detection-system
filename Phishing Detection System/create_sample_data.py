import pandas as pd
import random

# Create a sample dataset
data = []

# Generate safe URLs
safe_urls = [
    "https://google.com",
    "https://github.com",
    "https://stackoverflow.com",
    "https://python.org",
    "https://microsoft.com",
    "https://apple.com",
    "https://amazon.com",
    "https://netflix.com",
    "https://twitter.com",
    "https://facebook.com"
]

# Generate phishing URLs
phishing_urls = [
    "http://192.168.1.1.login-secure.com",
    "https://paypal-verify-security.com",
    "http://google-login-verify.com",
    "https://microsoft-account-security.com",
    "http://10.0.0.1.bank-login.com",
    "https://facebook-account-recovery.com",
    "http://apple-id-verify-security.com",
    "https://netflix-payment-update.com",
    "http://amazon-account-security-verify.com",
    "https://twitter-password-reset-verify.com"
]

for url in safe_urls:
    data.append({
        "url": url,
        "label": 0,  # 0 = safe
        "url_length": len(url),
        "has_ip": 0,
        "has_at_symbol": 0,
        "has_dash": 0,
        "is_https": 1 if url.startswith("https") else 0,
        "subdomain_count": url.count(".") - 1
    })

for url in phishing_urls:
    data.append({
        "url": url,
        "label": 1,  # 1 = phishing
        "url_length": len(url),
        "has_ip": 1 if any(char.isdigit() and url.count(".") >= 3 for char in url.split(".")[0]) else 0,
        "has_at_symbol": 1 if "@" in url else 0,
        "has_dash": 1 if "-" in url else 0,
        "is_https": 1 if url.startswith("https") else 0,
        "subdomain_count": url.count(".") - 1
    })

# Create DataFrame
df = pd.DataFrame(data)
df.to_csv("sample_phishing_data.csv", index=False)
print(f"Created sample dataset with {len(data)} entries")
print(df.head())
