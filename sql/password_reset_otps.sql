-- Bảng OTP quên mật khẩu
CREATE TABLE IF NOT EXISTS password_reset_otps (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id),
  email VARCHAR NOT NULL,
  otp_hash VARCHAR NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  attempts INTEGER NOT NULL DEFAULT 0,
  is_used BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_password_reset_otps_id ON password_reset_otps (id);
CREATE INDEX IF NOT EXISTS ix_password_reset_otps_user_id ON password_reset_otps (user_id);
CREATE INDEX IF NOT EXISTS ix_password_reset_otps_email ON password_reset_otps (email);
