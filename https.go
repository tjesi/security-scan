package main

import (
	"crypto/ecdsa"
	"crypto/rsa"
	"crypto/tls"
	"strconv"
)

/*
https receive the url of a website, connect to the
website and check if it can set up a TLS-connection.
if the website support TLS, we store data about the
TLS-connection and the certificate.
*/

func https(website string) string {

	content := ""

	// we store the session cache to check if we can
	// continue the same session later
	tlsConf := &tls.Config{
		ClientSessionCache: tls.NewLRUClientSessionCache(1),
	}

	con, err := tls.Dial("tcp", website+":443", tlsConf)
	if err == nil {

		// (only) fetch the website's certificate
		cert := con.ConnectionState().PeerCertificates[0]
		content += "Issuer:" + cert.Issuer.Organization[0] + "\n"

		year1, month1, day1 := cert.NotBefore.Date()
		content += "NotBefore:" + strconv.Itoa(year1) + "-" + month1.String() + "-" + strconv.Itoa(day1) + "\n"

		year2, month2, day2 := cert.NotAfter.Date()
		content += "NotAfter:" + strconv.Itoa(year2) + "-" + month2.String() + "-" + strconv.Itoa(day2) + "\n"

		content += "PublicKeyAlgorithm:" + cert.PublicKeyAlgorithm.String() + "\n"

		switch pubKey := cert.PublicKey.(type) {
		case *ecdsa.PublicKey:
			content += "BitSize:" + strconv.Itoa(pubKey.Params().BitSize) + "\n"
		case *rsa.PublicKey:
			content += "BitSize:" + strconv.Itoa(pubKey.N.BitLen()) + "\n"
		}

		content += "SignatureAlgorithm:" + cert.SignatureAlgorithm.String() + "\n"
		content += "Version:" + v[con.ConnectionState().Version] + "\n"
		content += "Ciphersuite:" + id[con.ConnectionState().CipherSuite] + "\n"

		if len(con.ConnectionState().SignedCertificateTimestamps) != 0 {
			content += "Certificate-Transparency:YES\n"
		} else {
			content += "Certificate-Transparency:NO\n"
		}

		if len(con.ConnectionState().OCSPResponse) != 0 {
			content += "OCSPResponse:YES\n"
		} else {
			content += "OCSPResponse:NO\n"
		}

		con.Close()
		con, err := tls.Dial("tcp", website+":443", tlsConf)
		if err == nil {

			// check if session resumpsion is allowed
			// https://tools.ietf.org/html/rfc5077
			content += "SesssionResumpsion:"
			if con.ConnectionState().DidResume {
				content += "YES\n"
			} else {
				content += "NO\n"
			}
			con.Close()
		}
		return content
	}
	return ""
}

// constants from https://golang.org/pkg/crypto/tls
var id = map[uint16]string{

	0x0005: "TLS_RSA_WITH_RC4_128_SHA",
	0x000a: "TLS_RSA_WITH_3DES_EDE_CBC_SHA",
	0x002f: "TLS_RSA_WITH_AES_128_CBC_SHA",
	0x0035: "TLS_RSA_WITH_AES_256_CBC_SHA",
	0x003c: "TLS_RSA_WITH_AES_128_CBC_SHA256",
	0x009c: "TLS_RSA_WITH_AES_128_GCM_SHA256",
	0x009d: "TLS_RSA_WITH_AES_256_GCM_SHA384",
	0xc007: "TLS_ECDHE_ECDSA_WITH_RC4_128_SHA",
	0xc009: "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA",
	0xc00a: "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA",
	0xc011: "TLS_ECDHE_RSA_WITH_RC4_128_SHA",
	0xc012: "TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA",
	0xc013: "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",
	0xc014: "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA",
	0xc023: "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256",
	0xc027: "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256",
	0xc02f: "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256",
	0xc02b: "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256",
	0xc030: "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384",
	0xc02c: "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384",
	0xcca8: "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305",
	0xcca9: "TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305",
	0x5600: "TLS_FALLBACK_SCSV",
}

var v = map[uint16]string{

	0x0300: "VersionSSL30",
	0x0301: "VersionTLS10",
	0x0302: "VersionTLS11",
	0x0303: "VersionTLS12",
}
