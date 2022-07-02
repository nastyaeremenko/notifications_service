CREATE TYPE "notification_types" AS ENUM (
  'email',
  'sms',
  'telegram'
);

ALTER TABLE "notification" ADD COLUMN "notification_type" notification_types DEFAULT 'email';
