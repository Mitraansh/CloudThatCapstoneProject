from Backend import db, auth


def seed_data() -> None:
    db.initialize_database()
    db.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", ("Roses", "Classic rose bouquets."))
    db.execute("INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)", ("Seasonal", "Seasonal flowers and arrangements."))
    db.execute(
        "INSERT OR IGNORE INTO flowers (name, category_id, price, stock, description, season) VALUES (?, ?, ?, ?, ?, ?)",
        ("Red Rose", 1, 39.99, 10, "Fresh red roses for romance .", "Valentine"),
    )
    db.execute(
        "INSERT OR IGNORE INTO flowers (name, category_id, price, stock, description, season) VALUES (?, ?, ?, ?, ?, ?)",
        ("Tulip Bouquet", 2, 29.99, 4, "Bright mixed tulips for spring.", "Spring"),
    )
    db.execute(
        "INSERT OR IGNORE INTO care_instructions (flower_id, topic, content) VALUES (?, ?, ?)",
        (1, "water", "Keep roses hydrated with fresh water daily."),
    )
    db.execute(
        "INSERT OR IGNORE INTO care_instructions (flower_id, topic, content) VALUES (?, ?, ?)",
        (2, "sunlight", "Tulips enjoy bright, indirect sunlight."),
    )
    db.execute(
        "INSERT OR IGNORE INTO promotions (code, description, discount_percent, active) VALUES (?, ?, ?, ?)",
        ("SPRING10", "10% off seasonal bouquets", 10, 1),
    )
    db.execute(
        "INSERT OR IGNORE INTO support_articles (title, content) VALUES (?, ?)",
        ("Flower care tips", "Keep stems clean and change water every two days."),
    )


if __name__ == "__main__":
    seed_data()
    print("Seed data loaded.")
