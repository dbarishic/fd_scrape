CREATE TABLE IF NOT EXISTS venue (
    venue_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    v_name varchar(250) NOT NULL,
    address varchar(250),
    google_maps_url varchar(250),
    arrival_parking_info TEXT,
    cloakroom TEXT,
    gastronomy TEXT,
    wheelchair_access TEXT,
    late_admission_info TEXT
);

CREATE TABLE IF NOT EXISTS performer (
    performer_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    p_name varchar(250) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS event (
    event_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title varchar(250) NOT NULL,
    image_url varchar(250),
    e_date DATE,
    e_time TIME,
    description TEXT,
    program varchar(250),
    festival varchar(100),
    ticket_purchase_url varchar(250),
    venue_id uuid REFERENCES venue(venue_id),
    price numeric(15, 2), /* This doesn't handle differentcurrencies and treats everything as CHF for simplicity's (and time) sake */
    performer_id uuid REFERENCES performer(performer_id)
);