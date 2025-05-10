# backend/game_state.py
import json
from database import DatabaseManager
from typing import Optional, Dict, List

class GameStateManager:
    @staticmethod
    def create_save(player_name: str, initial_state: dict) -> int:
        with DatabaseManager() as cursor:
            cursor.execute(
                "INSERT INTO saves (player_name, game_state) VALUES (?, ?)",
                (player_name, json.dumps(initial_state)))
            return cursor.lastrowid

    @staticmethod
    def update_state(save_id: int, new_state: dict):
        with DatabaseManager() as cursor:
            cursor.execute(
                "UPDATE saves SET game_state = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (json.dumps(new_state), save_id))

    @staticmethod
    def log_history(save_id: int, event_type: str, data: dict):
        with DatabaseManager() as cursor:
            cursor.execute(
                "INSERT INTO history (save_id, event_type, event_data) VALUES (?, ?, ?)",
                (save_id, event_type.upper(), json.dumps(data)))

    @staticmethod
    def get_recent_history(save_id: int, limit: int = 5) -> list[dict]:
        with DatabaseManager() as cursor:
            cursor.execute(
                "SELECT event_type, event_data, created_at FROM history "
                "WHERE save_id = ? ORDER BY created_at DESC LIMIT ?",
                (save_id, limit))
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_save(save_id: int) -> dict | None:
        with DatabaseManager() as cursor:
            cursor.execute(
                "SELECT id, player_name, game_state, created_at "
                "FROM saves WHERE id = ?",
                (save_id,)
            )
            result = cursor.fetchone()
            return dict(result) if result else None