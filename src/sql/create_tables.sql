CREATE TABLE IF NOT EXISTS venue (
    venue_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    v_name varchar NOT NULL,
    address varchar,
    google_maps_url varchar,
    arrival_parking_info TEXT,
    cloakroom TEXT,
    gastronomy TEXT,
    wheelchair_access TEXT,
    late_admission_info TEXT
);

CREATE TABLE IF NOT EXISTS performer (
    performer_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    p_name varchar NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS event (
    event_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title varchar NOT NULL,
    image_url varchar,
    e_date DATE,
    e_time TIME,
    description TEXT,
    program varchar,
    festival varchar,
    ticket_purchase_url varchar,
    venue_id uuid REFERENCES venue(venue_id),
    price numeric(15, 2), /* This doesn't handle differentcurrencies and treats everything as CHF for simplicity's (and time) sake */
    performer_id uuid REFERENCES performer(performer_id)
);

CREATE TABLE IF NOT EXISTS event_performer (
    event_id uuid REFERENCES event(event_id),
    performer_id uuid REFERENCES performer(performer_id),
    CONSTRAINT event_performer_pkey PRIMARY KEY (event_id, performer_id)
);