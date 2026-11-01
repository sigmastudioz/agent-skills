# Sigma Sync CLI

Syncs a local folder to S3-compatible storage. Content-hashes every file, uploads only what
changed, and keeps a local manifest so repeat runs are fast.

```sh
sigma sync ./site s3://acme-site
```

Status: private beta, 14 design partners. No public uptime figures are published; the hosted
manifest service has been up since 2026-08-12 with two planned maintenance windows.
Testimonials: none collected yet (first partner interviews are scheduled for 2026-11-18).
