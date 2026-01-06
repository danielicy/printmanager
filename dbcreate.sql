CREATE TABLE job_status_names (
  jobstatus_id SERIAL PRIMARY KEY, -- Use SERIAL for auto-incrementing integer
  jobstatus_name VARCHAR(200) NOT NULL, -- VARCHAR for string data type
  UNIQUE (jobstatus_name) -- Add unique constraint to enforce distinct names
);

CREATE TABLE job_type (
  jobtype_id SERIAL PRIMARY KEY, -- Use SERIAL for auto-incrementing integer
  jobtype_name VARCHAR(200) NOT NULL, -- VARCHAR for string data type
  jobtype_max_retries SMALLINT NOT NULL DEFAULT 7 -- SMALLINT for short integer, DEFAULT value
);

CREATE TABLE session_key_value_log (
  id SERIAL PRIMARY KEY, -- Use SERIAL for auto-incrementing integer
  global_session_id CHAR(36) REFERENCES jobs_contentstore(global_session) ON DELETE SET NULL, -- Foreign key to jobs_contentstore
  jobtype_id INTEGER REFERENCES job_type(jobtype_id) ON DELETE SET NULL, -- Foreign key to job_type
  key VARCHAR(100) NOT NULL, -- Key value
  value VARCHAR(10000) NULL, -- Value (longer max_length)
  UNIQUE (global_session_id, key) -- Unique constraint on (global_session_id, key) pair
);

CREATE TABLE jobs_contentstore (
  global_session CHAR(36) PRIMARY KEY, -- CHAR for fixed-length string, max_length from model
  bvp_content_create TEXT, -- TEXT for large text content
  bvp_content_update TEXT, -- TEXT for large text content
  account_name VARCHAR(30) NOT NULL -- VARCHAR for string data type
);

CREATE TABLE jobs_status (
  jobid SERIAL PRIMARY KEY, -- Use SERIAL for auto-incrementing integer
  jobstatus_id INTEGER REFERENCES job_status_names(jobstatus_id) ON DELETE SET NULL, -- Foreign key to job_status_names
  jobtype_id INTEGER REFERENCES job_type(jobtype_id) ON DELETE SET NULL, -- Foreign key to job_type
  job_priority INTEGER NOT NULL DEFAULT 50, -- Job priority
  job_failure_count INTEGER NOT NULL DEFAULT 0, -- Job failure count
  job_step INTEGER NOT NULL DEFAULT 0, -- Job steps
  global_session_id CHAR(36) REFERENCES jobs_contentstore(global_session) ON DELETE SET NULL, -- Foreign key to jobs_contentstore
  fullfilename VARCHAR(1000) NULL, -- Full filename
  task_id VARCHAR(50) NULL, -- Task ID
  UNIQUE (global_session_id, jobid) -- Unique constraint for (global_session_id, jobid) pair
);




