CREATE TABLE IF NOT EXISTS recipes (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  url TEXT,
  total_time_min INTEGER
);

CREATE TABLE IF NOT EXISTS recipe_ingredients (
  id INTEGER PRIMARY KEY,
  recipe_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  quantity REAL,
  unit TEXT,
  FOREIGN KEY(recipe_id) REFERENCES recipes(id)
);

CREATE INDEX IF NOT EXISTS idx_ing_name ON recipe_ingredients(name);

