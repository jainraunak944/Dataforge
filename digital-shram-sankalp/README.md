# Digital Shram Sankalp submission package (encrypted)

This folder holds one AES-256 encrypted bundle, `DSS_Submission_Package.tar.gz.enc`.
The competition requires the entries to stay confidential and this repository is public,
so the plaintext files (twelve PDFs, the editable deck, the combined PDF, the canonical
text, the private guide and the generator scripts) are not committed here.

Decrypt with the passphrase provided privately:

    openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -in DSS_Submission_Package.tar.gz.enc | tar xzf -

This extracts `output/submission/`, `output/private/`, `build/` and `DSS_Submission_Package.zip`.
Regenerate after edits with `python3 build/wordcount.py && python3 build/export.py && python3 build/make_guide.py && python3 build/package.py`
(needs python-pptx, pypdf, PyMuPDF and LibreOffice Impress).
