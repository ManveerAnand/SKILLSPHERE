-- User Table
CREATE TABLE "User" (
  user_id    SERIAL PRIMARY KEY,
  name       VARCHAR(100) NOT NULL,
  email      VARCHAR(255) UNIQUE NOT NULL,
  role       VARCHAR(50)  NOT NULL,
  created_at TIMESTAMP    NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP    NOT NULL DEFAULT NOW()
);

-- Course Table
CREATE TABLE "Course" (
  course_id     SERIAL PRIMARY KEY,
  instructor_id INT REFERENCES "User"(user_id) ON DELETE SET NULL,
  title         VARCHAR(255) NOT NULL,
  description   TEXT,
  price         DECIMAL(10,2),
  created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Chapter Table
CREATE TABLE "Chapter" (
  chapter_id  SERIAL PRIMARY KEY,
  course_id   INT NOT NULL REFERENCES "Course"(course_id) ON DELETE CASCADE,
  title       VARCHAR(255) NOT NULL,
  video_url   VARCHAR(500),
  content     TEXT,
  created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Enrollment Table
CREATE TABLE "Enrollment" (
  enrollment_id SERIAL PRIMARY KEY,
  user_id       INT NOT NULL REFERENCES "User"(user_id) ON DELETE CASCADE,
  course_id     INT NOT NULL REFERENCES "Course"(course_id) ON DELETE CASCADE,
  progress      DECIMAL(5,2) DEFAULT 0,
  status        VARCHAR(50),
  created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMP NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, course_id)
);

-- Transaction Table
CREATE TABLE "Transaction" (
  transaction_id SERIAL PRIMARY KEY,
  user_id        INT NOT NULL REFERENCES "User"(user_id) ON DELETE CASCADE,
  course_id      INT NOT NULL REFERENCES "Course"(course_id) ON DELETE CASCADE,
  amount         DECIMAL(10,2),
  status         VARCHAR(50),
  created_at     TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at     TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Feature_Store Table
CREATE TABLE "Feature_Store" (
  feature_store_id SERIAL PRIMARY KEY,
  course_id        INT NOT NULL REFERENCES "Course"(course_id) ON DELETE CASCADE,
  metadata         JSONB,
  version          INT,
  created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at       TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Feature_Store_Audit Table
CREATE TABLE "Feature_Store_Audit" (
  audit_id         SERIAL PRIMARY KEY,
  feature_store_id INT NOT NULL REFERENCES "Feature_Store"(feature_store_id) ON DELETE CASCADE,
  changed_by       INT REFERENCES "User"(user_id) ON DELETE SET NULL,
  changes          JSONB,
  created_at       TIMESTAMP NOT NULL DEFAULT NOW()
);