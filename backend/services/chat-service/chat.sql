-- Create the database
CREATE DATABASE fitplan_chat;

-- Connect to the new database
\c fitplan_chat;

--**********************************************************************************************

CREATE TABLE IF NOT EXISTS users
(
    id         INT PRIMARY KEY NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS coach
(
    id         INT PRIMARY KEY NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS admin
(
    id         INT PRIMARY KEY NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS user_coach_chat
(
    id            SERIAL PRIMARY KEY,
    user_id       INT         NOT NULL,
    coach_id      INT         NOT NULL,
    content       TEXT        NOT NULL,
    sender_type   VARCHAR(10) NOT NULL,
    receiver_type VARCHAR(10) NOT NULL,
    date          VARCHAR(55),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (coach_id) REFERENCES coach (id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS user_coach_with
(
    user_id INT PRIMARY KEY NOT NULL,
    coach_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS admin_user_chat
(
    id            SERIAL PRIMARY KEY,
    user_id       INT         NOT NULL,
    admin_id      INT         NOT NULL,
    content       TEXT        NOT NULL,
    sender_type   VARCHAR(10) NOT NULL,
    receiver_type VARCHAR(10) NOT NULL,
    date          VARCHAR(55),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES admin (id) ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS admin_coach_chat
(
    id            SERIAL PRIMARY KEY,
    coach_id      INT        NOT NULL,
    admin_id      INT         NOT NULL,
    content       TEXT        NOT NULL,
    sender_type   VARCHAR(10) NOT NULL,
    receiver_type VARCHAR(10) NOT NULL,
    date          VARCHAR(55),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (coach_id) REFERENCES coach (id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES admin (id) ON DELETE CASCADE
);