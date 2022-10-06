from django.urls import path
from casino.apps import CasinoConfig
from casino.views import (
    Home,
    StartGame,
    StopGameView,
    RollView,
    # CloseSessionView
)

app_name: str = CasinoConfig.name


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("start/", StartGame.as_view(), name="start"),
    path("roll/", RollView.as_view(), name="roll"),
    path("stop/", StopGameView.as_view(), name="stop"),
]
