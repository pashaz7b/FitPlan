-- Create the database
CREATE DATABASE fitplan_db;

-- Connect to the new database
\c fitplan_db;

--**********************************************************************************************

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

--**********************************************************************************************
 
CREATE TABLE admin (
    id SERIAL PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    gender VARCHAR(10),
    date_of_birth VARCHAR(15),
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified boolean DEFAULT false
);


CREATE TRIGGER set_timestamp_admin
BEFORE UPDATE ON admin
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

--**********************************************************************************************

CREATE TABLE coach (
    id SERIAL PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20) NOT NULL UNIQUE,
    gender VARCHAR(10),
    status boolean DEFAULT false,
    date_of_birth VARCHAR(15),
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified boolean DEFAULT false,
    verification_status VARCHAR(50) DEFAULT 'pending'
);


CREATE TABLE coach_metrics (
    id SERIAL PRIMARY KEY,
    coach_id INT UNIQUE, -- 1-to-1 relation with Coach table
    height DECIMAL(5, 2), -- Height in cm
    weight DECIMAL(5, 2), -- Weight in kg
    specialization VARCHAR(255), -- E.g., fitness, strength training, etc.
    biography TEXT, -- Brief biography of the coach
    rating INTEGER DEFAULT 0 CHECK (rating BETWEEN 0 AND 5),
    coaching_id VARCHAR(100),
    coaching_card_image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (coach_id) REFERENCES coach(id) ON DELETE CASCADE
);


CREATE TRIGGER set_timestamp_coach
BEFORE UPDATE ON coach
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE TRIGGER set_timestamp_coach_metrics
BEFORE UPDATE ON coach_metrics
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

--**********************************************************************************************

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    user_name VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone_number VARCHAR(20) UNIQUE,
    gender VARCHAR(10),
    date_of_birth VARCHAR(15),
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified boolean DEFAULT false
);


CREATE TABLE user_metrics (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE,  -- This is the 1-to-1 relation to the User table
    height DECIMAL(5, 2), -- Height in cm (or other units as needed)
    weight DECIMAL(5, 2), -- Weight in kg (or other units as needed)
    waist DECIMAL(5, 2), -- Waist measurement in cm
    injuries TEXT,  -- Any description of injuries
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


CREATE TRIGGER set_timestamp_user
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE TRIGGER set_timestamp_user_metrics
BEFORE UPDATE ON user_metrics
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

--**********************************************************************************************

CREATE TABLE transaction_log (
    id SERIAL PRIMARY KEY,
    amount DECIMAL(10, 2) NOT NULL,
    reason VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    date TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TRIGGER set_timestamp_transaction_log
BEFORE UPDATE ON transaction_log
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE TABLE user_transaction_log(
    transaction_id INT NOT NULL,
    user_id INT NOT NULL,
    PRIMARY KEY(transaction_id),
    FOREIGN KEY (transaction_id) REFERENCES transaction_log(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

--**********************************************************************************************

CREATE TABLE workout_plan (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,                 
    duration_month INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER set_timestamp_workout_plan
BEFORE UPDATE ON workout_plan
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE TABLE take (
    user_id INT Not NULL,
    workout_plan_id INT Not NULL,
    PRIMARY KEY (user_id, workout_plan_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (workout_plan_id) REFERENCES workout_plan(id) ON DELETE CASCADE
);


CREATE TABLE present (
    coach_id INT NOT NULL,
    workout_plan_id INT NOT NULL,
    PRIMARY KEY (workout_plan_id),
    FOREIGN KEY (coach_id) REFERENCES coach(id) ON DELETE CASCADE,
    FOREIGN KEY (workout_plan_id) REFERENCES workout_plan(id) ON DELETE CASCADE
);

--**********************************************************************************************

CREATE TABLE class_time (
    id SERIAL PRIMARY KEY,
    day VARCHAR(50) NOT NULL,
    hour TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TRIGGER set_timestamp_class_time
BEFORE UPDATE ON class_time
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();



CREATE TABLE workout_plan_class_time (
    workout_plan_id INT NOT Null,
    class_time_id INT NOT Null,
    PRIMARY KEY (workout_plan_id, class_time_id),
    FOREIGN KEY (workout_plan_id) REFERENCES workout_plan(id) ON DELETE CASCADE,
    FOREIGN KEY (class_time_id) REFERENCES class_time(id) ON DELETE CASCADE
);

--**********************************************************************************************

CREATE TABLE user_exercise (
    id SERIAL PRIMARY KEY,
    weight DECIMAL(5, 2) NOT NULL,
    waist DECIMAL(5, 2) NOT NULL,
    type VARCHAR(10) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TRIGGER set_timestamp_user_exercise
BEFORE UPDATE ON user_exercise
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE TABLE user_request_exercise(
    user_id INT NOT Null,
    user_exercise_id INT NOT Null,
    PRIMARY KEY (user_exercise_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user_exercise_id) REFERENCES user_exercise(id) ON DELETE CASCADE
);

--**********************************************************************************************


CREATE TABLE exercise (
    id SERIAL PRIMARY KEY,
    day VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    set VARCHAR(100) NOT NULL,
    expire_time INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TRIGGER set_timestamp_exercise
BEFORE UPDATE ON exercise
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();



CREATE TABLE user_exercise_exercise(
    exercise_id INT NOT Null,
    user_exercise_id INT NOT Null,
    PRIMARY KEY (exercise_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(id) ON DELETE CASCADE,
    FOREIGN KEY (user_exercise_id) REFERENCES user_exercise(id) ON DELETE CASCADE
);


CREATE TABLE workout_plan_exercise(
    exercise_id INT NOT Null,
    workout_plan_id INT NOT Null,
    PRIMARY KEY (exercise_id, workout_plan_id),
    FOREIGN KEY (exercise_id) REFERENCES exercise(id) ON DELETE CASCADE,
    FOREIGN KEY (workout_plan_id) REFERENCES workout_plan(id) ON DELETE CASCADE
);


--**********************************************************************************************

CREATE TABLE user_meal (
    id SERIAL PRIMARY KEY,  
    weight DECIMAL(5, 2) NOT NULL,
    waist DECIMAL(5, 2) NOT NULL,
    type VARCHAR(10) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    image TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TRIGGER set_timestamp_user_meal
BEFORE UPDATE ON user_meal
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();


CREATE TABLE user_request_meal(
    user_id INT NOT Null,
    user_meal_id INT NOT Null,
    PRIMARY KEY (user_meal_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (user_meal_id) REFERENCES user_meal(id) ON DELETE CASCADE
);



--**********************************************************************************************


CREATE TABLE meal_supplement (
    id SERIAL PRIMARY KEY,
    breakfast TEXT,
    lunch TEXT,
    dinner TEXT,
    supplement TEXT,
    expire_time INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TRIGGER set_timestamp_meal_supplement
BEFORE UPDATE ON meal_supplement
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();



CREATE TABLE user_meal_meal_supplement(
    meal_supplement_id INT NOT Null,
    user_meal_id INT NOT Null UNIQUE,
    PRIMARY KEY (meal_supplement_id),
    FOREIGN KEY (meal_supplement_id) REFERENCES meal_supplement(id) ON DELETE CASCADE,
    FOREIGN KEY (user_meal_id) REFERENCES user_meal(id) ON DELETE CASCADE
);


CREATE TABLE workout_plan_meal_supplement(
    meal_supplement_id INT NOT Null,
    workout_plan_id INT NOT Null,
    PRIMARY KEY (meal_supplement_id, workout_plan_id),
    FOREIGN KEY (meal_supplement_id) REFERENCES meal_supplement(id) ON DELETE CASCADE,
    FOREIGN KEY (workout_plan_id) REFERENCES workout_plan(id) ON DELETE CASCADE
);




--**********************************************************************************************



CREATE TABLE user_duplicates (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(20)
);


CREATE OR REPLACE FUNCTION insert_into_user_duplicates()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_duplicates (user_name, email, phone_number)
    VALUES (NEW.user_name, NEW.email, NEW.phone_number);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER user_insert_trigger
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION insert_into_user_duplicates();


CREATE TRIGGER coach_insert_trigger
AFTER INSERT ON coach
FOR EACH ROW
EXECUTE FUNCTION insert_into_user_duplicates();




CREATE TRIGGER admin_insert_trigger
AFTER INSERT ON admin
FOR EACH ROW
EXECUTE FUNCTION insert_into_user_duplicates();


--**********************************************************************************************



CREATE OR REPLACE FUNCTION update_user_duplicates()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE user_duplicates
    SET user_name = NEW.user_name,
        email = NEW.email,
        phone_number = NEW.phone_number
    WHERE user_name = OLD.user_name AND email = OLD.email AND phone_number = OLD.phone_number;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER user_update_trigger
AFTER UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_user_duplicates();

CREATE TRIGGER coach_update_trigger
AFTER UPDATE ON coach
FOR EACH ROW
EXECUTE FUNCTION update_user_duplicates();

CREATE TRIGGER admin_update_trigger
AFTER UPDATE ON admin
FOR EACH ROW
EXECUTE FUNCTION update_user_duplicates();




CREATE OR REPLACE FUNCTION delete_from_user_duplicates()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM user_duplicates
    WHERE user_name = OLD.user_name AND email = OLD.email AND phone_number = OLD.phone_number;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;




CREATE TRIGGER user_delete_trigger
AFTER DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION delete_from_user_duplicates();

CREATE TRIGGER coach_delete_trigger
AFTER DELETE ON coach
FOR EACH ROW
EXECUTE FUNCTION delete_from_user_duplicates();

CREATE TRIGGER admin_delete_trigger
AFTER DELETE ON admin
FOR EACH ROW
EXECUTE FUNCTION delete_from_user_duplicates();


--**********************************************************************************************

--not adding updated_at now


CREATE TABLE gym (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    license_number VARCHAR(100) NOT NULL,
    license_image TEXT,
    location TEXT,
    image TEXT,
    sport_facilities TEXT,
    welfare_facilities TEXT,
    rating INTEGER DEFAULT 0 CHECK (rating BETWEEN 0 AND 5),
    verification_status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (owner_id) REFERENCES coach (id) ON DELETE CASCADE
);


CREATE TABLE coach_comment (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    coach_id INTEGER NOT NULL,
    comment TEXT,
    rating INTEGER DEFAULT 0 CHECK (rating BETWEEN 0 AND 5),
    date VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (coach_id) REFERENCES coach (id) ON DELETE CASCADE
);


CREATE TABLE gym_comment (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    gym_id INTEGER NOT NULL,
    comment TEXT,
    rating INTEGER DEFAULT 0 CHECK (rating BETWEEN 0 AND 5),
    date VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (gym_id) REFERENCES gym (id) ON DELETE CASCADE
);


CREATE TABLE user_gym_registration(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    gym_id INTEGER NOT NULL,
    registered_sessions INTEGER DEFAULT 0,
    registered_days INTEGER DEFAULT 0,
    is_vip BOOLEAN DEFAULT FALSE,
    remaining_sessions INTEGER DEFAULT 0,
    remaining_days INTEGER DEFAULT 0,
    is_expired BOOLEAN DEFAULT FALSE,
    date VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (gym_id) REFERENCES gym (id) ON DELETE CASCADE
);


CREATE TABLE coach_plan_price (
    id SERIAL PRIMARY KEY,
    coach_id INTEGER NOT NULL UNIQUE ,
    exercise_price INTEGER NOT NULL CHECK (exercise_price >= 0),
    meal_price INTEGER NOT NULL CHECK (meal_price >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (coach_id) REFERENCES coach (id)  ON DELETE CASCADE
);


CREATE TABLE gym_plan_price (
    id SERIAL PRIMARY KEY,
    gym_id INTEGER NOT NULL,
    session_counts INTEGER NOT NULL CHECK (session_counts >= 0),
    duration_days INTEGER NOT NULL CHECK (duration_days >= 0),
    is_vip BOOLEAN DEFAULT FALSE,
    price INTEGER NOT NULL CHECK (price >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (gym_id) REFERENCES gym (id) ON DELETE CASCADE
);


CREATE TABLE coach_gym(
    coach_id INTEGER NOT NULL,
    gym_id INTEGER NOT NULL,

    FOREIGN KEY (coach_id) REFERENCES coach (id) ON DELETE CASCADE,
    FOREIGN KEY (gym_id) REFERENCES gym (id) ON DELETE CASCADE,
    PRIMARY KEY (coach_id, gym_id)
);