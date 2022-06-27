from asyncpg import Pool

pool = None


def get_repository_pool() -> Pool:
    return pool