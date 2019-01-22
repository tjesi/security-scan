package main

import (
	"fmt"
	"net/http"
	"strings"
	"time"
)

/*
securityHeaders receive the url of a website, connect to the
website and check if certain security regarding security
return acceptable data to maintain security and privacy.
*/

func securityHeaders(website string, preaload *string) string {

	content := ""
	var ok bool
	var list []string
	timeout := time.Duration(5 * time.Second)
	client := http.Client{Timeout: timeout}

	// Checking for security headers in general
	url := "http://" + website
	resp, err := client.Get(url)
	if err != nil {
		// XXXX this is a HTTP error, not SSL.
		content += "SSLerror"
		return content
	}

	// https://scotthelme.co.uk/a-new-security-header-feature-policy
	content += hasPolicy("Feature-Policy", resp)

	// https://scotthelme.co.uk/a-new-security-header-expect-ct
	content += hasPolicy("Expect-CT", resp)

	// https://scotthelme.co.uk/content-security-policy-an-introduction
	content += hasPolicy("Content-Security-Policy", resp)

	// https://scotthelme.co.uk/hardening-your-http-response-headers
	// https://www.troyhunt.com/clickjack-attack-hidden-threat-right-in
	// You have three values: DENY, SAMEORIGIN, ALLOW-FROM, and all is good.
	content += hasPolicy("X-Frame-Options", resp)

	// https://scotthelme.co.uk/hardening-your-http-response-headers
	// You have one value: nosniff
	content += hasPolicy("X-Content-Type-Options", resp)

	// https://scotthelme.co.uk/tough-cookies/
	// You have two main values: HttpOnly and Secure
	content += hasPolicy("Set-Cookie", resp)

	/* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Allow-Origin
	 */
	content += hasPolicy("Access-Control-Allow-Origin", resp)

	// https://scotthelme.co.uk/a-new-security-header-referrer-policy
	// Some values are okay, some are not
	list, ok = resp.Header["Referrer-Policy"]
	if ok && (inList("strict-origin", list) || inList("same-origin", list) || inList("no-referrer-when-downgrade", list)) {
		content += "Feature-Policy:YES" + "\n"
	} else {
		content += "Feature-Policy:NO" + "\n"
	}

	// https://scotthelme.co.uk/hardening-your-http-response-headers
	list, ok = resp.Header["X-XSS-Protection"]
	if ok && inList("1", list) {
		content += "X-XSS-Protection:YES" + "\n"
	} else {
		content += "X-XSS-Protection:NO" + "\n"
	}

	resp.Body.Close()

	// Checking for security headers regarding HTTPS
	url = "https://" + website

	resp, err = client.Get(url)
	if err != nil {
		content += "SSLerror" + "\n"
		return content
	}
	defer resp.Body.Close()

	// https://scotthelme.co.uk/hpkp-http-public-key-pinning
	content += hasPolicy("Public-Key-Pins", resp)

	// https://scotthelme.co.uk/hsts-preloading
	list, ok = resp.Header["Strict-Transport-Security"]
	if ok {
		content += "HSTS:YES"
		if inList("includeSubDomains", list) {
			content += ":includeSubDomains"
		}
		if inList("preload", list) {
			content += ":preload"
		}
	} else if checkPreloadHSTS(website, "hsts/hsts_preload_firefox.txt") || checkPreloadHSTS(website, "hsts/hsts_preload_google.txt") {
		fmt.Printf("No HSTS header on %s, but it is in the preloaded list from Firefox and/or Google.\n\n", website)
		*preaload += website + "\n"
		content += "HSTS:YES"
	} else {
		content += "HSTS:NO"
	}
	return content + "\n"
}

/*
hasPolicy receive a policy anc connection, and
just check if we receive an error or not. this
function is used if all return values are a
sign of expected security. otherwise, we need
to check manually.
*/

func hasPolicy(policy string, resp *http.Response) string {
	_, ok := resp.Header[policy]
	if ok {
		return policy + ":YES\n"
	}
	return policy + ":NO\n"
}

func inList(val string, list []string) bool {
	for _, element := range list {
		if strings.Contains(element, val) {
			return true
		}
	}
	return false
}
