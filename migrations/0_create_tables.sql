CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY,
    filename VARCHAR NOT NULL UNIQUE,
    storagePath VARCHAR UNIQUE NOT NULL,
);

CREATE TABLE IF NOT EXISTS pages (
    id UUID PRIMARY KEY,
    documentId UUID REFERENCES documents(id),
    storagePath VARCHAR UNIQUE NOT NULL,
    pageNumber INT 
);

CREATE TABLE IF NOT EXISTS pages_with_boxes (
    pageId UUID REFERENCES pages(id),
    storagePath VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS figures (
    id UUID PRIMARY KEY,
    pageId UUID REFERENCES pages(id),
    storagePath VARCHAR UNIQUE NOT NULL,
    n INT 
);

CREATE TABLE IF NOT EXISTS markdowns (
    pageId UUID REFERENCES pages(id),
    content VARCHAR NOT NULL
);