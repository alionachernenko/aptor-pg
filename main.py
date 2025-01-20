from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from models import Interaction
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from jobs import update_embeddings_job
from fastapi_utilities import repeat_every
from dependencies import get_recommender, get_profile_builder, get_interactions_repository, get_embedder
from recommender import Recommender
from profile_builder import ProfileBuilder
from embedder import Embedder
from interactions_repository import InteractionsRepository


@asynccontextmanager
async def lifespan(app: FastAPI, embedder: Embedder = Depends(get_embedder)):
    load_dotenv()
    embedder.create_items_embeddings()
    yield

app = FastAPI(lifespan=lifespan)


@repeat_every(seconds=60 * 60 * 24)
async def update_embeddings(background_tasks: BackgroundTasks):
    background_tasks.add_task(update_embeddings_job)


@app.post("/interaction")
def track_interaction(interaction: Interaction, profile_builder: ProfileBuilder = Depends(get_profile_builder), interactions_repository: InteractionsRepository = Depends(get_interactions_repository)):
    try:
        interactions_repository.add(interaction)
        profile = profile_builder.build_user_profile(interaction.user_id)
        return profile
    except:
        raise HTTPException(status_code="500",
                            detail="Failed to track interaction")


@app.get("/recommendations")
def retrieve_recommendations(user_id, recommender: Recommender = Depends(get_recommender)):
    try:
        recommendations = recommender.get_recommendations(user_id)
        return recommendations
    except:
        raise HTTPException(status_code="500", detail="Something went wrong")
