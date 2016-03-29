DROP TABLE cage.model ;

CREATE TABLE cage.model(cellType text PRIMARY KEY, refgem text, source text, fileName text,
lastUpdate timestamp, metric text, score double);

