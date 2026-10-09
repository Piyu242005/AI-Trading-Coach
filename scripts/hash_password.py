"""Generate a PBKDF2 password hash for AI_TRADING_COACH_USERS_JSON."""
import getpass
import hashlib
import secrets


def main() -> None:
    password = getpass.getpass("Password to hash (input hidden): ")
    if len(password) < 12:
        raise SystemExit("Use a password with at least 12 characters.")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310_000)
    print(f"{salt.hex()}:{digest.hex()}")
    print("Store the output as the value for this user ID in AI_TRADING_COACH_USERS_JSON.")
    print("Never commit the password or the environment variable to source control.")


if __name__ == "__main__":
    main()
