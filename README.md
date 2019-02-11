# security-scan
Tool for scanning websites and checking their security.

## Version 2:

We will:

- Scan top 1 million websites from Alexa, Majestic, Quantcast and Umbrella
- Document the web security by looking at:
  - HTTPS usage (including redirects)
  - HSTS usage (including preloaded in browsers)
  - OSCP stapling usage
  - Certificate Transparency (CT)
  - Other security headers/policies
  - TLS versions
  - Session resumption availability
  - Public key encryption and signing algorithms
  - Symmetric key encryption algorithms and hash-functions
  - Key sizes and modes
  - Certificate validity
    - Is the CA trusted by mainstream browsers?
    - Valid length (3, 6, 9, 12, 15 months etc, not 40 years...)
- Look at trends:
  - Shorter certificate lengths?
  - CA popularity?
  - Increased HTTPS and HSTS usage?
  - Increased TLS 1.3 usage?
  - Increased OSCP/CT usage?
  - Larger keys?
  - ECDH/ECDSA vs RSA vs DH/DSA?
- Compare with other scans like:
  - [crawler.ninja](https://crawler.ninja)
  - [SSL Pulse](https://www.ssllabs.com/ssl-pulse/)
  - [Google Transparency Report](https://transparencyreport.google.com/?hl=en)

## Version 1:

This is what we did:

- Scanned Alexa top 500 most popular websites in 9 countries of interest
- Documented the web security by looking at:
  - HTTPS usage
  - HSTS usage
  - Encryption and signing algorithms
  - Key sizes
  - Certificate validity (naive)
- Published a [short-paper](/papers/short-paper/Where_is_the_web_still_insecure__Regional_scans_for_HTTPS_certificates.pdf)
and [presentation](/presentations/NISK2018/NISK_presentation.pdf) at NISK 2018.

Take a look at the [Python-code and raw data](/archive/Version1_Python).

## Log

- 11.02.19: Updated project description for v2
- 23.01.19: Uploaded top 1 million websites from Alexa, Majestic, Quantcast and Umbrella
- 22.01.19: All previous data is archived. Ready to start v2 of the project.
- 19.09.18: Uploaded presentation at NISK 2018 as PDF, with LaTeX-source and pictures
- 17.09.18: Improved documentation of code and created new issues for further improvement
- 08.08.18: Uploaded short paper, data from previous scans and relevant resources
- 08.08.18: Uploaded all code to scan and obtain raw data

## Installation

- Download and install `Go` from [golang.org](https://golang.org/doc/install)
- Fork and download this repository
- Use command line and `cd` to your local version of the repository
- Type `make run` to run a new scan
