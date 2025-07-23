function FindProxyForURL(url, host) {
  if (dnsDomainIs(host, "youtube.com") || dnsDomainIs(host, "instagram.com"))
    return "PROXY 38.114.102.88:5421";
  return "DIRECT";
}