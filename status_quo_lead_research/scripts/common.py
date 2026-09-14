#!/usr/bin/env python3
"""Shared normalization and parsing helpers for the Status Quo lead pipeline.

Every canonical field the later stages rely on is derived here, so normalization
is defined in exactly one place and the audit, dedupe, prefilter and research
stages cannot drift apart.
"""
from __future__ import annotations
import re, csv, sys, unicodedata
from pathlib import Path
from urllib.parse import urlsplit

csv.field_size_limit(sys.maxsize)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
CANONICAL_CSV = DATA / "us-software-saas-companies-cleaned.csv"
DB_PATH = ROOT / "research_state.sqlite"

# ---------------------------------------------------------------- country ----
# The dataset mixes full country names with ISO-3166 alpha-2 codes, in mixed case.
ISO2 = {
    "US": "United States", "PR": "Puerto Rico", "VI": "U.S. Virgin Islands",
    "GB": "United Kingdom", "CA": "Canada", "IL": "Israel", "IN": "India",
    "DE": "Germany", "AU": "Australia", "FR": "France", "CN": "China",
    "NL": "Netherlands", "CH": "Switzerland", "DK": "Denmark", "PK": "Pakistan",
    "SE": "Sweden", "JP": "Japan", "BE": "Belgium", "BR": "Brazil", "IT": "Italy",
    "AE": "United Arab Emirates", "IE": "Ireland", "ES": "Spain", "TW": "Taiwan",
    "MX": "Mexico", "TR": "Turkey", "KR": "South Korea", "FI": "Finland",
    "NO": "Norway", "ZA": "South Africa", "NZ": "New Zealand", "CO": "Colombia",
    "AT": "Austria", "PL": "Poland", "BD": "Bangladesh", "AR": "Argentina",
    "EE": "Estonia", "CZ": "Czechia", "NG": "Nigeria", "EG": "Egypt",
    "HK": "Hong Kong", "ID": "Indonesia", "RO": "Romania", "PT": "Portugal",
    "SA": "Saudi Arabia", "CY": "Cyprus", "RU": "Russia", "KE": "Kenya",
    "LK": "Sri Lanka", "CL": "Chile", "PE": "Peru", "MY": "Malaysia",
    "CR": "Costa Rica", "PH": "Philippines", "KZ": "Kazakhstan", "BG": "Bulgaria",
    "IR": "Iran", "QA": "Qatar", "VE": "Venezuela", "GH": "Ghana", "HU": "Hungary",
    "UA": "Ukraine", "LV": "Latvia", "MT": "Malta", "JO": "Jordan", "HR": "Croatia",
    "SI": "Slovenia", "GR": "Greece", "TH": "Thailand", "VN": "Vietnam",
    "LU": "Luxembourg", "LT": "Lithuania", "TZ": "Tanzania", "AM": "Armenia",
    "TN": "Tunisia", "SK": "Slovakia", "BY": "Belarus", "ZW": "Zimbabwe",
    "ZM": "Zambia", "OM": "Oman", "KW": "Kuwait", "PA": "Panama",
    "AZ": "Azerbaijan", "LB": "Lebanon", "AO": "Angola", "VG": "British Virgin Islands",
    "LI": "Liechtenstein", "EC": "Ecuador", "IQ": "Iraq", "JE": "Jersey",
    "MC": "Monaco", "BO": "Bolivia", "SC": "Seychelles", "NP": "Nepal",
    "MU": "Mauritius", "RS": "Serbia", "GE": "Georgia", "XK": "Kosovo",
    "SY": "Syria", "TT": "Trinidad and Tobago", "SN": "Senegal", "CM": "Cameroon",
    "SD": "Sudan", "UY": "Uruguay", "CG": "Congo", "DZ": "Algeria",
    "HN": "Honduras", "IS": "Iceland", "KH": "Cambodia", "GI": "Gibraltar",
    "MZ": "Mozambique", "AL": "Albania", "BS": "Bahamas", "BH": "Bahrain",
    "SG": "Singapore",
}
US_NAMES = {"united states", "us", "usa", "u.s.", "u.s.a.", "united states of america",
            "america", "united  states"}
# US territories: American businesses for our purposes, but flagged for verification.
US_TERRITORIES = {"puerto rico", "u.s. virgin islands", "guam", "american samoa",
                  "northern mariana islands"}

def normalize_country(raw: str) -> str:
    """Canonical country name, or '' when unknown."""
    if not raw:
        return ""
    s = raw.strip()
    if not s:
        return ""
    if len(s) == 2 and s.upper() in ISO2:
        return ISO2[s.upper()]
    low = s.lower().strip(". ")
    if low in US_NAMES or low.replace(".", "") in {"us", "usa"}:
        return "United States"
    return s.strip()

def us_status(country_norm: str) -> str:
    """'us' | 'us_territory' | 'foreign' | 'unknown'"""
    if not country_norm:
        return "unknown"
    low = country_norm.lower()
    if low == "united states":
        return "us"
    if low in US_TERRITORIES:
        return "us_territory"
    return "foreign"

# ----------------------------------------------------------------- domain ----
_TLDX = None
def _tldextract():
    global _TLDX
    if _TLDX is None:
        import tldextract
        # suffix_list_urls=None -> use the bundled snapshot, no network at runtime
        _TLDX = tldextract.TLDExtract(suffix_list_urls=None)
    return _TLDX

PLATFORM_DOMAINS = {
    "myshopify.com", "wixsite.com", "squarespace.com", "weebly.com", "github.io",
    "wordpress.com", "blogspot.com", "webflow.io", "netlify.app", "vercel.app",
    "herokuapp.com", "azurewebsites.net", "firebaseapp.com", "web.app",
    "godaddysites.com", "business.site", "glideapp.io", "bubbleapps.io",
    "notion.site", "carrd.co", "framer.website", "sites.google.com",
    "wpcomstaging.com", "hubspotpagebuilder.com", "pages.dev", "onrender.com",
    "yolasite.com", "lpages.co", "clickfunnels.com", "leadpages.co", "site123.me",
    "strikingly.com", "tilda.ws", "mystrikingly.com", "websitebuilder.com",
}

def normalize_domain(raw: str) -> str:
    """Lowercase registrable domain: no protocol, no www., no path/query/port."""
    if not raw:
        return ""
    s = raw.strip().lower()
    if not s or s in {"-", "n/a", "na", "none", "null"}:
        return ""
    if "://" not in s:
        s = "http://" + s
    try:
        host = urlsplit(s).hostname or ""
    except ValueError:
        return ""
    if not host:
        return ""
    host = host.strip(".")
    if host.startswith("www."):
        host = host[4:]
    ext = _tldextract()(host)
    if ext.domain and ext.suffix:
        registrable = f"{ext.domain}.{ext.suffix}".lower()
        # On shared hosting the registrable domain identifies the platform, not the
        # company, so keep the full host to avoid merging unrelated businesses.
        if registrable in PLATFORM_DOMAINS and ext.subdomain:
            return host.lower()
        return registrable
    return host.lower()

def website_url(domain_norm: str) -> str:
    return f"https://{domain_norm}" if domain_norm else ""

# --------------------------------------------------------------- linkedin ----
_LI_RE = re.compile(r"linkedin\.com/(?:company|school|showcase)/([^/?#]+)", re.I)

def normalize_linkedin(raw: str) -> tuple[str, str]:
    """Return (canonical_url, slug). Strips tracking params and trailing slashes."""
    if not raw:
        return "", ""
    s = raw.strip()
    if not s:
        return "", ""
    m = _LI_RE.search(s)
    if not m:
        return "", ""
    slug = m.group(1).strip().strip("/").lower()
    try:
        from urllib.parse import unquote
        slug = unquote(slug)
    except Exception:
        pass
    if not slug:
        return "", ""
    return f"https://www.linkedin.com/company/{slug}", slug

def valid_url(raw: str) -> bool:
    if not raw:
        return False
    s = raw.strip()
    if "://" not in s:
        s = "http://" + s
    try:
        parts = urlsplit(s)
    except ValueError:
        return False
    return bool(parts.hostname) and "." in (parts.hostname or "")

# ------------------------------------------------------------- company name --
LEGAL_SUFFIXES = [
    "incorporated", "corporation", "limited liability company", "llc", "l.l.c",
    "inc", "corp", "ltd", "limited", "co", "plc", "gmbh", "bv", "b.v", "nv",
    "ag", "sa", "s.a", "srl", "s.r.l", "pty", "pte", "llp", "lp", "pc",
    "holdings", "holding", "group",
]
_PUNCT_RE = re.compile(r"[^\w\s&]+", re.UNICODE)
_WS_RE = re.compile(r"\s+")

def normalize_company_name(raw: str) -> str:
    """Lowercased, de-punctuated, legal-suffix-stripped name for duplicate matching."""
    if not raw:
        return ""
    s = unicodedata.normalize("NFKD", raw)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = s.replace("&", " and ")
    s = _PUNCT_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    if s.startswith("the "):
        s = s[4:]
    changed = True
    while changed and s:
        changed = False
        for suf in LEGAL_SUFFIXES:
            if s.endswith(" " + suf):
                s = s[: -(len(suf) + 1)].strip()
                changed = True
    return _WS_RE.sub(" ", s).strip()

# --------------------------------------------------------------- employees ----
_RANGE_MAP = {
    "0-1 employees": (0, 1),
    "2-10 employees": (2, 10),
    "11-50 employees": (11, 50),
    "51-200 employees": (51, 200),
    "201-500 employees": (201, 500),
    "501-1,000 employees": (501, 1000),
    "1,001-5,000 employees": (1001, 5000),
    "5,001-10,000 employees": (5001, 10000),
    "10,001+ employees": (10001, 100000),
    "self-employed": (1, 1),
}

def parse_employee_range(raw: str):
    if not raw:
        return (None, None, "")
    key = raw.strip().lower()
    if key in _RANGE_MAP:
        lo, hi = _RANGE_MAP[key]
        return (lo, hi, raw.strip())
    return (None, None, raw.strip())

def parse_headcount(raw: str):
    if raw is None:
        return None
    s = str(raw).strip().replace(",", "")
    if not s:
        return None
    try:
        v = int(float(s))
    except ValueError:
        return None
    return v if v >= 0 else None

TARGET_EMP_LOW, TARGET_EMP_HIGH = 11, 50

def employee_assessment(headcount, range_low, range_high):
    """Return (initial_fit, conflict, verification_required).

    initial_fit: 'in_range' | 'below' | 'above' | 'unknown'
    Numeric headcount and the size band are both treated as estimates; where they
    disagree the row is kept and flagged rather than silently resolved in whichever
    direction would make the company qualify.
    """
    hc_fit = None
    if headcount is not None and headcount > 0:
        hc_fit = "in_range" if TARGET_EMP_LOW <= headcount <= TARGET_EMP_HIGH else (
            "below" if headcount < TARGET_EMP_LOW else "above")
    rg_fit = None
    if range_low is not None:
        overlaps = not (range_high < TARGET_EMP_LOW or range_low > TARGET_EMP_HIGH)
        rg_fit = "in_range" if overlaps else ("below" if range_high < TARGET_EMP_LOW else "above")

    conflict = bool(hc_fit and rg_fit and hc_fit != rg_fit)
    if hc_fit and rg_fit:
        if not conflict:
            return hc_fit, False, hc_fit != "in_range" and False
        # Conflict: keep if either estimate lands in range, and demand verification.
        fit = "in_range" if "in_range" in (hc_fit, rg_fit) else hc_fit
        return fit, True, True
    if hc_fit:
        return hc_fit, False, True
    if rg_fit:
        return rg_fit, False, True
    return "unknown", False, True

# ----------------------------------------------------------------- revenue ----
_REV_MAP = {
    "0-500K": (0, 500_000), "500K-1M": (500_000, 1_000_000),
    "1M-5M": (1_000_000, 5_000_000), "5M-10M": (5_000_000, 10_000_000),
    "10M-25M": (10_000_000, 25_000_000), "25M-75M": (25_000_000, 75_000_000),
    "75M-200M": (75_000_000, 200_000_000), "200M-500M": (200_000_000, 500_000_000),
    "500M-1B": (500_000_000, 1_000_000_000), "1B-10B": (1_000_000_000, 10_000_000_000),
    "10B-100B": (10_000_000_000, 100_000_000_000),
    "100B-1T": (100_000_000_000, 1_000_000_000_000),
}

def parse_revenue(raw: str):
    """Return (band, low, high, midpoint). All values are ESTIMATES, never confirmed."""
    if not raw:
        return ("", None, None, None)
    band = raw.strip()
    if band in _REV_MAP:
        lo, hi = _REV_MAP[band]
        return (band, lo, hi, (lo + hi) / 2)
    return (band, None, None, None)

# ----------------------------------------------------------------- funding ----
_FUND_MAP = {
    "Under $1M": (0, 1_000_000), "$1M - $5M": (1_000_000, 5_000_000),
    "$5M - $10M": (5_000_000, 10_000_000), "$10M - $25M": (10_000_000, 25_000_000),
    "$25M - $50M": (25_000_000, 50_000_000), "$50M - $100M": (50_000_000, 100_000_000),
    "$100M - $250M": (100_000_000, 250_000_000), "$250M+": (250_000_000, None),
    "Funding unknown": (None, None),
}

def parse_funding(raw: str):
    if not raw:
        return ("", None, None)
    band = raw.strip()
    if band in _FUND_MAP:
        lo, hi = _FUND_MAP[band]
        return (band, lo, hi)
    return (band, None, None)

# ------------------------------------------------------------------- misc ----
def parse_year(raw: str):
    if not raw:
        return None
    m = re.search(r"(1[89]\d{2}|20[0-4]\d)", str(raw))
    return int(m.group(1)) if m else None

def parse_int(raw: str):
    if raw is None:
        return None
    s = str(raw).strip().replace(",", "")
    if not s:
        return None
    try:
        return int(float(s))
    except ValueError:
        return None

US_STATE_ABBR = {
 "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS",
 "KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY",
 "NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV",
 "WI","WY","DC","PR","VI","GU"}
US_STATE_NAMES = {
 "alabama","alaska","arizona","arkansas","california","colorado","connecticut",
 "delaware","florida","georgia","hawaii","idaho","illinois","indiana","iowa",
 "kansas","kentucky","louisiana","maine","maryland","massachusetts","michigan",
 "minnesota","mississippi","missouri","montana","nebraska","nevada",
 "new hampshire","new jersey","new mexico","new york","north carolina",
 "north dakota","ohio","oklahoma","oregon","pennsylvania","rhode island",
 "south carolina","south dakota","tennessee","texas","utah","vermont","virginia",
 "washington","west virginia","wisconsin","wyoming","district of columbia",
 "puerto rico"}

def locality_looks_us(locality: str) -> bool:
    """True when a locality string clearly names a US state or DC."""
    if not locality:
        return False
    parts = [p.strip() for p in re.split(r"[,/|]", locality) if p.strip()]
    for p in parts:
        if p.upper() in US_STATE_ABBR and len(p) == 2:
            return True
        if p.lower() in US_STATE_NAMES:
            return True
    return False

def open_canonical():
    return CANONICAL_CSV.open("r", newline="", encoding="utf-8")
