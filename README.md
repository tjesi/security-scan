# security-scan
Tool for scanning websites and check their security.

## Version 2:

We will:

- Scan top 1 million websites from Alexa, Majestic, Quantcast and Umbrella
- Document the web security by looking at:
  - HTTPS usage (including re-directs)
  - HSTS usage (including preloaded in browsers)
  - OSCP stapling usage
  - Certificate Transparency
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
  - Larger keys?
  - ECC vs RSA?

## Version 1:

This is what we did:

- Scanned Alexa top 500 most popular websites in 9 countries of interest
- Documented the web security by looking at:
  - HTTPS usage
  - HSTS usage
  - Encryption and signing algorithms
  - Key sizes
  - Certificate validity (naive)
- Published a [short-paper at NISK 2018](/papers/short-paper/Where_is_the_web_still_insecure__Regional_scans_for_HTTPS_certificates.pdf).

Take a look at the [Python-code and raw data](/archive/Version1_Python).

## Log

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
