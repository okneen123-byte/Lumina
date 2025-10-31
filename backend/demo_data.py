# backend/demo_data.py
# ====================================================
# Lumina News – Offline-Demo-Datenbank
# Enthält Beispielnachrichten für alle Kategorien
# in Deutsch und Englisch.
# ====================================================

demo_news = {
    "general": {
        "de": [
            {
                "title": "Künstliche Intelligenz verändert die Arbeitswelt",
                "description": "Immer mehr Unternehmen setzen KI zur Automatisierung und Entscheidungsfindung ein.",
                "url": "https://www.handelsblatt.com/technik/kuenstliche-intelligenz/",
                "importance": 8.9,
                "published_at": "2025-10-29"
            },
            {
                "title": "Deutschland plant neue Energiepolitik",
                "description": "Die Bundesregierung will den Ausbau erneuerbarer Energien drastisch beschleunigen.",
                "url": "https://www.tagesschau.de/inland/energiewende-deutschland-101.html",
                "importance": 8.2,
                "published_at": "2025-10-28"
            }
        ],
        "en": [
            {
                "title": "AI reshapes the global workforce",
                "description": "Companies worldwide adopt AI to improve efficiency and cut costs.",
                "url": "https://www.bbc.com/news/technology",
                "importance": 8.7,
                "published_at": "2025-10-29"
            },
            {
                "title": "Europe launches new climate plan",
                "description": "EU leaders agreed on a stronger commitment to renewable energy.",
                "url": "https://www.theguardian.com/environment/",
                "importance": 8.3,
                "published_at": "2025-10-28"
            }
        ]
    },
    "business": {
        "de": [
            {
                "title": "DAX erreicht neues Rekordhoch",
                "description": "Die deutschen Aktienmärkte profitieren von starken Quartalszahlen.",
                "url": "https://www.faz.net/aktuell/finanzen/",
                "importance": 8.1,
                "published_at": "2025-10-30"
            },
            {
                "title": "Amazon expandiert weiter in Europa",
                "description": "Der US-Konzern plant neue Logistikzentren in Deutschland und Frankreich.",
                "url": "https://www.manager-magazin.de/",
                "importance": 7.8,
                "published_at": "2025-10-29"
            }
        ],
        "en": [
            {
                "title": "Stock markets hit record highs",
                "description": "Investors show confidence despite global uncertainty.",
                "url": "https://edition.cnn.com/business",
                "importance": 8.0,
                "published_at": "2025-10-30"
            },
            {
                "title": "Tesla announces new European factory",
                "description": "The EV giant expands production capacity in Germany.",
                "url": "https://www.reuters.com/business/autos-transportation/",
                "importance": 8.2,
                "published_at": "2025-10-28"
            }
        ]
    },
    "technology": {
        "de": [
            {
                "title": "Apple stellt revolutionäres AR-Headset vor",
                "description": "Das neue Gerät soll Arbeit und Freizeit in virtuellen Welten verbinden.",
                "url": "https://www.heise.de/news/",
                "importance": 9.0,
                "published_at": "2025-10-29"
            },
            {
                "title": "Europäische Raumfahrtagentur testet KI im All",
                "description": "Neue Satelliten sollen mit autonomen Entscheidungsmodulen ausgerüstet werden.",
                "url": "https://www.spiegel.de/wissenschaft/",
                "importance": 8.5,
                "published_at": "2025-10-28"
            }
        ],
        "en": [
            {
                "title": "Google unveils next-gen AI chip",
                "description": "The new Tensor chip promises faster AI processing and energy savings.",
                "url": "https://techcrunch.com/",
                "importance": 9.1,
                "published_at": "2025-10-30"
            },
            {
                "title": "NASA uses AI to plan Mars missions",
                "description": "Machine learning helps optimize mission routes and save fuel.",
                "url": "https://www.nasa.gov/",
                "importance": 8.6,
                "published_at": "2025-10-28"
            }
        ]
    },
    "sports": {
        "de": [
            {
                "title": "Deutschland gewinnt Nations League",
                "description": "Die deutsche Nationalmannschaft feiert ein starkes Comeback.",
                "url": "https://www.kicker.de/",
                "importance": 8.7,
                "published_at": "2025-10-27"
            },
            {
                "title": "Lewis Hamilton kündigt Karriereende an",
                "description": "Der siebenfache Weltmeister verlässt die Formel 1 nach der Saison 2025.",
                "url": "https://www.sport1.de/",
                "importance": 9.2,
                "published_at": "2025-10-30"
            }
        ],
        "en": [
            {
                "title": "Manchester City wins Champions League",
                "description": "City secures their second consecutive European title.",
                "url": "https://www.espn.com/",
                "importance": 9.3,
                "published_at": "2025-10-30"
            },
            {
                "title": "US sprinter breaks 100m world record",
                "description": "A new era begins in track and field with record-breaking performance.",
                "url": "https://www.bbc.com/sport",
                "importance": 8.8,
                "published_at": "2025-10-29"
            }
        ]
    },
    "science": {
        "de": [
            {
                "title": "Forscher entdecken mögliches Heilmittel gegen Alzheimer",
                "description": "Ein neues Medikament zeigt beeindruckende Ergebnisse in klinischen Studien.",
                "url": "https://www.spektrum.de/",
                "importance": 9.0,
                "published_at": "2025-10-29"
            },
            {
                "title": "Klimawandel: 2025 war eines der heißesten Jahre",
                "description": "Globale Temperaturen erreichen Rekordwerte, warnen Experten.",
                "url": "https://www.tagesspiegel.de/",
                "importance": 8.5,
                "published_at": "2025-10-28"
            }
        ],
        "en": [
            {
                "title": "Scientists develop new Alzheimer treatment",
                "description": "Early results show a potential breakthrough in neurodegenerative research.",
                "url": "https://www.nature.com/",
                "importance": 9.1,
                "published_at": "2025-10-29"
            },
            {
                "title": "Earth records warmest year ever",
                "description": "Global temperatures hit unprecedented highs in 2025.",
                "url": "https://www.nationalgeographic.com/",
                "importance": 8.7,
                "published_at": "2025-10-28"
            }
        ]
    },
    "entertainment": {
        "de": [
            {
                "title": "Neue Netflix-Serie begeistert Zuschauer weltweit",
                "description": "Die Sci-Fi-Serie 'Eclipse' wird zum globalen Streaming-Erfolg.",
                "url": "https://www.filmstarts.de/",
                "importance": 8.9,
                "published_at": "2025-10-30"
            }
        ],
        "en": [
            {
                "title": "Hollywood embraces AI in film production",
                "description": "Studios use AI to optimize visual effects and post-production.",
                "url": "https://variety.com/",
                "importance": 8.5,
                "published_at": "2025-10-29"
            }
        ]
    },
    "powi": {  # Politik / Wirtschaft Unterricht
        "de": [
            {
                "title": "Bundestag diskutiert über neue Bildungsoffensive",
                "description": "Politiker fordern mehr digitale Ausstattung für Schulen.",
                "url": "https://www.bundesregierung.de/",
                "importance": 8.4,
                "published_at": "2025-10-29"
            },
            {
                "title": "Inflation sinkt in Deutschland auf 2,1 Prozent",
                "description": "Ökonomen sehen eine Trendwende bei den Verbraucherpreisen.",
                "url": "https://www.tagesschau.de/wirtschaft/",
                "importance": 8.2,
                "published_at": "2025-10-28"
            }
        ],
        "en": [
            {
                "title": "Germany debates new education reform",
                "description": "Government pushes for more digital tools in classrooms.",
                "url": "https://www.dw.com/en/",
                "importance": 8.5,
                "published_at": "2025-10-29"
            },
            {
                "title": "European inflation slows down",
                "description": "Experts predict stable economic growth across the Eurozone.",
                "url": "https://www.ft.com/",
                "importance": 8.0,
                "published_at": "2025-10-28"
            }
        ]
    }
}
