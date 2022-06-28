CREATE TYPE "history_status" AS ENUM (
  'created',
  'in_progress',
  'done'
);

CREATE TYPE "task_status" AS ENUM (
  'created',
  'in_progress',
  'done',
  'canceled',
  'process_error'
);

CREATE TABLE "notification" (
  "id" SERIAL PRIMARY KEY,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NOT NULL,
  "template_id" int NOT NULL,
  "template_params" json,
  "role" varchar,
  "permission" varchar,
  "email" varchar
);

CREATE TABLE "template" (
  "id" SERIAL PRIMARY KEY,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NOT NULL,
  "name" varchar UNIQUE NOT NULL,
  "description" varchar NOT NULL,
  "path" varchar UNIQUE NOT NULL,
  "params" json NOT NULL
);

CREATE TABLE "history" (
  "id" SERIAL PRIMARY KEY,
  "created_at" timestamp NOT NULL,
  "notification_id" int,
  "status" history_status NOT NULL
);

CREATE TABLE "task" (
  "id" SERIAL PRIMARY KEY,
  "created_at" timestamp,
  "updated_at" timestamp,
  "execution_time" timestamp,
  "notification_id" int,
  "status" task_status
);

ALTER TABLE "notification" ADD FOREIGN KEY ("template_id") REFERENCES "template" ("id");

ALTER TABLE "history" ADD FOREIGN KEY ("notification_id") REFERENCES "notification" ("id");

ALTER TABLE "task" ADD FOREIGN KEY ("notification_id") REFERENCES "notification" ("id");
