import re
from urllib.parse import urlparse
import tldextract

def extract_features(url):
    """Extract features from a URL for phishing detection"""
    
    features = {}
    
    # Ensure URL has protocol
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    # 1. URL length
    features['url_length'] = len(url)
    
    # 2. Check for IP address in URL
    features['has_ip'] = bool(re.search(r'\d+\.\d+\.\d+\.\d+', url))
    
    # 3. Check for @ symbol
    features['has_at_symbol'] = '@' in url
    
    # 4. Check for double slash redirect
    features['double_slash_redirect'] = '//' in url[7:]
    
    # 5. Check for dash in domain
    parsed = urlparse(url)
    domain = parsed.netloc if parsed.netloc else parsed.path.split('/')[0]
    features['has_dash'] = '-' in domain
    
    # 6. Check for multiple subdomains
    ext = tldextract.extract(url)
    features['subdomain_count'] = len(ext.subdomain.split('.')) if ext.subdomain else 0
    
    # 7. Check for HTTPS
    features['is_https'] = url.startswith('https')
    
    # 8. Domain registration length (simulated - would need WHOIS in production)
    features['domain_age'] = 1  # Placeholder
    
    return features
