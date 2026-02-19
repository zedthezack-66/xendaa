"""
consultants.py — Xtenda Finance Loan Consultant Pool
Structure: Province → Town → Branch → List of Consultants

Each consultant has:
  - name: Display name
  - phone: International format (260XXXXXXXXX) — links directly to phone book
  - wa: WhatsApp number (same or different)

Add/remove consultants here. Bot will pick one RANDOMLY from the branch pool.
"""

import random

CONSULTANTS = {
    "🌆 Lusaka Province": {
        "Lusaka": {
            "Cairo Road Branch": [
                {"name": "Chanda Mutale",   "phone": "260971100001"},
                {"name": "Bwalya Mwape",    "phone": "260971100002"},
                {"name": "Namukolo Phiri",  "phone": "260971100003"},
            ],
            "Kalingalinga Branch": [
                {"name": "Mwamba Banda",    "phone": "260971100004"},
                {"name": "Lweendo Siame",   "phone": "260971100005"},
            ],
            "Woodlands Branch": [
                {"name": "Kapambwe Zulu",   "phone": "260971100006"},
                {"name": "Thandiwe Moyo",   "phone": "260971100007"},
            ],
        },
        "Kafue": {
            "Kafue Branch": [
                {"name": "Mulenga Kasonde", "phone": "260971100008"},
                {"name": "Chiluba Tembo",   "phone": "260971100009"},
            ],
        },
        "Chongwe": {
            "Chongwe Branch": [
                {"name": "Mirriam Lungu",   "phone": "260971100010"},
                {"name": "Joseph Sichone",  "phone": "260971100011"},
            ],
        },
    },

    "⛏️ Copperbelt Province": {
        "Kitwe": {
            "Kitwe Central Branch": [
                {"name": "Kelvin Musonda",  "phone": "260971200001"},
                {"name": "Brenda Chiti",    "phone": "260971200002"},
                {"name": "Musa Kabwe",      "phone": "260971200003"},
            ],
            "Nkana East Branch": [
                {"name": "Alice Mwenda",    "phone": "260971200004"},
                {"name": "Felix Chisanga",  "phone": "260971200005"},
            ],
        },
        "Ndola": {
            "Ndola Main Branch": [
                {"name": "Sharon Kabunda",  "phone": "260971200006"},
                {"name": "Patrick Zulu",    "phone": "260971200007"},
            ],
            "Masala Branch": [
                {"name": "Grace Mulwanda",  "phone": "260971200008"},
                {"name": "Dennis Chanda",   "phone": "260971200009"},
            ],
        },
        "Chingola": {
            "Chingola Branch": [
                {"name": "Esther Nkonde",   "phone": "260971200010"},
                {"name": "Ronald Mwape",    "phone": "260971200011"},
            ],
        },
        "Luanshya": {
            "Luanshya Branch": [
                {"name": "Betty Muteba",    "phone": "260971200012"},
                {"name": "George Chileshe", "phone": "260971200013"},
            ],
        },
    },

    "🌿 Southern Province": {
        "Livingstone": {
            "Livingstone Branch": [
                {"name": "Precious Sikaonga", "phone": "260971300001"},
                {"name": "Victor Hamusimbi",  "phone": "260971300002"},
            ],
        },
        "Choma": {
            "Choma Branch": [
                {"name": "Rosemary Mwanza",  "phone": "260971300003"},
                {"name": "Bernard Mudenda",  "phone": "260971300004"},
            ],
        },
        "Mazabuka": {
            "Mazabuka Branch": [
                {"name": "Agatha Hamaundu",  "phone": "260971300005"},
                {"name": "Clement Siame",    "phone": "260971300006"},
            ],
        },
    },

    "🌾 Eastern Province": {
        "Chipata": {
            "Chipata Main Branch": [
                {"name": "Isaac Banda",      "phone": "260971400001"},
                {"name": "Mary Phiri",       "phone": "260971400002"},
                {"name": "Henry Tembo",      "phone": "260971400003"},
            ],
        },
        "Petauke": {
            "Petauke Branch": [
                {"name": "Esnart Zulu",      "phone": "260971400004"},
                {"name": "Kenneth Banda",    "phone": "260971400005"},
            ],
        },
    },

    "🏔️ Northern Province": {
        "Kasama": {
            "Kasama Branch": [
                {"name": "Lilian Mulenga",   "phone": "260971500001"},
                {"name": "Simon Kabwe",      "phone": "260971500002"},
            ],
        },
        "Mpika": {
            "Mpika Branch": [
                {"name": "Anna Chilumba",    "phone": "260971500003"},
                {"name": "David Mwape",      "phone": "260971500004"},
            ],
        },
    },

    "🌊 Western Province": {
        "Mongu": {
            "Mongu Branch": [
                {"name": "Nalumino Liswaniso", "phone": "260971600001"},
                {"name": "Mutumwa Sianga",      "phone": "260971600002"},
            ],
        },
    },

    "🌱 Central Province": {
        "Kabwe": {
            "Kabwe Branch": [
                {"name": "Charity Mwansa",   "phone": "260971700001"},
                {"name": "Maxwell Tembo",    "phone": "260971700002"},
            ],
        },
        "Mkushi": {
            "Mkushi Branch": [
                {"name": "Florence Chungu",  "phone": "260971700003"},
                {"name": "Joseph Ngosa",     "phone": "260971700004"},
            ],
        },
    },

    "🌺 North-Western Province": {
        "Solwezi": {
            "Solwezi Branch": [
                {"name": "Cecilia Kafula",   "phone": "260971800001"},
                {"name": "Daniel Mwanza",    "phone": "260971800002"},
            ],
        },
    },

    "🌻 Luapula Province": {
        "Mansa": {
            "Mansa Branch": [
                {"name": "Harriet Mutale",   "phone": "260971900001"},
                {"name": "Samuel Chanda",    "phone": "260971900002"},
            ],
        },
        "Nchelenge": {
            "Nchelenge Branch": [
                {"name": "Veronica Musonda", "phone": "260971900003"},
                {"name": "Peter Kalaba",     "phone": "260971900004"},
            ],
        },
    },

    "🏝️ Muchinga Province": {
        "Chinsali": {
            "Chinsali Branch": [
                {"name": "Joyce Mulenga",    "phone": "260971010001"},
                {"name": "Abel Chomba",      "phone": "260971010002"},
            ],
        },
    },
}


def get_provinces() -> list[str]:
    return list(CONSULTANTS.keys())


def get_towns(province: str) -> list[str]:
    return list(CONSULTANTS.get(province, {}).keys())


def get_branches(province: str, town: str) -> list[str]:
    return list(CONSULTANTS.get(province, {}).get(town, {}).keys())


def get_random_consultant(province: str, town: str, branch: str) -> dict | None:
    pool = CONSULTANTS.get(province, {}).get(town, {}).get(branch, [])
    if not pool:
        return None
    return random.choice(pool)
