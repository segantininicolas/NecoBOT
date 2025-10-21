import asyncio
import json
import os
from ossapi import OssapiAsync
from dotenv import load_dotenv

load_dotenv()

secret = os.getenv('client_secret_osu')
id = os.getenv('client_id_osu')
api = OssapiAsync(id, secret)
    
async def profile(profile: str):
    try:
        user = await api.user(profile)

        dados_perfil = {
            "id": user.id,
            "username": user.username,
            "avatar_url": user.avatar_url,
            "cover_url": user.cover_url,
            "team_flag_url": user.team.flag_url if user.team else None,
            "team_name": user.team.name if user.team else None,
            "country": user.country.name,
            "country_code": user.country.code,
            "pp": int(round(user.statistics.pp)),
            "rank": user.statistics.global_rank if user.statistics else None,
            "country_rank": user.statistics.country_rank if user.statistics else None,
            "rank_highest": user.rank_highest.rank,
            "accuracy": round(user.statistics.hit_accuracy, 2),
            "play_count": user.statistics.play_count,
            "level": user.statistics.level.current,
            "grade_SSH": user.statistics.grade_counts.ssh,
            "grade_SS": user.statistics.grade_counts.ss,
            "grade_SH": user.statistics.grade_counts.sh,
            "grade_S": user.statistics.grade_counts.s,
            "grade_A": user.statistics.grade_counts.a,
        }

        nome_arquivo = f"data.json"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados_perfil, f, ensure_ascii=False, indent=4)

        return nome_arquivo

        
    except ValueError:
        return None




