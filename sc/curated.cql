DROP TABLE cage.curated ;

CREATE TABLE cage.curated(id uuid PRIMARY KEY, species text, cellType text, dataName text,
lastUpdate timestamp, name text, org text, publication text);


